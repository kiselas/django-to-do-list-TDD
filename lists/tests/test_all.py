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

    def test_uses_list_template(self):
        '''тест: используется шаблон списка'''
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        '''тест: отображаются элементы только для этого списка'''
        correct_list = List.objects.create()
        Item.objects.create(text='Item 1', list = correct_list)
        Item.objects.create(text='Item 2', list = correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='другой элемент 1 списка', list=other_list)
        Item.objects.create(text='другой элемент 2 списка', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')
        self.assertNotContains(response, 'другой элемент 1 списка')
        self.assertNotContains(response, 'другой элемент 2 списка')

class NewListTest(TestCase):
    """тест нового списка"""

    def test_passes_correct_list_to_template(self):
        """тест: передается правильный шаблон списка"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """тест: можем сохранить ПОСТ запрос в существующий список"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text' : 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirect_to_list_view(self):
        """тест: переадресуется в представление списка"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new list item in existing list'}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
