from django.apps import apps
from django.core.management.base import (
    BaseCommand,
    CommandError,
    CommandParser,
)


class Command(BaseCommand):
    help = "Delete all entries of the specific Model"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "model_name",
            type=str,
            help="Name of the model to delete entries from",
        )

    def handle(self, *args, **kwargs):
        model_name = kwargs.get("model_name")
        print("hello world")

        if model_name == "*":
            # Delete all entries in all models of the app
            app_name = "Core"  # Replace with your app name
            all_models = apps.all_models[app_name]
            for model in all_models.values():
                model.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"All entries in {app_name} models have been deleted"))
        else:
            try:
                model = apps.get_model("Core", model_name)
            except LookupError:
                raise CommandError(f"Model '{model_name}' not found")

            model.objects.all().delete()

        model.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"All entries in {model_name} have been deleted"
            )
        )
