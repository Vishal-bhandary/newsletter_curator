# newsletter/admin_views.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from collections import Counter
from django.db.models import Count
from .models import Subscriber, NewsletterLog

@staff_member_required
def resend_newsletter(request, pk):
    log = NewsletterLog.objects.get(pk=pk)
    subscribers = Subscriber.objects.filter(frequency='weekly')  # or all

    for sub in subscribers:
        msg = EmailMultiAlternatives(
            subject=f"[Resent] {log.subject}",
            body="View this email in HTML mode.",
            from_email="aryavbhandary@gmail.com",
            to=[sub.email]
        )
        msg.attach_alternative(log.content, "text/html")
        msg.send()

    messages.success(request, f"✅ Resent newsletter to {subscribers.count()} users.")
    return HttpResponseRedirect("/admin/newsletter/newsletterlog/")

@staff_member_required
def analytics_dashboard(request):
    # Count all subscribers
    total_subscribers = Subscriber.objects.count()

    # Category preference breakdown
    category_breakdown = (
        Subscriber.objects.values('categories__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Frequency breakdown
    frequency_breakdown = (
        Subscriber.objects.values('frequency')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    context = {
        'total_subscribers': total_subscribers,
        'category_breakdown': category_breakdown,
        'frequency_breakdown': frequency_breakdown,
    }

    return render(request, "newsletter/admin_dashboard.html", context)
