import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from purchase_order.models import PurchaseOrder, Supplier, LineItem
from django.urls import reverse
from urllib.parse import urlencode


class PurchaseOrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def create_sample_data(self):
        """
            This method creates sample data for tests
        """
        supplier = Supplier.objects.create(name="Supplier 1", email="supplier@email.com")

        purchase_order = PurchaseOrder.objects.create(
            supplier=supplier,
        )

        line_item = LineItem.objects.create(
            item_name="Test Product",
            quantity=1,
            price_without_tax=10.00,
            tax_name="GST 5%",
            tax_amount=0.50,
            purchase_order=purchase_order
        )

    def test_create_purchase_order_with_null_supplier_id(self):
        """
            This test create a new purchase order,
            We donot supply the supplier_id here,
            Thus this creates a new supplier as well
            The test checks for new purchase order created and new supplier added
        """
        self.create_sample_data()
        data = {
            "supplier": {
                "id": None,
                "name": "New Supplier",
                "email": "new_supplier@email.com"
            },
            "line_items": [
                {
                    "item_name": "New Product",
                    "quantity": 2,
                    "price_without_tax": "15.00",
                    "tax_name": "GST 5%",
                    "tax_amount": "0.75"
                }
            ]
        }

        response = self.client.post(reverse('purchase-order-list-create'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(PurchaseOrder.objects.all()),2)
        self.assertEqual(len(Supplier.objects.all()),2)

    def test_create_purchase_order_with_supplier_id(self):
        """
            This test creates a purchase order for a particular supplier.
            This test checks for new puchase order created and no new supplier added
        """
        self.create_sample_data()
        supplier = Supplier.objects.first()
        data = {
            "supplier": {
                "id": supplier.id,
                "name": supplier.name,
                "email": supplier.email
            },
            "line_items": [
                {
                    "item_name": "New Product 5",
                    "quantity": 2,
                    "price_without_tax": "15.00",
                    "tax_name": "GST 5%",
                    "tax_amount": "0.75"
                }
            ]
        }

        response = self.client.post(reverse('purchase-order-list-create'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(PurchaseOrder.objects.all()),2)
        self.assertEqual(len(Supplier.objects.all()),1)

    def test_get_all_purchase_orders(self):
        """
            This test checks if all the PurchaseOrder created are returned
        """
        self.create_sample_data()

        response = self.client.get(reverse('purchase-order-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_all_purchase_orders_with_supplier_filter(self):
        """
            This test checks if appropriate PurchaseOrder(s) are returned with supplier filter
        """
        self.create_sample_data()

        query_params = {'supplier_name': 'Supplier 1'}
        response = self.client.get(reverse('purchase-order-list-create')+ '?' + urlencode(query_params))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_all_purchase_orders_with_supplier_filter_with_wrong_input(self):
        """
            This test checks if appropriate PurchaseOrder(s) are returned with supplier filter
        """
        self.create_sample_data()

        query_params = {'supplier_name': 'Supplier 999'}
        response = self.client.get(reverse('purchase-order-list-create')+ '?' + urlencode(query_params))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_all_purchase_orders_with_item_name_filter(self):
        """
            This test checks if appropriate PurchaseOrder(s) are returned with item filter
        """
        self.create_sample_data()

        query_params = {'item_name': 'Test Product'}
        response = self.client.get(reverse('purchase-order-list-create')+ '?' + urlencode(query_params))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 

    def test_get_all_purchase_orders_with_item_name_filter_with_wrong_input(self):
        """
            This test checks if appropriate PurchaseOrder(s) are returned with item filter
        """
        self.create_sample_data()

        query_params = {'item_name': 'No Product '}
        response = self.client.get(reverse('purchase-order-list-create')+ '?' + urlencode(query_params))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0) 

    def test_get_single_purchase_order(self):
        """
            This test checks if the single purchase order is returned given the purchase_order_id
        """
        self.create_sample_data()

        purchase_order_id = PurchaseOrder.objects.first().id
        response = self.client.get(reverse('purchase-order-details', args=[purchase_order_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_single_purchase_order_with_wrong_input(self):
        """
            This test checks 404 is returned with wrong purchase_order_id
        """
        self.create_sample_data()

        purchase_order_id = 99999
        response = self.client.get(reverse('purchase-order-details', args=[purchase_order_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_purchase_order(self):
        """
            This test checks the update functionality of the specific purchase order
        """
        self.create_sample_data()

        old_response = self.client.get(reverse('purchase-order-list-create'))

        purchase_order_id = PurchaseOrder.objects.first().id
        data = {
            "id": purchase_order_id,
            "supplier": {
                "id": 1,  # Existing supplier ID
                "name": "Updated Supplier",
                "email": "updated_supplier@email.com"
            },
            "line_items": [
                {
                    "id": 1,  # Existing line item ID
                    "item_name": "Updated Product",
                    "quantity": 3,
                    "price_without_tax": "20.00",
                    "tax_name": "GST 10%",
                    "tax_amount": "2.00"
                },
                {
                    "item_name": "New Product",
                    "quantity": 2,
                    "price_without_tax": "15.00",
                    "tax_name": "GST 5%",
                    "tax_amount": "0.75"
                }
            ]
        }

        response = self.client.put(reverse('purchase-order-details', args=[purchase_order_id]), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['supplier']['name'],"Updated Supplier")
        self.assertEqual(len(response.data['line_items']),2)
        self.assertNotEqual(old_response.data[0]['total_amount'], response.data['total_amount'])


    def test_delete_purchase_order(self):
        """
            This test checks if the given purchase order with the id is deleted 
        """
        self.create_sample_data()

        purchase_order_id = PurchaseOrder.objects.first().id
        response = self.client.delete(reverse('purchase-order-details', args=[purchase_order_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(PurchaseOrder.objects.all()),0)

    def test_delete_purchase_order_with_wrong_input(self):
        """
            This test checks if 404 returned with the wrong purchase order id
        """
        self.create_sample_data()

        purchase_order_id = 999999
        response = self.client.delete(reverse('purchase-order-details', args=[purchase_order_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)