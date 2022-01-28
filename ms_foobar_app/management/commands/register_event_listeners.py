from django.core.management.base import BaseCommand

from ms_foobar_app.events.event_listener import EventListener


class Command(BaseCommand):
    def handle(self, *args, **options):
        bus = EventListener()
        bus.run()
        bus.subscribe()
