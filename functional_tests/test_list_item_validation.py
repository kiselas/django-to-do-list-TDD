from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    '''тест валидации элемента списка'''
    @skip
    def test_cannot_add_empty_list_items(self):
        """тест: нельзя добавлять пустые элементы списка"""

