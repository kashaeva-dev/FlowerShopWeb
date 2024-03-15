from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.show_catalog, name='catalog'),
    path('bouquet/<int:bouquet_id>/', views.view_bouquet, name='bouquet_detail'),
    path('bouquets/ajax/', views.bouquet_list_ajax, name='bouquet_list_ajax'),
    path('consultation/', views.consultation, name='consultation'),
    path('consulting_request/', views.consulting_request, name='consulting_request'),
    path('checkout/', views.checkout, name='checkout'),
    path('charge/', views.charge, name='charge'),
]
