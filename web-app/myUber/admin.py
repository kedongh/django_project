from django.contrib import admin
from .models import account, driver, ride
# Register your models here.
admin.site.register(account)
admin.site.register(driver)
admin.site.register(ride)