from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    # Add this line for the summary field
    summary = models.TextField(max_length=1000, blank=True, null=True) # Use TextField for longer text
    url = models.URLField(max_length=2048, unique=True) # url should be unique
    image_url = models.URLField(max_length=2048, blank=True, null=True)
    published_at = models.DateTimeField()
    source = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True) # Optional: for tracking when it was added to your DB

    class Meta:
        # Add an ordering to display newest articles first by default
        ordering = ['-published_at']
        # You might also consider a unique_together constraint if title + source should be unique
        # unique_together = (('title', 'source'),)

    def __str__(self):
        return self.title

class Subscriber(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Technology'),
        ('ai', 'Artificial Intelligence'),
        ('politics', 'Politics'),
        ('science', 'Science'),
        ('world', 'World'),
        ('startup', 'Startup'),
    ]

    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]

    email = models.EmailField(unique=True)
    categories = models.JSONField(default=list)  # Store list of selected categories
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='weekly')
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class NewsletterLog(models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()  # store rendered HTML content
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Newsletter sent on {self.sent_at.strftime('%Y-%m-%d %H:%M')}"
