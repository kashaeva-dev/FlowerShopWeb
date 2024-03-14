from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.show_catalog, name='catalog'),
    path('bouquet/<int:bouquet_id>/', views.view_bouquet, name='bouquet_detail'),
    path('checkout/', views.checkout, name='catalog'),
    path('charge/', views.charge, name='charge'),
]
