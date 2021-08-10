from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from lists.models import Item, List
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


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        """тест сохранения и получения элемепнтов списка"""
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):
    '''тест представления списка'''

    def test_displays_all_items(self):
        '''тест: отображаются все элементы списка'''
        list_ = List.objects.create()

        Item.objects.create(text='Item 1', list = list_)
        Item.objects.create(text='Item 2', list = list_)

        response = self.client.get('/lists/unique_id_test/')

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')

    def test_uses_list_template(self):
        '''тест: используется шаблон списка'''

        response = self.client.get('/lists/unique_id_test/')
        self.assertTemplateUsed(response, 'list.html')

class NewListTest(TestCase):
    '''тест нового списка'''

    def test_can_save_a_POST_request(self):
        """тест: можем сохранить ПОСТ запрос"""
        response = self.client.post('/lists/new', data={'item_text' : 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirect_after_POST(self):
        '''тест:  переадресация после ПОСТ запроса'''
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/unique_id_test/')
