from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class Car(models.Model):
    #degisme ihtimali olan tüm verileri koda degil veritabanina ekleriz
    GEAR=(
        ('a','automatic'),
        ('m', 'manual'),
    )
    plate_number=models.CharField(max_length=20, unique=True)
    brand=models.CharField(max_length=30)
    model=models.CharField(max_length=20)
    year=models.SmallIntegerField()
    gear=models.CharField(max_length=1, choices=GEAR)
    rent_per_day=models.DecimalField(
        max_digits=8, 
        decimal_places=3,
        #en düsük ucreti göster
        validators=[MinValueValidator(50)]
        )
    availability=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand}-{self.model}-{self.plate_number}"
    


class Reservation(models.Model):

    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations_customer', blank=True, null=True)  #örneegin bir numarali müsterinin yaptigi reservasyonlari görmek icin related_name'i aldik. ona ait bilgilere erismek istiyorsam
    car=models.ForeignKey(Car,on_delete=models.CASCADE,related_name="reservations_car")  #on_delete= arac yoksa o araca ait bilgiler de olmasin
    start_date=models.DateField()
    end_date=models.DateField()
   

    def __str__(self):
        return f"{self.customer}-{self.car}-{self.start_date} - {self.end_date}"
    
    # def save(self, *args, **kwargs):
    #     # Rezervasyon tarih çakışması kontrolü
    #     if Reservation.objects.filter(car=self.car, start_date__lt=self.end_date, end_date__gt=self.start_date).exists():
    #         raise ValidationError("This car is not available for the selected dates.")
        
    #     super().save(*args, **kwargs)


# def clean(self):
    # from django.utils import timezone
    # now = timezone.now()

    # if self.start_date < now:
    #     raise ValidationError("You cannot make a reservation for past dates.")
    # if self.end_date < now:
    #     raise ValidationError("You cannot make a reservation with an end date in the past.")
    
    # existing_reservations = Reservation.objects.filter(user=self.user, start_date__lt=self.end_date, end_date__gt=self.start_date)
    
    # if self.pk:
    #     existing_reservations = existing_reservations.exclude(pk=self.pk)
    
    # if existing_reservations.exists():
    #     raise ValidationError("You already have a reservation for the selected dates.")
