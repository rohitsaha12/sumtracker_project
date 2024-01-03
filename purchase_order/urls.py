from django.urls import path
from .views import PurchaseOrderListCreateView, PurchaseOrderDetailsView

urlpatterns = [
    path('purchase/orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('purchase/orders/<int:id>/', PurchaseOrderDetailsView.as_view(), name='purchase-order-details'),
]
