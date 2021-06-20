from django.urls import path

from . import views

urlpatterns = [
    path('', views.name_input, name='name_input'),
    path('bidding/', views.bidding, name='bidding'),
    path('bidding/update_bids/', views.update_bids, name='update_bids'),
    path('bidding/add_bid/<int:item_id>/<str:price>/<str:name>/', views.add_bid, name='add_bid'),
]
