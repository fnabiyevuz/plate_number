from django.db import models


class Car(models.Model):
    plate_number = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plate_number}"
