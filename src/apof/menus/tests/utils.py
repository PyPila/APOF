from apof.menus.models import (
    Category,
    Ingredient,
    Meal,
    Menu,
    Price,
    Size,
    Topping
)
from apof.restaurants.models import Restaurant


class MenusTestMixin(object):
    def setUp(self):
        self.category = Category(name='test category')
        self.ingredient = Ingredient(name='test ingredient')
        self.menu = Menu(restaurant=Restaurant(name='test restaurant'))
        self.meal = Meal(menu=self.menu, name='test meal')
        self.size = Size(menu=self.menu)
        self.price = Price(value='24.99', size=self.size, content_object=self.meal)
        self.topping = Topping(menu=self.menu, ingredient=self.ingredient)
