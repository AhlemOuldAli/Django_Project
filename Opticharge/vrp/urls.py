from django.urls import path
from .views import *


urlpatterns = [
    path('index/', index,name='index'),
    path('export/', export,name='export'),
    path('java/', java,name='java'),
    path('show/<int:pk>/', show, name='showing'), # get this error:No such file or directory: 'data/dist_mat_[tour_1].csv'
    path('show_vrp/<int:pk>/', show, name='show_vrp'), # get this error:No such file or directory: 'data/dist_mat_[tour_1].csv'

    #path adress

    path('adress/', AddressListView.as_view(), name='address-list'),
    path('adress/<int:pk>/',AddressDetailView.as_view(), name='address-detail'),
    path('adress/create/', AddressCreateView.as_view(), name='address-create'),
    path('adress/<int:pk>/update/', AddressUpdateView.as_view(), name='address-update'),
    path('adress/<int:pk>/delete/', AddressDeleteView.as_view(), name='address-delete'),

    #path vehicle
    path('vehicule/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicule/<int:pk>/',VehicleDetailView.as_view(), name='vehicle-detail'),
    path('vehicule/create/', VehicleCreateView.as_view(), name='vehicle-create'),
    path('vehicule/<int:pk>/update/', VehicleUpdateView.as_view(), name='vehicle-update'),
    path('vehicule/<int:pk>/delete/', VehicleDeleteView.as_view(), name='vehicle-delete'),

    #path tour
    path('tour/', TourListView.as_view(), name='tour-list'),
    path('tour/<int:pk>/',TourDetailView.as_view(), name='tour-detail'),
    path('tour/create/', TourCreateView.as_view(), name='tour-create'),
    path('tour/<int:pk>/update/', TourUpdateView.as_view(), name='tour-update'),
    path('tour/<int:pk>/delete/', TourDeleteView.as_view(), name='tour-delete'),
    path('tour/<int:pk>/calculate/', tour_calculate, name='tour-calculate'),
    path('tour/<int:pk>/routes/', tour_show_routes, name='show_routes'),
    path('tour/<int:pk>/send_routes/', tour_send_routes, name='send_routes'),

    #path planification
    path('planification/', PlanificationListView.as_view(), name='planification-list'),
    path('planification/<int:pk>/',PlanificationDetailView.as_view(), name='planification-detail'),
    path('planification/create/', PlanificationCreateView.as_view(), name='planification-create'),
    path('planification/<int:pk>/update/', PlanificationUpdateView.as_view(), name='planification-update'),
    path('planification/<int:pk>/delete/', PlanificationDeleteView.as_view(), name='planification-delete'),

    #path customer
    path('customer/', CustomerListView.as_view(), name='customer-list'),
    path('customer/<int:pk>/',CustomerDetailView.as_view(), name='customer-detail'),
    path('customer/create/', CustomerCreateView.as_view(), name='customer-create'),
    path('customer/<int:pk>/update/', CustomerUpdateView.as_view(), name='customer-update'),
    path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer-delete'),

    path('file-customer/', customer_upload, name='uploaded_file_customer_url'),
    path('file-vehicle/', vehicle_upload, name='uploaded_file_vehicle_url'),

    path('customer_to_json/',customer_to_json,name='customer_to_json'),
    path('vehicle_to_json/',vehicle_to_json,name='vehicle_to_json'),
    path('planning/',vrp_planning,name='vrp_planning'),
    path('routes/',vrp_planning,name='routes'),

]