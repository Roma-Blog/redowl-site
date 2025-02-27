from django.shortcuts import render
from django.http import JsonResponse
from wagtail import hooks
from django.urls import path
from wagtail.admin.menu import MenuItem
from wagtail.models import Page



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
    

# Определите представление для вашей кастомной страницы
def custom_admin_view(request):
    pages = Page.objects.all()

    context = {
        'all_pages': structure_tree_page(pages[0].get_children(), True)
    }

    return render(request, 'site_settings/site_settings_menu.html', context)

def edit_menu(request):
    if request.method == "POST":
        item_menu = request.POST
        name_menu = item_menu.get('name-menu')
        slug_id = item_menu.get('slug-id')
        name_link = item_menu.getlist('name-link')
        print(name_link)

        

           

        return JsonResponse({'status': 'ok'})
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
