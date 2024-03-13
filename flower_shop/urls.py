from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('bouquet/<int:bouquet_id>/', views.view_bouquet, name='bouquet_detail'),
]
