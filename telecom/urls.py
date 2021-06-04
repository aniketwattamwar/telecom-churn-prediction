from django.urls import path

from . import views
from . import models

urlpatterns = [
        
        path('',views.home, name = 'home'),
        path('train',models.training, name = 'training'),
        path('predict',models.testing, name = 'testing'),
        path('eval',models.eval, name = 'eval')
        ]