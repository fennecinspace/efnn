from django.contrib import admin
from django.urls import path, include
from app.views import *

urlpatterns = [
    path('', Home),
    path('run/<slug:sample_name>', Run),
    path('upload/', Upload),
]
