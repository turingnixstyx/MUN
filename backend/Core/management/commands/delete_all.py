from django.core.management.base import BaseCommand, CommandParser, CommandError
from django.apps import apps


class Command(BaseCommand):
    help = "Delete all entries of the specific Model"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('model_name', type=str, help='Name of the model to delete entries from')

    def handle(self, *args, **kwargs):
        model_name = kwargs.get('model_name')

        try:
            model = apps.get_model('Core', model_name)

        except LookupError:
            raise CommandError(f"Model '{model_name}' not found")
        
        model.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS(f'All entries in {model_name} have been deleted'))