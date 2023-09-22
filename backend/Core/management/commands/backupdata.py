import asyncio
from django.core.management.base import BaseCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from Core.utils import perform_database_backup


class Command(BaseCommand):
    help = 'Backup database data every hour using asyncio and apscheduler'

    def handle(self, *args, **options):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(perform_database_backup, 'interval', hours=1)
        scheduler.start()

        try:
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            scheduler.shutdown()
