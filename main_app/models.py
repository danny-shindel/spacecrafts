from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

# Create your models here.

class Craft(models.Model):
    # from API
    cargo_capacity = models.BigIntegerField()
    consumables = models.CharField(max_length=100)
    cost_in_credits = models.BigIntegerField()
    crew = models.IntegerField()
    length = models.DecimalField(decimal_places=10, max_digits=20)
    manufacturer = models.CharField(max_length=500)
    max_atmosphering_speed = models.IntegerField()
    model = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    passengers = models.IntegerField()
    hyperdrive_rating = models.FloatField()
    url = models.CharField(max_length=100, default=None)
    # may or may not exist
    vehicle_class = models.CharField(max_length=100)
    starship_class = models.CharField(max_length=100)
    MGLT = models.CharField(max_length=100)
    # own stuff
    sell_price = models.IntegerField()
    BUCKET = 'Bucket'
    FAIR = 'Fair'
    GOOD = 'Good'
    EXCELLENT = 'Excellent'
    LIKE_NEW = 'Like New'
    CONDITION = (
        (BUCKET, 'Bucket'),
        (FAIR, 'Fair'),
        (GOOD, 'Good'),
        (EXCELLENT, 'Excellent'),
        (LIKE_NEW, 'Like New'),
    )
    condition = models.CharField(max_length=100, choices = CONDITION, default = GOOD)
    description = models.TextField(max_length=1000)
    mileage = models.IntegerField()
    date_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self): 
        return self.name

    def get_absolute_url(self):
        return reverse('crafts')

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    craft = models.ForeignKey(Craft, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return f"{self.craft_id}"

