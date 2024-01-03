from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Supplier, LineItem, PurchaseOrder
from .serializers import SupplierSerializer, LineItemSerializer, PurchaseOrderSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    get=extend_schema(summary="List all purchase orders", operation_id="list_purchase_orders"),
    post=extend_schema(summary="Create a purchase order", operation_id="create_purchase_order")
)
class PurchaseOrderListCreateView(APIView):
    serializer_class = PurchaseOrderSerializer 

    def get(self, request, *args, **kwargs):
        """
            This method gets all the PurchaseOrders 
        """
        queryset = PurchaseOrder.objects.all()

        supplier_name = self.request.query_params.get('supplier_name', None)
        item_name = self.request.query_params.get('item_name', None)

        if supplier_name:
            queryset = queryset.filter(supplier__name__icontains=supplier_name)

        if item_name:
            queryset = queryset.filter(line_items__item_name__icontains=item_name)

        serializer = PurchaseOrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
            This method creates new PurchaseOrder
        """
        serializer = PurchaseOrderSerializer(data=request.data)
        
        if serializer.is_valid():
            supplier_data = serializer.validated_data.get('supplier', {})
            
            supplier_id = supplier_data.get('id')
            
            if supplier_id is not None:
                supplier_instance = Supplier.objects.filter(id=supplier_id).first()
                
                if not supplier_instance:
                    return Response({"error": "Supplier with provided id does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If no supplier id is provided, create a new supplier
                supplier_serializer = SupplierSerializer(data=supplier_data)
                if supplier_serializer.is_valid():
                    supplier_instance = supplier_serializer.save()
                else:
                    return Response({"error": "Invalid supplier data."}, status=status.HTTP_400_BAD_REQUEST)
                
            serializer.validated_data['supplier'] = supplier_instance
            
            purchase_order_instance = serializer.save()
            
            response_serializer = PurchaseOrderSerializer(purchase_order_instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response({"error": "Invalid purchase order data."}, status=status.HTTP_400_BAD_REQUEST)
    

@extend_schema_view(
    get=extend_schema(summary="Retrieve a purchase order", operation_id="retrieve_purchase_order"),
    put=extend_schema(summary="Update a purchase order", operation_id="update_purchase_order"),
    delete=extend_schema(summary="Delete a purchase order", operation_id="delete_purchase_order")
)
class PurchaseOrderDetailsView(APIView):
    serializer_class = PurchaseOrderSerializer 

    def get(self, request, id, *args, **kwargs):
        """
            This method returns the specific purchase order with given id 
        """
        try:
            purchase_order = PurchaseOrder.objects.get(pk=id)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        """
            This method updates a specific purchase order with given id 
        """
        try:
            purchase_order = PurchaseOrder.objects.get(pk=id)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseOrderSerializer(instance=purchase_order, data=request.data)
        if serializer.is_valid():
            purchase_order_instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print("this error: ",serializer.errors)
            return Response({"error": "Invalid purchase order data."}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, *args, **kwargs):
        """
            This method deletes a specific purchase order with givenid 
        """
        try:
            purchase_order = PurchaseOrder.objects.get(pk=id)
        except PurchaseOrder.DoesNotExist:
            return Response({"detail": "Purchase Order with given ID does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseOrderSerializer(purchase_order)
        serializer.destroy(serializer.data)

        return Response(status=status.HTTP_204_NO_CONTENT)