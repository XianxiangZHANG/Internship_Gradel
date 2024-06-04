"""database URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from web.views import account, project, part, bushing, interface, link, winding, user, department, fiber, resin, r_and_d, sequenceType
from web.views.load_parts import load_parts, load_interfaces, load_links
from web.views.load_fiber_resin import get_fiber_data, get_resin_data



urlpatterns = [
    # path('', account.login),
    # path('accounts/login/', account.loginA),
    path('login/', account.login),
    path('logout/', account.logout),
    path('img/code/', account.img_code),
    path('home/', account.home),
    path('upload/', account.upload),
    path('check/', account.check),
    path('changePassword/<int:aid>/', account.changePassword),

    path('fiber/list/', fiber.fiber_list),
    path('fiber/valid/', fiber.fiber_valid),
    path('fiber/add/', fiber.fiber_add),
    path('fiber/add-multiple/', fiber.fiber_add_multiple),
    path('fiber/edit/<int:aid>/', fiber.fiber_edit),
    path('fiber/delete/', fiber.fiber_delete),
    path('fiber/modify-multiple/', fiber.fiber_modify_multiple),

    path('resin/list/', resin.resin_list),
    path('resin/valid/', resin.resin_valid),
    path('resin/add/', resin.resin_add),
    path('resin/add-multiple/', resin.resin_add_multiple),
    path('resin/edit/<int:aid>/', resin.resin_edit),
    path('resin/delete/', resin.resin_delete),
    path('resin/modify-multiple/', resin.resin_modify_multiple),

    path('r_and_d/list/', r_and_d.r_and_d_list),
    path('r_and_d/valid/', r_and_d.r_and_d_valid),
    path('r_and_d/add/', r_and_d.r_and_d_add),
    path('r_and_d/add-multiple/', r_and_d.r_and_d_add_multiple),
    path('r_and_d/edit/<int:aid>/', r_and_d.r_and_d_edit),
    path('r_and_d/delete/', r_and_d.r_and_d_delete),
    path('r_and_d/modify-multiple/', r_and_d.r_and_d_modify_multiple),
    path('r_and_d/load-fiber-resin/', get_fiber_data, name='get_fiber_data'),
    path('r_and_d/load-fiber-resin/', get_resin_data, name='get_resin_data'),
    path('get-fiber-details/<int:fiber_id>/', get_fiber_data, name='get_fiber_data'),
    path('get-resin-details/<int:resin_id>/', get_resin_data, name='get_resin_data'),

    path('project/list/', project.project_list),
    path('project/valid/', project.project_valid),
    # path('project/input/', project.project_input),
    path('project/add/', project.project_add),
    # /project/edit/123/
    path('project/edit/<int:aid>/', project.project_edit),
    # /project/delete/?aid=123
    path('project/delete/', project.project_delete),

    path('part/list/', part.part_list),
    path('part/valid/', part.part_valid),
    path('part/add/', part.part_add),
    path('part/edit/<int:aid>/', part.part_edit),
    path('part/delete/', part.part_delete),

    path('bushing/list/', bushing.bushing_list),
    path('bushing/valid/', bushing.bushing_valid),
    path('bushing/add/', bushing.bushing_add),
    path('bushing/edit/<int:aid>/', bushing.bushing_edit),
    path('bushing/delete/', bushing.bushing_delete),
    path('bushing/load-parts/', load_parts, name='load_parts'),
    path('bushing/add-multiple/', bushing.bushing_add_multiple),
    path('bushing/modify-multiple/', bushing.bushing_modify_multiple),

    path('interface/list/', interface.interface_list),
    path('interface/valid/', interface.interface_valid),
    path('interface/add/', interface.interface_add),
    path('interface/edit/<int:aid>/', interface.interface_edit),
    path('interface/delete/', interface.interface_delete),
    path('interface/load-parts/', load_parts, name='load_parts'),
    path('interface/add-multiple/', interface.interface_add_multiple),
    path('interface/modify-multiple/', interface.interface_modify_multiple),

    path('link/list/', link.link_list),
    path('link/valid/', link.link_valid),
    path('link/add/', link.link_add),
    path('link/edit/<int:aid>/', link.link_edit),
    path('link/delete/', link.link_delete),
    path('link/load-parts/', load_parts, name='load_parts'),
    path('link/load-interface/', load_interfaces, name='load_interfaces'),
    path('link/add-multiple/', link.link_add_multiple),
    path('link/modify-multiple/', link.link_modify_multiple),

    path('winding/list/', winding.winding_list),
    path('winding/valid/', winding.winding_valid),
    path('winding/add/', winding.winding_add),
    path('winding/edit/<int:aid>/', winding.winding_edit),
    path('winding/delete/', winding.winding_delete),
    path('winding/load-parts/', load_parts, name='load_parts'),
    path('winding/load-interface/', load_interfaces, name='load_interfaces'),
    path('winding/load-link/', load_links, name='load_links'),
    path('winding/add-multiple/', winding.winding_add_multiple),
    path('winding/modify-multiple/', winding.winding_modify_multiple),

    path('user/list/', user.user_list),
    path('user/edit/<int:aid>/', user.user_edit),
    path('user/delete/', user.user_delete),
    path('user/add-multiple/', user.user_add_multiple),
    path('user/modify-multiple/', user.user_modify_multiple),

    path('department/list/', department.department_list),
    path('department/edit/<int:aid>/', department.department_edit),
    path('department/delete/', department.department_delete),
    path('department/add-multiple/', department.department_add_multiple),
    path('department/modify-multiple/', department.department_modify_multiple),

    path('sequenceType/list/', sequenceType.sequenceType_list),
    path('sequenceType/valid/', sequenceType.sequenceType_valid),
    path('sequenceType/edit/<int:aid>/', sequenceType.sequenceType_edit),
    path('sequenceType/delete/', sequenceType.sequenceType_delete),
    path('sequenceType/add-multiple/', sequenceType.sequenceType_add_multiple),
    path('sequenceType/modify-multiple/', sequenceType.sequenceType_modify_multiple),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)