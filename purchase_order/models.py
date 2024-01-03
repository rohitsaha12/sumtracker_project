from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

class LineItem(models.Model):
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price_without_tax = models.DecimalField(max_digits=10, decimal_places=2)
    tax_name = models.CharField(max_length=255)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_order = models.ForeignKey('PurchaseOrder', on_delete=models.CASCADE, related_name="line_items")

    @property
    def line_total(self):
        return self.quantity * (self.price_without_tax + self.tax_amount)



class PurchaseOrder(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, related_name="orders")
    order_time = models.DateTimeField(auto_now_add=True)
    order_number = models.PositiveIntegerField(default=0)

    @property
    def total_quantity(self):
        total_quantity = 0
        for line_item in self.line_items.all():
            total_quantity += line_item.quantity
        return total_quantity

    @property
    def total_amount(self):
        total_amount = 0
        for line_item in self.line_items.all():
            total_amount += line_item.line_total
        return total_amount
    
    @property
    def total_tax(self):
        total_tax = 0
        for line_item in self.line_items.all():
            total_tax += line_item.tax_amount
        return total_tax

    def save(self, *args, **kwargs):
        """
            Added fuctionality to increment order number wheneven new PurchaseOrder is created
        """
        if not self.order_number:
            last_order = PurchaseOrder.objects.order_by('-order_number').first()
            if last_order:
                self.order_number = last_order.order_number + 1
            else:
                self.order_number = 1

        super().save(*args, **kwargs)
    