from django.urls import path

from . import views

app_name = "digit_painter"
urlpatterns = [
    path('', views.paint, name='paint'),
    path('submit/', views.submit, name='submit')
]
