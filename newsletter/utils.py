from .models import NewsletterLog  # Add this at the top with other imports
import pandas as pd
from datetime import datetime, timedelta
import pytz
from .models import Article, Subscriber
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def get_cleaned_articles():
    ist = pytz.timezone("Asia/Kolkata")
    now_ist = datetime.now(ist)
    from_datetime = now_ist - timedelta(days=3)
    to_datetime = now_ist

    articles = Article.objects.filter(
        published_at__gte=from_datetime,
        published_at__lte=to_datetime
    ).order_by("-published_at")

    if not articles.exists():
        return pd.DataFrame()

    data = list(articles.values(
        "title", "summary", "url", "image_url", "published_at", "source"
    ))

    df = pd.DataFrame(data)
    df.dropna(subset=["summary"], inplace=True)
    df.drop_duplicates(subset=["url"], inplace=True)

    def truncate_summary(text, max_length):
        if not text:
            return ""
        if len(text) <= max_length:
            return text
        truncated_text = text[:max_length]
        last_space = truncated_text.rfind(' ')
        if last_space > (max_length * 0.8):
            return truncated_text[:last_space] + "..."
        return truncated_text + "..."

    df["summary"] = df["summary"].apply(lambda x: truncate_summary(x, 300))
    df["published_at"] = df["published_at"].apply(
        lambda dt: dt.astimezone(ist).strftime("%b %d, %Y %H:%M %Z") if dt.tzinfo else dt.strftime("%b %d, %Y %H:%M")
    )

    return df


def send_newsletter(frequency='weekly'):
    subscribers = Subscriber.objects.filter(frequency=frequency)
    if not subscribers.exists():
        print(f"No {frequency} subscribers to send to.")
        return

    df = get_cleaned_articles()
    if df.empty:
        print("No articles available to send.")
        return

    for sub in subscribers:
        # Filter articles based on subscriber's selected categories
        sub_categories = sub.categories  # this is a list
        filtered_df = df[df['source'].str.lower().isin(sub_categories)]

        if filtered_df.empty:
            print(f"❌ No matching articles for {sub.email}. Skipping.")
            continue

        articles = filtered_df.to_dict('records')

        html_content = render_to_string('newsletter/email_template.html', {
            'articles': articles
        })

        msg = EmailMultiAlternatives(
            subject=f"🗞️ Your {frequency.capitalize()} Newsletter",
            body="View this email in HTML mode.",
            from_email="aryavbhandary@gmail.com",
            to=[sub.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print(f"✅ Sent to {sub.email}")

    # Log the newsletter once (we log weekly only for now)
    if frequency == 'weekly':
        NewsletterLog.objects.create(
            subject=f"🗞️ {frequency.capitalize()} Newsletter",
            content=html_content
        )
        print("📝 Newsletter logged.")