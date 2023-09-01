from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.home, name="home"),
    path("upload_excel/", views.upload_excel, name="upload_excel"),
]
