from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
class Products(models.Model):
    name=models.CharField(max_length=100)
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    image=models.ImageField(null=True,upload_to="images")

    @property
    def avg_rating(self):
        ratings=self.reviews_set.all().values_list("rating",flat=True)
        if ratings:
            return sum(ratings)/len(ratings)
        else:
            return 0

    def review_count(self):
        ratings=self.reviews_set.all().values_list("rating",flat=True)
        if ratings:
            return len(ratings)
        else:
            return 0




    def __str__(self):
        return self.name
#orm for creating a resource
#modelname.object.create(field1=value1,field2=value2....)
#Products.objects.create(name="vivo123",price=23000,description="mobile",category="electronics")

#orm query for fetching all records
#qs=modelname.objects.all()

#orm for filtering queries
#qs=modelname.objects.filter(category="electronics")

#modelname.objects.all().exclude(description="mobile")
#qs=Products.objects.all().exclude(description="mobile")

#qs=modelname.objects.get(id=1)
#qs=Products.objects.get(id=1)

#price>25000
#qs=Products.objects.filter(price__gt=25000)
#products in range of 20000 to 30000?
#filter all category

#type(qs)---- Queryset                              !!!!!!!!!!!!!!!!!!!


class Carts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    options=(
        ("order-placed","order-placed"),
        ("in-cart","in-cart"),       
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=200,choices=options,default="in-cart")

class Reviews(models.Model):
    products=models.ForeignKey(Products,on_delete=models.CASCADE)
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.CharField(max_length=200)

    def __str__(self):
        return self.comment


class Orders(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    options=(
        ("order-placed","order-placed"),
        ("despathed","despatched"),
        ("in-transit","in-transit"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=200,choices=options,default="order-placed")
    date=models.DateField(auto_now_add=True)
    address=models.CharField(max_length=250)
    phone=models.CharField(max_length=20)
    