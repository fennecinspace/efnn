from django.contrib import admin
from django.urls import path, include
from app.views import Home

urlpatterns = [
    path('', Home),
]
