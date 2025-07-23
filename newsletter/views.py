from django.shortcuts import render, redirect
from .models import Article
from .forms import SubscriberForm
from django.contrib import messages
from .models import Subscriber
from django.shortcuts import get_object_or_404
from .models import NewsletterLog


def article_list(request):
    articles = Article.objects.order_by('-published_at')[:20]
    form = SubscriberForm()

    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not Subscriber.objects.filter(email=email).exists():
                form.save()
                messages.success(request, "You're subscribed successfully!")
            else:
                messages.warning(request, "You’re already subscribed.")
            return redirect('article_list')

    return render(request, 'newsletter/article_list.html', {
        'articles': articles,
        'form': form
    })


def newsletter_archive(request):
    logs = NewsletterLog.objects.order_by('-sent_at')
    return render(request, 'newsletter/newsletter_archive.html', {'logs': logs})

def view_newsletter(request, log_id):
    log = get_object_or_404(NewsletterLog, id=log_id)
    return render(request, 'newsletter/view_newsletter.html', {'log': log})

