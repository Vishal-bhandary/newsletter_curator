from django_cron import CronJobBase, Schedule
from .utils import send_newsletter
from datetime import datetime

class DailyNewsletterCronJob(CronJobBase):
    RUN_AT_TIMES = ['09:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'newsletter.daily_newsletter'

    def do(self):
        send_newsletter(frequency='daily')


class WeeklyNewsletterCronJob(CronJobBase):
    RUN_AT_TIMES = ['10:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'newsletter.weekly_newsletter'

    def do(self):
        if datetime.today().weekday() == 5:  # Saturday
            send_newsletter(frequency='weekly')
