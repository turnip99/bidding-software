from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),),
    path('', views.NameInputView.as_view(), name='name_input'),
    path('no_active_auction_error/', views.NoActiveAuctionErrorView.as_view(), name='no_active_auction_error'),
    path('bidding/', views.BiddingView.as_view(), name='bidding'),
    path('bidding/update_bids/', views.update_bids, name='update_bids'),
    path('bidding/add_bid/<int:item_id>/<str:price>/<str:name>/<str:phone_number>/', views.add_bid, name='add_bid'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('admin_panel/', views.AdminPanelView.as_view(), name='admin_panel'),
    path('admin_panel/message_generator/', views.MessageGeneratorView.as_view(), name='message_generator'),
]
