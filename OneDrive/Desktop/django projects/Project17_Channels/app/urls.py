from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('<str:group>/', views.index, name="index"),  # Passing the function directly without calling it
    path('<str:group>/<str:chat>/', views.chat),

]
