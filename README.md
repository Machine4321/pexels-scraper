# Pexels Video & Image Bulk Scraper

The most reliable, high-performance, and cost-effective Apify Actor for downloading high-quality stock videos and images in bulk from Pexels. Designed specifically for AI video generators, faceless content creators, and marketing automation pipelines.

---

## 🚀 Why Use This Scraper?

Unlike standard scrapers that try to scrape Pexels' web pages directly—which leads to frequent IP blocks, slow page loads, and Cloudflare 403 Forbidden errors—this Actor is built on top of the **official Pexels REST API**. 

*   **100% Ban-Free & Reliable**: Zero scraping blocks, no CAPTCHAs, and no proxies needed.
*   **Insanely Fast**: Crawls and structures hundreds of videos and images in seconds.
*   **Direct MP4 Links**: Extracts direct high-resolution `.mp4` video downloads and direct image URLs. No page crawling, no scraping, just pure direct media URLs ready for download or AI models.
*   **No Pexels Account Required**: Comes with a built-in fallback API key so you can start scraping immediately. You can also provide your own free key (which gives you 25,000 free requests per month) for heavy scaling.

---

## 🛠️ Configuration Options

This Actor is highly customizable. In the Apify Console, you can configure:

*   `query` (String, **Required**): The keyword you want to search (e.g., `nature`, `cyberpunk`, `meditation`, `office`).
*   `mediaType` (Enum): Filter search results by:
    *   `Both Videos & Images` (Default)
    *   `Videos Only`
    *   `Images Only`
*   `maxResults` (Integer): The maximum number of results you want to retrieve.
*   `apiKey` (String, **Optional**): Your custom Pexels API key. If left blank, the Actor uses a default fallback key.

---

## 📊 Output Data Structure

The results are pushed directly to your default Apify Dataset. Below are examples of the data structure.

### For Videos:
```json
{
  "id": 857064,
  "type": "video",
  "search_query": "waterfall",
  "alt_text": "Video by Kelly Lacy",
  "url": "https://www.pexels.com/video/drone-shot-of-a-beautiful-waterfall-857064/",
  "width": 3840,
  "height": 2160,
  "duration_seconds": 15,
  "author_name": "Kelly Lacy",
  "author_url": "https://www.pexels.com/@kelly-lacy",
  "author_id": 12345,
  "preview_url": "https://images.pexels.com/videos/857064/pictures/preview.jpg",
  "download_url": "https://player.vimeo.com/external/371433846.hd.mp4?s=...",
  "alternative_resolutions": [
    {
      "quality": "hd",
      "file_type": "video/mp4",
      "width": 1920,
      "height": 1080,
      "link": "https://player.vimeo.com/external/371433846.hd.mp4?s=..."
    },
    {
      "quality": "sd",
      "file_type": "video/mp4",
      "width": 960,
      "height": 540,
      "link": "https://player.vimeo.com/external/371433846.sd.mp4?s=..."
    }
  ]
}
```

### For Images:
```json
{
  "id": 3408744,
  "type": "image",
  "search_query": "waterfall",
  "alt_text": "Scenic View of Waterfall",
  "url": "https://www.pexels.com/photo/scenic-view-of-waterfall-3408744/",
  "width": 4000,
  "height": 6000,
  "avg_color": "#4A5247",
  "author_name": "Tomáš Malík",
  "author_url": "https://www.pexels.com/@maliktomas",
  "author_id": 98765,
  "preview_url": "https://images.pexels.com/photos/3408744/pexels-photo-3408744.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500",
  "download_url": "https://images.pexels.com/photos/3408744/pexels-photo-3408744.jpeg",
  "alternative_resolutions": {
    "original": "https://images.pexels.com/photos/3408744/pexels-photo-3408744.jpeg",
    "large2x": "https://images.pexels.com/photos/3408744/pexels-photo-3408744.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
    "large": "https://images.pexels.com/photos/3408744/pexels-photo-3408744.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
    "medium": "https://images.pexels.com/photos/3408744/pexels-photo-3408744.jpeg?auto=compress&cs=tinysrgb&h=350&w=300",
    "small": "https://images.pexels.com/photos/3408744/pexels-photo-3408744.jpeg?auto=compress&cs=tinysrgb&h=130&w=200",
    "portrait": "https://images.pexels.com/photos/3408744/pexels-photo-3408744.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800",
    "landscape": "https://images.pexels.com/photos/3408744/pexels-photo-3408744.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200",
    "tiny": "https://images.pexels.com/photos/3408744/pexels-photo-3408744.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=200&w=280"
  }
}
```

---

## 💵 Monetization (Pay-Per-Event)

This Actor uses the **Pay-Per-Event (PPE)** pricing model. You only pay for the exact amount of items extracted.
*   **Price**: **$1.00 per 1,000 media items** ($0.001 per item).
*   **Minimum compute overhead**: Uses ultra-lightweight async Python, running in seconds on the minimal 256MB RAM allocation, keeping Apify compute usage costs near $0.

---

## 🔑 Getting Your Own Free Pexels API Key
If you are running bulk extractions (over 5,000 items per day), it is recommended to get your own API key:
1.  Go to [Pexels API Page](https://www.pexels.com/api/).
2.  Click **Get Started** and register a free account.
3.  Fill in your project name and description to instantly generate your key (it is completely free and takes 10 seconds!).
