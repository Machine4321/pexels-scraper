import asyncio
import logging
from typing import Any, Dict, List, Optional
import httpx
from apify import Actor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base URLs for Pexels API
PEXELS_SEARCH_PHOTOS_URL = "https://api.pexels.com/v1/search"
PEXELS_SEARCH_VIDEOS_URL = "https://api.pexels.com/v1/videos/search"

# We can define a default fallback API key. 
# Users can sign up for a free key at https://www.pexels.com/api/
# The key is instantly generated and has a generous limit of 25,000 requests/month.
DEFAULT_PEXELS_API_KEY = "3S8Si3wJtmaGnGTg3MCTlb9GFsdl3GFEN65gYJtg0i4A5LSuuv9KC7DT"


async def fetch_media(
    client: httpx.AsyncClient,
    url: str,
    query: str,
    headers: Dict[str, str],
    max_results: int,
    media_type: str,
) -> List[Dict[str, Any]]:
    """
    Fetches media items (photos or videos) from Pexels API.
    """
    results: List[Dict[str, Any]] = []
    page = 1
    per_page = min(80, max_results)  # Pexels API max per_page is 80

    while len(results) < max_results:
        params = {
            "query": query,
            "page": page,
            "per_page": per_page,
        }
        
        logger.info(f"Fetching page {page} for {media_type} with query '{query}'...")
        try:
            response = await client.get(url, headers=headers, params=params, timeout=20.0)
        except Exception as e:
            logger.error(f"Failed to fetch page {page} for {media_type}: {e}")
            break

        if response.status_code == 429:
            logger.warning("Rate limit hit. Waiting 5 seconds...")
            await asyncio.sleep(5)
            continue
        elif response.status_code != 200:
            logger.error(f"Error from Pexels API (Status {response.status_code}): {response.text}")
            break

        data = response.json()
        
        # Pexels returns 'photos' for photos search and 'videos' for videos search
        items = data.get("photos", []) if media_type == "photo" else data.get("videos", [])
        
        if not items:
            logger.info(f"No more {media_type} items found.")
            break

        for item in items:
            if len(results) >= max_results:
                break
            
            # Format and normalize item
            normalized_item = format_item(item, media_type)
            results.append(normalized_item)

        # Check if there is a next page
        if not data.get("next_page") or len(items) < per_page:
            break

        page += 1
        # Prevent hitting rate limits too quickly
        await asyncio.sleep(0.5)

    return results


def format_item(item: Dict[str, Any], media_type: str) -> Dict[str, Any]:
    """
    Normalizes the Pexels API item structure to a clean output format.
    """
    if media_type == "photo":
        src = item.get("src", {})
        return {
            "id": item.get("id"),
            "type": "image",
            "search_query": item.get("search_query"),  # Will be populated in main loop
            "alt_text": item.get("alt", ""),
            "url": item.get("url"),
            "width": item.get("width"),
            "height": item.get("height"),
            "avg_color": item.get("avg_color"),
            "author_name": item.get("photographer"),
            "author_url": item.get("photographer_url"),
            "author_id": item.get("photographer_id"),
            "preview_url": src.get("medium"),
            "download_url": src.get("original"),
            "alternative_resolutions": {
                "original": src.get("original"),
                "large2x": src.get("large2x"),
                "large": src.get("large"),
                "medium": src.get("medium"),
                "small": src.get("small"),
                "portrait": src.get("portrait"),
                "landscape": src.get("landscape"),
                "tiny": src.get("tiny")
            }
        }
    else:  # video
        user = item.get("user", {})
        video_files = item.get("video_files", [])
        
        # Find the best quality direct MP4 download link (usually HD or highest resolution)
        best_file = None
        for f in video_files:
            # Prefer MP4 format
            if f.get("file_type") == "video/mp4":
                if not best_file:
                    best_file = f
                else:
                    # Prefer higher resolution
                    current_pixels = (best_file.get("width") or 0) * (best_file.get("height") or 0)
                    new_pixels = (f.get("width") or 0) * (f.get("height") or 0)
                    if new_pixels > current_pixels:
                        best_file = f

        download_url = best_file.get("link") if best_file else None
        
        # List all available video resolutions
        resolutions = []
        for f in video_files:
            resolutions.append({
                "quality": f.get("quality"),
                "file_type": f.get("file_type"),
                "width": f.get("width"),
                "height": f.get("height"),
                "link": f.get("link")
            })

        video_pictures = item.get("video_pictures", [])
        preview_url = video_pictures[0].get("picture") if video_pictures else item.get("image")

        return {
            "id": item.get("id"),
            "type": "video",
            "search_query": item.get("search_query"),  # Will be populated in main loop
            "alt_text": f"Video by {user.get('name')}",
            "url": item.get("url"),
            "width": item.get("width"),
            "height": item.get("height"),
            "duration_seconds": item.get("duration"),
            "author_name": user.get("name"),
            "author_url": user.get("url"),
            "author_id": user.get("id"),
            "preview_url": preview_url,
            "download_url": download_url,
            "alternative_resolutions": resolutions
        }


async def main() -> None:
    async with Actor:
        # Load Actor input configuration
        actor_input = await Actor.get_input() or {}
        query = actor_input.get("query")
        media_type = actor_input.get("mediaType", "both")
        max_results = actor_input.get("maxResults", 50)
        api_key = actor_input.get("apiKey")

        if not query:
            logger.error("Missing 'query' parameter in configuration.")
            await Actor.fail(status_message="Search query is required.")
            return

        # Choose API key: user-provided key, or environment variable, or fallback default
        final_api_key = api_key or DEFAULT_PEXELS_API_KEY
        if not final_api_key:
            logger.error("No Pexels API Key found.")
            await Actor.fail(
                status_message="Pexels API key is required. Get a free key at https://www.pexels.com/api/"
            )
            return

        headers = {
            "Authorization": final_api_key.strip()
        }

        logger.info(f"Starting Pexels Scraper for query '{query}' (Type: {media_type}, Max Results: {max_results})")

        async with httpx.AsyncClient() as client:
            tasks = []
            
            # Fetch photos if type is 'images' or 'both'
            if media_type in ("images", "both"):
                photo_limit = max_results if media_type == "images" else (max_results // 2 + max_results % 2)
                tasks.append(
                    fetch_media(
                        client=client,
                        url=PEXELS_SEARCH_PHOTOS_URL,
                        query=query,
                        headers=headers,
                        max_results=photo_limit,
                        media_type="photo",
                    )
                )

            # Fetch videos if type is 'videos' or 'both'
            if media_type in ("videos", "both"):
                video_limit = max_results if media_type == "videos" else (max_results // 2)
                tasks.append(
                    fetch_media(
                        client=client,
                        url=PEXELS_SEARCH_VIDEOS_URL,
                        query=query,
                        headers=headers,
                        max_results=video_limit,
                        media_type="video",
                    )
                )

            # Run parallel fetches
            results_lists = await asyncio.gather(*tasks)
            
            # Combine results
            all_items: List[Dict[str, Any]] = []
            for results_list in results_lists:
                all_items.extend(results_list)

            # Add search query to metadata and cap to max results in case of minor overlap
            for item in all_items:
                item["search_query"] = query
            
            all_items = all_items[:max_results]

            logger.info(f"Extracted {len(all_items)} media items successfully.")

            # Push results to the default Apify dataset
            if all_items:
                await Actor.push_data(all_items)
                logger.info("Successfully pushed results to Apify dataset.")
            else:
                logger.warning("No media found for the query.")

        await Actor.exit()
