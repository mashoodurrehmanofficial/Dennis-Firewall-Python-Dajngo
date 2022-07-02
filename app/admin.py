from django.contrib import admin

# Register your models here.
 

from django.contrib import admin
from .models import *
# Register your models here.
 
 

# Register your models here.
from django.db.models import ManyToOneRel, ForeignKey, OneToOneField
from django.contrib import admin
from django.apps import apps

MySpecialAdmin = lambda model: type('SubClass'+model.__name__, (admin.ModelAdmin,), {
    'list_display': [x.name for x in model._meta.fields if x.name!='id'],
    'list_select_related': [x.name for x in model._meta.fields if isinstance(x, (ManyToOneRel, ForeignKey, OneToOneField,))]
})



app = apps.get_app_config('app')

for model_name, model in app.models.items():
    admin.site.register(model, MySpecialAdmin(model))
    
 