from django.core.management.base import BaseCommand
from newsletter.utils import send_newsletter

class Command(BaseCommand):
    help = 'Send weekly newsletter to all subscribers manually'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Starting to send newsletters..."))
        send_newsletter()
        self.stdout.write(self.style.SUCCESS("🎉 Newsletters sent!"))
