from django.shortcuts import render
from django.http import JsonResponse
from wagtail import hooks
from django.urls import path
from wagtail.models import Page
from .models import Menu, ItemMenu
from wagtail.admin.menu import MenuItem



def structure_tree_page(pages, is_root: bool = False):
    structure = {}
    
    for page in pages:
        structure[page.title] = {
            'id': page.id,
            'title': page.title,
            'children': structure_tree_page(page.get_children())
        }
        if is_root:
            return structure

    return structure
    
def custom_admin_view(request):
    pages = Page.objects.all()
    list_menu = Menu.objects.exclude(name=None)

    context = {
        'all_pages': structure_tree_page(pages[0].get_children(), True),
        'all_menu': list_menu
    }

    return render(request, 'site_settings/site_settings_menu.html', context)

def create_data_menu(data_form):
    dict_menu = {
        'name': data_form.get('name-menu'),
        'slug': data_form.get('slug-id'),
        'items': {}
    }

    page = Page.objects.all()

    for i in range(len(data_form.getlist('id'))):
        dict_menu['items'][data_form.getlist('id')[i]] = {
            'name': data_form.getlist('name-link')[i],
            'id_page': page.get(id=data_form.getlist('id-page')[i]),
            'parent': data_form.getlist('parent')[i],
            'order': data_form.getlist('order-item')[i],
            'parant_id': None
        }
        
    return dict_menu
    

def create_menu(slug:str, name:str = None):
    menu = Menu.objects.create(
        name=name,
        slug=slug
    )
    return menu

def edit_menu(menu, name):
    menu.name = name
    menu.save()

def create_item_menu(data_item, slug):
    item = ItemMenu.objects.create(
        name=data_item['name'],
        page=data_item['id_page'],
        order=data_item['order']
    )
    item.sub_menu = create_menu(slug + '-' + str(item.id))
    item.save()
    return item

def edit_item_menu(item, data_item):
    item.name = data_item['name']
    item.order = data_item['order']
    item.save()

def get_item_menu(items, slug):
    data = {}
    try:
        for item in items:
            data[item.id] = {
                'name': item.name,
                'id_page': item.page.id,
                'order': item.order,
                'parent': slug,
                'sub_menu': {
                    'slug': item.sub_menu.slug,
                    'items': get_item_menu(item.sub_menu.items.all(), item.sub_menu.slug)
                }
            }
    except:
        pass

    return data

def get_parent_id(data, parent):
    print(data)
    print(parent)
    parent_id = None
    for item in data:
        if item == parent:
            parent_id = data[item]['parant_id']
            break
    print(parent_id)
    return parent_id

def edit_menu(request):
    if request.method == "POST":
        '''Сохранение данных меню, которые пришли из формы 
        и отправка их в базу данных. Также отправка обратно на 
        фронтент JSON ответа в виде дерева нового меню'''

        data_menu = create_data_menu(request.POST)
        menu = create_menu(data_menu['slug'], data_menu['name'])

        for item in data_menu['items']:
            item_menu = create_item_menu(data_menu['items'][item], data_menu['slug'])
            data_menu['items'][item]['parant_id'] = data_menu['slug'] + '-' + str(item_menu.id)

            if data_menu['items'][item]['parent'] == 'root':
                menu.items.add(item_menu)
                menu.save()
            else:
                sub_menu = Menu.objects.get(slug=get_parent_id(data_menu['items'], data_menu['items'][item]['parent']))
                sub_menu.items.add(item_menu)
                sub_menu.save()
        
        return JsonResponse({'status': 'ok'})
    
    elif request.method == "GET":
        '''Отправка на фронтент JSON ответа в виде дерева меню'''
        menu = Menu.objects.get(slug=request.GET.get('slug'))
        items = menu.items.all()
        data = {
            'name': menu.name,
            'slug': menu.slug,
            'items': get_item_menu(items, menu.slug)
        }
        return JsonResponse(data)
               
    return JsonResponse({'status': 'error'})

# Добавьте URL для вашей кастомной страницы
@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        path('settings-menu/', custom_admin_view, name='custom_admin_page'),
        path('settings-menu/edit-menu/', edit_menu, name='edit_menu_page'),
    ]

@hooks.register('register_settings_menu_item')
def register_custom_menu_item():
    return MenuItem('Настройка меню сайта', '/admin/settings-menu/', classnames='icon icon-menu', icon_name='cog', order=10000)
