from django.contrib import admin
from api.models import Products,Carts,Reviews,Orders

# Register your models here.

admin.site.register(Products)
admin.site.register(Carts)
admin.site.register(Reviews)
admin.site.register(Orders)
