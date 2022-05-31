from django.contrib import admin
from numpy import real

from .models import Locate_Info, full_data_model, realty_data

# Register your models here.


admin.site.register(Locate_Info)
admin.site.register(full_data_model)
admin.site.register(realty_data)