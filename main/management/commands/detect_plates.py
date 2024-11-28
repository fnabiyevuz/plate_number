from django.core.management.base import BaseCommand
from main.models import Car
from main.utils import detect_license_plates


class Command(BaseCommand):
    help = "Detect license plates and save them to the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting license plate detection...")

        try:
            for plate_number in detect_license_plates():
                # Save the detected plate number to the database
                car = Car.objects.create(plate_number=plate_number)
                self.stdout.write(f"Saved plate: {car.plate_number}")
        except Exception as e:
            self.stderr.write(f"Error: {e}")
