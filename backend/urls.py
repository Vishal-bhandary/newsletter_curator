from django.contrib import admin
from django.urls import path
from newsletter import views
from newsletter.admin_views import analytics_dashboard, resend_newsletter

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin
    path('', views.article_list, name='article_list'),
    path('archive/', views.newsletter_archive, name='newsletter_archive'),
    path('archive/<int:log_id>/', views.view_newsletter, name='view_newsletter'),

    # 💡 Rename these to avoid conflict with Django admin:
    path('dashboard/analytics/', analytics_dashboard, name='analytics_dashboard'),
    path('dashboard/resend/<int:pk>/', resend_newsletter, name='resend_newsletter'),
]
