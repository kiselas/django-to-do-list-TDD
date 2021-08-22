from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    '''тест валидации элемента списка'''

    def test_cannot_add_empty_list_items(self):
        """тест: нельзя добавлять пустые элементы списка"""
        # отправляем пустое поле.
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        # проверяем появилась ли ошибка
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # теперь отправляем поле с текстом
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # после чего опят пробуем отправить пустой элемент
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # снова появляется ошибка
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # теперь отправляем элемент с текстом и проверяем, что оба элемента на месте
        # И она может его исправить, заполнив поле неким текстом
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

