
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *  
 
urlpatterns = [       
    
    path('login/', loginRouter, name='loginRouter'),     
    path('logout/', logoutRouter, name='logoutRouter'),
    path('', dashboard, name='dashboard'),
    path('dashboard/', dashboard, name='dashboard'),
    path('changeAccessStatus/', changeAccessStatus, name='changeAccessStatus'),
    path('getUUID/', getUUID, name='getUUID'),
    path('getWaitingList/', getWaitingList, name='getWaitingList'),
    
    
        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

