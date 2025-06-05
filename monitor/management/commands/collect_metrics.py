import time

from django.core.management.base import BaseCommand
from django.utils import timezone

from monitor.models import SystemMetrics
from monitor.utils import collect_system_metrics


class Command(BaseCommand):
    help = 'Collect system metrics and store in database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=60,
            help='Collection interval in seconds (default: 60)'
        )

    def handle(self, *args, **options):
        interval = options['interval']

        self.stdout.write(self.style.SUCCESS(
            f'Starting system metrics collection every {interval} seconds...'
        ))

        try:
            while True:
                metrics = collect_system_metrics()
                SystemMetrics.objects.create(**metrics)

                self.stdout.write(self.style.SUCCESS(
                    f'Successfully collected metrics at {timezone.now()}'
                ))

                time.sleep(interval)
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Stopping metrics collection...'))