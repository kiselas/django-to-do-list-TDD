from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
    'тест нового посетителя'

    def setUp(self):

        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
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
        time.sleep(1)

        # после загрузки должен появиться наш эллемент в таблице
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        #пробуем добавить второй эллемент
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Сделать мушку')

        # после нажатия Enter страница обновиться, ждем загрузку одну секунду
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # после загрузки должен появиться наш эллемент в таблице
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn('1: Купить перья', [row.text for row in rows])
        self.assertIn('2: Сделать мушку ', [row.text for row in rows])

        self.fail('Закончить тест!')

if __name__ == '__main__':
    unittest.main()