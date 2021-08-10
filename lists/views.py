from django.shortcuts import render, redirect
from lists.models import Item

def home_page(request):
    """home page"""
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/unique_id_test/')
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

def view_list(request):
    '''представление списка'''
    items = Item.objects.all()
    return render(request, 'list.html', {'items' : items})