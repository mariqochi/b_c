from django.db import models
#from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=12, null=True)
    email = models.CharField(max_length=25, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.username
    

# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=50, null=True)
#     last_name = models.CharField(max_length=50, null=True)
#     phone = models.CharField(max_length=12, null=True)
#     email = models.CharField(max_length=25, null=True)
#     date_created = models.DateTimeField(auto_now_add=True, null=True)
#     date_updated = models.DateTimeField(auto_now=True, null=True)
#     profile_pic = models.ImageField(default="basicUser.jpg", null=True, blank=True)

#     def __str__(self):
        # return f"{self.first_name} {self.last_name}"



class Type(models.Model):
    name=models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    


class Car(models.Model):
    make = models.CharField(max_length=20, null=True, blank=True)
    model = models.CharField(max_length=20, null=True, blank=True)
    manufacturing_year = models.IntegerField()
    fuel_consumption = models.DecimalField(max_digits=4, decimal_places=2)
    color = models.CharField(max_length=20, null=True, blank=True)
    num_seats = models.IntegerField()
    car_type = models.ForeignKey('Type', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    picture = models.ImageField(upload_to='images/', null=True, blank=True)
    #car_type = models.ForeignKey('CarType', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.make} {self.model}"

class CarAvailability(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"Availability for {self.car} on {self.date}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    loc_from = models.CharField(max_length=50, default="")
    loc_to = models.CharField(max_length=50, default="")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.user.username} - {self.car}"

    def save(self, *args, **kwargs):
        # Calculate total cost based on the number of days and car's price
        if self.start_date and self.end_date and self.car.price:
            self.total_cost = (self.end_date - self.start_date).days * self.car.price
        super().save(*args, **kwargs)

    def clean(self):
        # Check if the car is available for the selected dates
        if self.start_date and self.end_date:
            car_availabilities = CarAvailability.objects.filter(
                car=self.car,
                date__range=[self.start_date, self.end_date]
            )
            if car_availabilities.count() != (self.end_date - self.start_date).days + 1:
                raise ValidationError('Car is not available for the selected dates.')

    
    # class Order(models.Model) :
    # order_id = models.AutoField(primary_key=True)
    # name = models.CharField(max_length=90,default="")
    # email = models.CharField(max_length=50,default="")
    # phone = models.CharField(max_length=20,default="")
    # address = models.CharField(max_length=500,default="")
    # city = models.CharField(max_length=50,default="")
    # cars = models.CharField(max_length=50,default="")
    # days_for_rent = models.IntegerField(default=0)
    # date = models.CharField(max_length=50,default="")
    # loc_from = models.CharField(max_length=50,default="")
    # loc_to = models.CharField(max_length=50,default="")
    
    # def __str__(self):
    #     return self.name

# class Contact(models.Model):
#     message = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=150,default="")
#     email = models.CharField(max_length=150,default="")
#     phone_number = models.CharField(max_length=15,default="")
#     message = models.TextField(max_length=500,default="")

    # def __str__(self) :
    #     return self.name
    
    # class Messages(models.Model):
    #     user = models.ForeignKey(User, on_delete=models.CASCADE)
    #     room = models.ForeignKey(Room, on_delete=models.CASCADE)
    #     body = models.TextField()
    #     updated = models.TextField()
    #     updated = models.DateTimeField(auto_row=True)
    #     created = models.DataTimeField(auto_row_add=True)
        
    #     def __str__(self):
    #         return self.body (0:50)