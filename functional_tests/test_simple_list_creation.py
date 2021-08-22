from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):
    """тест нового посетителя"""

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        inputbox.send_keys('Купить перья')

        # после нажатия Enter страница обновиться, ждем загрузку одну секунду
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Купить перья")

        # пробуем добавить второй эллемент
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Сделать мушку')

        # после нажатия Enter страница обновиться, ждем загрузку одну секунду
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Купить перья")
        self.wait_for_row_in_list_table("2: Сделать мушку")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        '''тест: несколько пользователей могут начать свои списки по разным ссылкам'''
        # эдит начинает свой список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить павлиньи перья')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # она замечает, что у ее списка уникальный адрес
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # теперь новый пользователь приходит на сайт

        ## Мы используем новый сеанс браузера, тем самым обеспечивая, чтобы никакая
        ## информация от Эдит не прошла через данные cookie и пр.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Фрэнсис посещает домашнюю страницу. Нет никаких признаков списка Эдит
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить перья', page_text)
        self.assertNotIn('Сделать мушку', page_text)

        # Фрэнсис начинает новый список, вводя новый элемент
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить молоко')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Фрэнсис получает уникальный URL-адрес
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Опять-таки, нет ни следа от списка Эдит
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)

class LayoutAndStylingTest(FunctionalTest):
    '''тест макета и стилевого оформления'''

    def test_layout_and_styling(self):
        """тест макета и стилевого оформления"""
        # пользователь открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # он замечает, что поле ввода аккуратно центрировано
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512,
            delta=10
        )
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

