from django.test import TestCase, Client
from rest_framework import status
from rest_framework.reverse import reverse

from core.models import Product
from core.serializers import ProductSerializer


class TestProductList(TestCase):

    def setUp(self):
        Product.objects.create(name="Product 1", price=100, description="some info")
        Product.objects.create(name="Product 2", price=100, description="some info")
        Product.objects.create(name="Product 3", price=100, description="some info")

    def test_get_products(self):
        """
        Ensure we can get list of products
        """
        c = Client()
        # get API response
        response = c.get("http://127.0.0.1:8000/product/")
        # get data from DB
        products = Product.objects.all()
        # convert it to JSON
        serializer = ProductSerializer(products, many=True)
        # check the status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_should_allow_post_and_get(self):
        c = Client()
        response = c.put("http://127.0.0.1:8000/product/")
        assert response.status_code == 405
        response = c.delete("http://127.0.0.1:8000/product/")
        assert response.status_code == 405
        response = c.patch("http://127.0.0.1:8000/product/")
        assert response.status_code == 405

    def test_should_create_product(self):
        c = Client()
        response = c.post(
            "http://127.0.0.1:8000/product/",
            data={
                "name": "test product 1",
                "price": 1200,
                "description": "some info",
            }
        )
        assert response.status_code == 201


class TestProductModel(TestCase):
    def test_too_long_name_should_fail(self):
        c = Client()
        text = "a" * 256
        response = c.post(
            "http://127.0.0.1:8000/product/",
            data={
                "name": text,
                "price": 1200,
                "description": "some info"
            }
        )
        assert response.status_code == 400

    def test_have_not_required_fields_should_fail(self):
        # required fields - name, description, price
        c = Client()
        response = c.post(
            "http://127.0.0.1:8000/product/",
            data={
                "name": "product 1",
                "description": "some info"
            }
        )
        assert response.status_code == 400

    def test_price_field_more8_digits_or_2decimal_places_should_fail(self):
        c = Client()
        response = c.post(
            "http://127.0.0.1:8000/product/",
            data={
                "name": "test product",
                "price": 120000000,
                "description": "some info"
            }
        )
        assert response.status_code == 400
        response = c.post(
            "http://127.0.0.1:8000/product/",
            data={
                "name": "test product",
                "price": 120.505,
                "description": "some info"
            }
        )
        assert response.status_code == 400

    def test_wrong_type_field_should_fail(self):
        c = Client()
        response = c.post(
            "http://127.0.0.1:8000/product/",
            data={
                "name": "test product",
                "price": "something",
                "description": "some info"
            }
        )
        assert response.status_code == 400


class TestProductDetail(TestCase):

    def setUp(self):
        Product.objects.create(name="Product 1", price=100, description="some info")
        Product.objects.create(name="Product 2", price=100, description="some info")
        Product.objects.create(name="Product 3", price=100, description="some info")

    # def test_update_put_post(self):
        """
        Check if we can update post
        """
        # c = Client()
        # product = Product.objects.get(id=1)
        # data = {'name': 'Product 1 modified', 'price': 200, 'description': 'info modified'}
        # response = c.put("http://127.0.0.1:8000/product/2", data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_allow_put_delete_get(self):
        c = Client()
        product = Product.objects.get(id=1)
        response = c.get("http://127.0.0.1:8000/product/1")
        assert response.status_code == 200
        response = c.post("http://127.0.0.1:8000/product/1")
        assert response.status_code == 405    # not allowed
        response = c.delete("http://127.0.0.1:8000/product/1")
        assert response.status_code == 204
        response = c.patch("http://127.0.0.1:8000/product/1")
        assert response.status_code == 405    # not allowed


