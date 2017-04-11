from datetime import time

from django.core.files import File
from django.test import TestCase
from mock import patch, MagicMock

from apof.restaurants.models import OpeningHours, PhoneNumber, Restaurant

file_mock = MagicMock(spec=File, name='FileMock')
file_mock.name = 'test1.jpg'


class RestaurantTestCase(TestCase):

    @patch('django.core.files.storage.default_storage._wrapped')
    def setUp(self, mocked_storage):
        self.restaurant = Restaurant.objects.create(
            name='Test',
            logo=file_mock
        )

    def test_string_representation(self):
        self.assertEqual(
            str(self.restaurant),
            'Test'
        )

    def test_repr(self):
        self.assertEqual(
            repr(self.restaurant),
            'Restaurant(Name: Test)'
        )

    def test_get_phone_numbers(self):
        number1 = '012345678'
        number2 = '876543210'
        expected_result = [number1, number2]

        PhoneNumber.objects.bulk_create([
            PhoneNumber(restaurant=self.restaurant, number=number1),
            PhoneNumber(restaurant=self.restaurant, number=number2)
        ])
        result = self.restaurant.get_phone_numbers()
        self.assertEqual(expected_result, result)


class OpeningHoursTestCase(TestCase):

    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Test',
        )
        self.opening_hours = OpeningHours.objects.create(
            restaurant=self.restaurant,
            day=0,
            opening_from=time(10),
            opening_to=time(20, 30)
        )

    def test_string_representation(self):
        self.assertEqual(str(self.opening_hours), 'Test | Monday | 10:00 | 20:30')

    def test_repr(self):
        self.assertEqual(
            repr(self.opening_hours),
            'OpeningHours(Restaurant: Test, Day: 0)'
        )


class PhoneNumberTestCase(TestCase):

    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Test',
        )
        self.phone_number = PhoneNumber.objects.create(
            restaurant=self.restaurant,
            number='012345678'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.phone_number), 'Test | 012345678')

    def test_repr(self):
        self.assertEqual(
            repr(self.phone_number),
            'PhoneNumber(Restaurant: Test, Number: 012345678)'
        )
