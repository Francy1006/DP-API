from django.utils import timezone


class DjangoClock:
    def now(self):
        return timezone.now()

    def format_log_timestamp(self, value):
        return timezone.localtime(value).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
