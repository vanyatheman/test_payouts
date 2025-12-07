from django.urls import path

from .views import PayoutDetailView, PayoutListCreateView

urlpatterns = [
    path("", PayoutListCreateView.as_view(), name="payouts-list"),
    path("<int:pk>/", PayoutDetailView.as_view(), name="payout-detail"),
]
