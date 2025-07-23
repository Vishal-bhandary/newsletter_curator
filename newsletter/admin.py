from django.contrib import admin
from .models import Article
from .models import NewsletterLog, Subscriber
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'published_at')
    search_fields = ('title', 'summary', 'source')
    list_filter = ('source', 'published_at')
    ordering = ('-published_at',)

@admin.register(NewsletterLog)
class NewsletterLogAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sent_at')
    search_fields = ('subject',)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'frequency', 'subscribed_at')
    list_filter = ('frequency', 'subscribed_at')
    search_fields = ('email',)
