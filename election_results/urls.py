from django.urls import path
from . import views


urlpatterns = [
    path('polling-unit/<int:polling_unit_id>/', views.polling_unit_result, name='polling_unit_result'),
    path('lga-summed-results/', views.lga_summed_results, name='lga_summed_results'),
    path('store-polling-unit-result/', views.store_polling_unit_result, name='store_polling_unit_result'),
    path('get-wards/', views.get_wards, name='get_wards'),
    path('get-polling-units/', views.get_polling_units, name='get_polling_units'),
    path('', views.home, name='home'),
]