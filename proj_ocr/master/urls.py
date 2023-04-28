from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="master_index"),
    path("process", views.fileProcessing, name="master_file_processing"),
]