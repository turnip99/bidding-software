from django.urls import path

from . import views

urlpatterns = [
    path('name_input', views.name_input, name='name_input'),
    path('', views.index, name='index'),
    path('update_bids/', views.update_bids, name='update_bids'),
    path('add_bid/<int:item_id>/<str:price>/<str:name>/', views.add_bid, name='add_bid'),
]
