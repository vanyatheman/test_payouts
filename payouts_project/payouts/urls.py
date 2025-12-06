from django.urls import path
from .views import PayoutListCreateView, PayoutDetailView

urlpatterns = [
    path('', PayoutListCreateView.as_view(), name='payouts-list'),
    path('<int:pk>/', PayoutDetailView.as_view(), name='payout-detail'),
]
