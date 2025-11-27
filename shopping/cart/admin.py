from django.contrib import admin
from .models import product,Contact,orders,updateorders

# Register your models here.

admin.site.register(product)
admin.site.register(Contact)
admin.site.register(orders)
admin.site.register(updateorders)