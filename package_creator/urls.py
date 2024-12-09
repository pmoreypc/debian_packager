from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_package, name='create_package'),
]
