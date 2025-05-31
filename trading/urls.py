from django.urls import path
from . import views

app_name = 'trading'

urlpatterns = [
    path('', views.trading_view, name='trading'),
]