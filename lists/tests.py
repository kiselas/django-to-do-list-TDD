from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from lists.models import Item
from django.http import HttpRequest


class HomePageTest(TestCase):
    """тест домашней страницы"""
    def test_root_url_resolves_to_home_page_view(self):
        """тест: корневой url преобразуется в представление домашней страницы"""
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """тест: домашняя стр. возвращает правильный url"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        """тест: можем сохранить ПОСТ запрос"""
        response = self.client.post('/', data={'item_text' : 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirect_after_POST(self):
        '''тест:  переадресация после ПОСТ запроса'''
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_displays_all_list_elements(self):
        '''тест: отображаются все элементы списка'''
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response = self.client.get('/')

        self.assertIn('item 1', response.content.decode())
        self.assertIn('item 2', response.content.decode())



    def test_only_saves_items_when_necessary(self):
        '''тест: сохраняет элементы, только когда нужно'''
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        """тест сохранения и получения элемепнтов списка"""
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')