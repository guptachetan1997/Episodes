from django_cron import CronJobBase, Schedule
from tvshow.models import Show
from django.db.models import Q
from django.utils import timezone
from _datetime import timedelta

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 60*24 # every day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'tvshow.cron'    # a unique code

    def do(self):
        print("Running update show cron.")
        show_list = Show.objects.filter(Q(runningStatus='Continuing'))
        for show in show_list:
            try:
                flag = True#show.update_show_data()
                if flag:
                    print("Show {} was udpdated at {}".format(show.seriesName, timezone.now()))
                    show.last_updated = timezone.now()
                    show.save()
            except Exception as e:
                print(e)