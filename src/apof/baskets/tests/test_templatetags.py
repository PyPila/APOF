from django.test import TestCase

from apof.baskets.templatetags.get_item import get_item


class GetItemTagTestCase(TestCase):

    def test_get_item(self):
        test_dict = {
            'a': 1,
            '2': 'b'
        }
        self.assertEqual(get_item(test_dict, 'a'), 1)
        self.assertIsNone(get_item(test_dict, 'b'))
