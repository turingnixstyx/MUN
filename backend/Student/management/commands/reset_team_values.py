from django.core.management.base import BaseCommand

from Student.models import Students


class Command(BaseCommand):
    help = "Reset team values to None for testing purposes"

    def handle(self, *args, **options):
        # Assuming the model has only one record
        instances = Students.objects.all()
        if len(instances) > 0:
            for instance in instances:
                instance.team = None
                instance.save()
                self.stdout.write(
                    self.style.SUCCESS(f"{instance.name}'s teams value set to None")
                )
        else:
            self.stdout.write(self.style.WARNING("No instances found for the Students"))
