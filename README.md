# Google Play Scraper for Python

A lightweight Python library for scraping publicly available data from the Google Play Store.

## What it does

- Searches for apps and retrieves basic info (title, rating, installs, etc.)
- Fetches app reviews with reviewer name, rating, date, and text
- Lists current permissions and tracks changes over time
- Extracts search-friendly keywords from app descriptions

## Installation

```bash
pip install google_play_scraper beautifulsoup4 scrapy
```

## Example usage

```python
from google_play_scraper import search, Sort

# Find the newest app matching your query
results = search(query="tiktok", sort=Sort.NEWEST)
app = results[0]

print(f"Title: {app.title}")
print(f"Rating: {app.rating} ({app.review_count} reviews)")
print(f"Installs: {app.install_count}")
```

Get detailed review data:

```python
from google_play_scraper import reviews

reviews_list, _ = reviews(app.app_id)
for r in reviews_list[:5]:
    print(f"[{r['score']}★] {r['reviewText'][:80]}…")
```

## Dependencies

- `beautifulsoup4` — HTML parsing
- `scrapy` — HTTP requests and parsing logic

Both are installed automatically with the package above.

## Contributing

Bug reports and PRs are welcome. See the [issues page](<repository-url>) to get started.

## License

MIT — see `LICENSE` for details.