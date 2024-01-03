from rest_framework import serializers
from .models import Supplier, LineItem, PurchaseOrder

class SupplierSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    email = serializers.EmailField()

    class Meta:
        model = Supplier
        fields = '__all__'

class LineItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = LineItem
        fields = '__all__'
        read_only_fields = ('line_total', 'purchase_order', 'id',)

    def get_line_total(self, obj: LineItem) -> float:
        return obj.line_total


class PurchaseOrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    supplier = SupplierSerializer()
    line_items = LineItemSerializer(many=True)
    total_amount = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()
    total_tax = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        read_only_fields = ('order_number', 'order_time', 'total_amount', 'total_quantity', 'total_tax', 'id',)


    def get_total_amount(self, obj: PurchaseOrder)-> float:
        return obj.total_amount

    def get_total_quantity(self, obj: PurchaseOrder) -> int:
        return obj.total_quantity

    def get_total_tax(self, obj: PurchaseOrder) -> float:
        return obj.total_tax


    def validate_line_items(self, value):
        """
            This method validates if the line items in request is a list and not empty
        """
        if type(value)==list and len(value)>0 :
            return value
        else:
            raise serializers.ValidationError("Line Items must not be empty")
            

    def create(self, validated_data) -> PurchaseOrder:
        """
            This method creates the Purchase order along with its line_itens
        """
        line_items_data = validated_data.pop('line_items', [])

        purchase_order = PurchaseOrder.objects.create(**validated_data)

        for line_item_data in line_items_data:
            line_item_data['purchase_order'] = purchase_order
            LineItem.objects.create(**line_item_data)

        return purchase_order

    def update(self, instance, validated_data) -> PurchaseOrder:
        """
            This method updates the specific PurchaseOrder
        """
        supplier_data = validated_data.get('supplier', {})
        supplier_instance, created = Supplier.objects.get_or_create(pk=supplier_data.get('id'), defaults=supplier_data)

        if not created:
            supplier_instance.name = supplier_data.get('name', supplier_instance.name)
            supplier_instance.email = supplier_data.get('email', supplier_instance.email)

        instance.supplier = supplier_instance

        line_items_data = validated_data.get('line_items', [])
        existing_line_item_ids = [item.id for item in instance.line_items.all()]

        for line_item_data in line_items_data:
            line_item_id = line_item_data.get('id', None)

            if line_item_id is not None:
                LineItem.objects.filter(id=line_item_id, purchase_order=instance).update(**line_item_data)
            else:
                new_line_item_instance = LineItem.objects.create(purchase_order=instance, **line_item_data)
                line_item_data['id'] = new_line_item_instance.id

        LineItem.objects.filter(id__in=existing_line_item_ids).exclude(id__in=[item['id'] for item in line_items_data]).delete()

        instance.save()
        return instance

    def delete(self, instance) -> None:
        """
            This method deletes the PurchaseOrder and the associated line_items
        """
        LineItem.objects.filter(purchase_order=instance).delete()
        instance.delete()

        return

    def destroy(self, validated_data) -> None:
        """
            This method is a wrapper around the delete method and validates if the deletion is possible
        """
        instance_id = validated_data.get('id')
        if instance_id is not None:
            try:
                instance = PurchaseOrder.objects.get(id=instance_id)
                self.delete(instance)
            except PurchaseOrder.DoesNotExist:
                raise serializers.ValidationError("Purchase Order with given ID does not exist")
        else:
            raise serializers.ValidationError("ID is required for deleting a Purchase Order")
        
        return