from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.
class Car(models.Model):
    plate_number=models.CharField(max_length=10)
    brand=models.CharField(max_length=100)
    model=models.CharField(max_length=30)
    year=models.SmallIntegerField()
    gear=models.CharField(max_length=30)
    rent_per_day=models.IntegerField()
    availability=models.BooleanField()

    def __str__(self):
        return f"{self.plate_number} - {self.brand}- {self.model}"
    


class Reservation(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    car=models.ForeignKey(Car,on_delete=models.CASCADE,related_name="reservations")
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
   

    def __str__(self):
        return f"{self.user} - {self.car}"
    
    def save(self, *args, **kwargs):
        # Rezervasyon tarih çakışması kontrolü
        if Reservation.objects.filter(car=self.car, start_date__lt=self.end_date, end_date__gt=self.start_date).exists():
            raise ValidationError("This car is not available for the selected dates.")
        
        super().save(*args, **kwargs)


def clean(self):
    # from django.utils import timezone
    # now = timezone.now()

    # if self.start_date < now:
    #     raise ValidationError("You cannot make a reservation for past dates.")
    # if self.end_date < now:
    #     raise ValidationError("You cannot make a reservation with an end date in the past.")
    
    existing_reservations = Reservation.objects.filter(user=self.user, start_date__lt=self.end_date, end_date__gt=self.start_date)
    
    if self.pk:
        existing_reservations = existing_reservations.exclude(pk=self.pk)
    
    if existing_reservations.exists():
        raise ValidationError("You already have a reservation for the selected dates.")
