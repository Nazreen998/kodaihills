from django.contrib import admin

# Register your models here.
from .models import Data,Cart,Order,Profile

admin.site.register(Data)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Profile)