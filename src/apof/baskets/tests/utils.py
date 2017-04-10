from django.contrib.auth.models import User
from django.core.files import File
from mock import patch, MagicMock

from apof.baskets.admin import OrderAdmin
from apof.baskets.models import Order, Basket
from apof.menus.models import Size, Meal, Menu, Topping, Ingredient, Price
from apof.restaurants.models import Restaurant


class OrderTestMixin(object):

    @patch('django.core.files.storage.default_storage._wrapped')
    def setUp(self, mocked_storage):
        file_mock = MagicMock(spec=File, name='FileMock')
        file_mock.name = 'test1.jpg'
        restaurant = Restaurant.objects.create(name='test restaurant2', logo=file_mock)
        menu = Menu.objects.create(restaurant=restaurant)
        size = Size.objects.create(menu=menu, value=15, value_unit='cm')
        test_meal = Meal.objects.create(menu=menu, name='test_meal')
        test1_topping = Topping.objects.create(
            menu=menu,
            ingredient=Ingredient.objects.create(
                name='test1_ingredient'
            )
        )
        test2_topping = Topping.objects.create(
            menu=menu,
            ingredient=Ingredient.objects.create(
                name='test2_ingredient'
            )
        )
        Price.objects.bulk_create([
            Price(value=22.99, size=size, content_object=test_meal),
            Price(value=2.5, size=size, content_object=test1_topping),
            Price(value=1.25, size=size, content_object=test2_topping)
        ])
        self.order = Order.objects.create(
            basket=Basket.objects.create(owner=User.objects.get(username='christopher')),
            meal=test_meal,
            size=size
        )
        self.order.toppings.set([test1_topping, test2_topping])
        self.data_mock = MagicMock()
        self.test_order = OrderAdmin(self.data_mock, self.data_mock)