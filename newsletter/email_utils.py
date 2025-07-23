from django.template.loader import render_to_string
from newsletter.utils import get_cleaned_articles

def generate_newsletter_html():
    df = get_cleaned_articles()

    if df.empty:
        return "<p>No articles found for today.</p>"

    # Convert DataFrame to list of dictionaries for template context
    articles = df.to_dict(orient="records")

    html = render_to_string("newsletter/email_template.html", {
        "articles": articles,
    })

    return html
