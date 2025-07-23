import requests
from django.core.management.base import BaseCommand
from newsletter.models import Article
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta
import pytz
import time

API_KEY = "709c93764c3a433d807b5c7a539c92cb"
BASE_URL = "https://newsapi.org/v2/everything"
QUERY = "technology OR science OR politics OR world OR startup OR ai"
PAGE_SIZE = 20  # NewsAPI free tier allows max 100 results

# Character limits
MAX_TITLE_LENGTH = 255
MAX_SUMMARY_LENGTH = 1000
MAX_URL_LENGTH = 2048
MAX_IMAGE_URL_LENGTH = 2048
MAX_SOURCE_LENGTH = 100

def truncate(value, max_length):
    return (value[:max_length]) if value and len(value) > max_length else value

class Command(BaseCommand):
    help = 'Fetch latest news articles and save them with pagination support'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=1, help='Number of past days to fetch (default: 1)')

    def handle(self, *args, **options):
        days = options['days']
        self.stdout.write(self.style.NOTICE(f"Fetching articles from the last {days} day(s)..."))

        # Timezone handling: use UTC for API consistency
        utc_now = datetime.utcnow().replace(microsecond=0)
        utc_from = utc_now - timedelta(days=days)

        total_saved = 0
        page = 1

        while True:
            params = {
                "q": QUERY,
                "from": utc_from.isoformat() + "Z",  # e.g. 2024-07-20T00:00:00Z
                "to": utc_now.isoformat() + "Z",
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": PAGE_SIZE,
                "page": page,
                "apiKey": API_KEY,
            }

            try:
                response = requests.get(BASE_URL, params=params)
                if response.status_code != 200:
                    self.stderr.write(f"API error (page {page}): {response.status_code} - {response.text}")
                    break
            except requests.RequestException as e:
                self.stderr.write(f"Request failed: {e}")
                break

            data = response.json()
            articles = data.get("articles", [])

            if not articles:
                self.stdout.write(f"No articles found on page {page}.")
                break

            for item in articles:
                title = truncate(item.get('title'), MAX_TITLE_LENGTH)
                summary = truncate(item.get('description'), MAX_SUMMARY_LENGTH)
                url = truncate(item.get('url'), MAX_URL_LENGTH)
                image_url = truncate(item.get('urlToImage'), MAX_IMAGE_URL_LENGTH)
                published_at = parse_datetime(item.get('publishedAt'))
                source = truncate(item.get('source', {}).get('name', 'Unknown'), MAX_SOURCE_LENGTH)

                if not title:
                    self.stdout.write(self.style.WARNING("Skipped article with no title"))
                    continue

                if not Article.objects.filter(url=url).exists():
                    Article.objects.create(
                        title=title,
                        summary=summary,
                        url=url,
                        image_url=image_url,
                        published_at=published_at or datetime.utcnow().replace(tzinfo=pytz.UTC),
                        source=source,
                    )
                    total_saved += 1
                    self.stdout.write(self.style.SUCCESS(f"✅ Saved: {title}"))
                else:
                    self.stdout.write(self.style.WARNING(f"⏩ Duplicate skipped: {url}"))

            if page >= 5:
                self.stdout.write("🛑 Reached API free-tier page limit (5 pages).")
                break

            page += 1
            time.sleep(1)  # Rate limiting

        self.stdout.write(self.style.SUCCESS(f"🎉 Fetch complete. {total_saved} new articles saved."))
