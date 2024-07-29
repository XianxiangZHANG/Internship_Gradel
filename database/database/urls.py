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
from web.views import account, project, part, bushing, interface, link, winding, user, department, fiber, resin, r_and_d, sequenceType,docs
from web.views.load_parts import load_parts, load_interfaces, load_links
from web.views.load_fiber_resin import get_fiber_data, get_resin_data
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.views.static import serve
import os



urlpatterns = [
    re_path(r'^documentation/(?P<path>.*)$', docs.serve_docs, name='documentation'),
    path('updateDoc/', docs.upload_docs, name='updateDoc'),

    path('', account.home, name='home0'),
    # path('accounts/login/', account.loginA),
    path('login/', account.login, name='login'),
    path('logout/', account.logout, name='logout'),
    path('img/code/', account.img_code, name='img_code'),
    path('home/', account.home, name='home'),
    # path('home/', log.log_list),
    path('upload/', account.upload, name='upload'),
    path('check/', account.check, name='check'),
    path('changePassword/<int:aid>/', account.changePassword, name='changePassword'),
    path('myLog/', account.user_log, name='user_log'),

    path('fiber/list/', fiber.fiber_list, name='fiber_list'),
    path('fiber/valid/', fiber.fiber_valid, name='fiber_valid'),
    path('fiber/add/', fiber.fiber_add, name='fiber_add'),
    path('fiber/add-multiple/', fiber.fiber_add_multiple, name='fiber_add_multiple'),
    path('fiber/edit/<int:aid>/', fiber.fiber_edit, name='fiber_edit'),
    path('fiber/delete/', fiber.fiber_delete, name='fiber_delete'),
    path('fiber/modify-multiple/', fiber.fiber_modify_multiple, name='fiber_modify_multiple'),

    path('resin/list/', resin.resin_list, name='resin_list'),
    path('resin/list-mechanical-properties/', resin.resin_list_mechanical_properties, name='resin_list_mechanical_properties'),
    path('resin/list-thermophysical-toughness-properties/', resin.resin_list_thermophysical_toughness_properties, name='resin_list_thermophysical_toughness_properties'),
    path('resin/valid/', resin.resin_valid, name='resin_valid'),
    path('resin/valid-mechanical-properties/', resin.resin_valid_mechanical_properties, name='resin_valid_mechanical_properties'),
    path('resin/valid-thermophysical-toughness-properties/', resin.resin_valid_thermophysical_toughness_properties, name='resin_valid_thermophysical_toughness_properties'),
    path('resin/add/', resin.resin_add, name='resin_add'),
    path('resin/add-multiple/', resin.resin_add_multiple, name='resin_add_multiple'),
    path('resin/add-mechanical-properties/', resin.resin_add_mechanical_properties, name='resin_add_mechanical_properties'),
    path('resin/add-thermophysical-toughness-properties/', resin.resin_add_thermophysical_toughness_properties, name='resin_add_thermophysical_toughness_properties'),
    path('resin/edit/<int:aid>/', resin.resin_edit, name='resin_edit'),
    path('resin/delete/', resin.resin_delete, name='resin_delete'),
    path('resin/modify-multiple/', resin.resin_modify_multiple, name='resin_modify_multiple'),
    path('resin/modify-mechanical-properties/', resin.resin_modify_mechanical_properties, name='resin_modify_mechanical_properties'),
    path('resin/modify-thermophysical-toughness-properties/', resin.resin_modify_thermophysical_toughness_properties, name='resin_modify_thermophysical_toughness_properties'),

    path('r_and_d/list/', r_and_d.r_and_d_list, name='r_and_d_list'),
    path('r_and_d/valid/', r_and_d.r_and_d_valid, name='r_and_d_valid'),
    path('r_and_d/add/', r_and_d.r_and_d_add, name='r_and_d_add'),
    path('r_and_d/edit/<int:aid>/', r_and_d.r_and_d_edit, name='r_and_d_edit'),
    path('r_and_d/delete/', r_and_d.r_and_d_delete, name='r_and_d_delete'),
    path('r_and_d/load-fiber-resin/', get_fiber_data, name='get_fiber_data'),
    path('r_and_d/load-fiber-resin/', get_resin_data, name='get_resin_data'),
    path('get-fiber-details/<int:fiber_id>/', get_fiber_data, name='get_fiber_data'),
    path('get-resin-details/<int:resin_id>/', get_resin_data, name='get_resin_data'),

    path('project/list/', project.project_list, name='project_list'),
    path('project/valid/', project.project_valid, name='project_valid'),
    path('project/add/', project.project_add, name='project_add'),
    path('project/edit/<int:aid>/', project.project_edit, name='project_edit'),
    path('project/delete/', project.project_delete, name='project_delete'),
    path('project/upload/', project.upload_file_project, name='upload_file_project'),
    path('project/pdf/', project.download_projects_pdf, name='download_projects_pdf'),

    path('part/list/', part.part_list, name='part_list'),
    path('part/list-doc/', part.part_list_doc, name='part_list_doc'),
    path('part/valid/', part.part_valid, name='part_valid'),
    path('part/valid-doc/', part.part_valid_doc, name='part_valid_doc'),
    path('part/add/', part.part_add, name='part_add'),
    path('part/edit/<int:aid>/', part.part_edit, name='part_edit'),
    path('part/edit-doc/<int:aid>/', part.part_edit_doc, name='part_edit_doc'),
    path('part/delete/', part.part_delete, name='part_delete'),
    path('part/upload/', part.upload_file_part, name='upload_file_part'),
    path('part/pdf/', part.download_parts_pdf, name='download_parts_pdf'),

    path('bushing/list/', bushing.bushing_list, name='bushing_list'),
    path('bushing/valid/', bushing.bushing_valid, name='bushing_valid'),
    path('bushing/add/', bushing.bushing_add, name='bushing_add'),
    path('bushing/edit/<int:aid>/', bushing.bushing_edit, name='bushing_edit'),
    path('bushing/delete/', bushing.bushing_delete, name='bushing_delete'),
    path('bushing/load-parts/', load_parts, name='load_parts'),
    path('bushing/add-multiple/', bushing.bushing_add_multiple, name='bushing_add_multiple'),
    path('bushing/modify-multiple/', bushing.bushing_modify_multiple, name='bushing_modify_multiple'),
    path('bushing/upload/', bushing.upload_file_bushing, name='upload_file_bushing'),
    path('bushing/pdf/', bushing.download_bushings_pdf, name='download_bushings_pdf'),

    path('interface/list/', interface.interface_list, name='interface_list'),
    path('interface/valid/', interface.interface_valid, name='interface_valid'),
    path('interface/add/', interface.interface_add, name='interface_add'),
    path('interface/edit/<int:aid>/', interface.interface_edit, name='interface_edit'),
    path('interface/delete/', interface.interface_delete, name='interface_delete'),
    path('interface/load-parts/', load_parts, name='load_parts'),
    path('interface/add-multiple/', interface.interface_add_multiple, name='interface_add_multiple'),
    path('interface/modify-multiple/', interface.interface_modify_multiple, name='interface_modify_multiple'),
    path('interface/upload/', interface.upload_file_interface, name='upload_file_interface'),
    path('interface/pdf/', interface.download_interfaces_pdf, name='download_interfaces_pdf'),

    path('link/list/', link.link_list, name='link_list'),
    path('link/valid/', link.link_valid, name='link_valid'),
    path('link/add/', link.link_add, name='link_add'),
    path('link/edit/<int:aid>/', link.link_edit, name='link_edit'),
    path('link/delete/', link.link_delete, name='link_delete'),
    path('link/load-parts/', load_parts, name='load_parts'),
    path('link/load-interface/', load_interfaces, name='load_interfaces'),
    path('link/add-multiple/', link.link_add_multiple, name='link_add_multiple'),
    path('link/modify-multiple/', link.link_modify_multiple, name='link_modify_multiple'),
    path('link/upload/', link.upload_file_link, name='upload_file_link'),
    path('link/pdf/', link.download_links_pdf, name='download_links_pdf'),


    path('winding/list/', winding.winding_list, name='winding_list'),
    path('winding/valid/', winding.winding_valid, name='winding_valid'),
    path('winding/add/', winding.winding_add, name='winding_add'),
    path('winding/edit/<int:aid>/', winding.winding_edit, name='winding_edit'),
    path('winding/delete/', winding.winding_delete, name='winding_delete'),
    path('winding/load-parts/', load_parts, name='load_parts'),
    path('winding/load-interface/', load_interfaces, name='load_interfaces'),
    path('winding/load-link/', load_links, name='load_links'),
    path('winding/add-multiple/', winding.winding_add_multiple, name='winding_add_multiple'),
    path('winding/modify-multiple/', winding.winding_modify_multiple, name='winding_modify_multiple'),

    path('user/list/', user.user_list, name='user_list'),
    path('user/list-read/', user.user_list_read, name='user_list_read'),
    path('user/edit/<int:aid>/', user.user_edit, name='user_edit'),
    path('user/delete/', user.user_delete, name='user_delete'),
    path('user/add-multiple/', user.user_add_multiple, name='user_add_multiple'),
    path('user/modify-multiple/', user.user_modify_multiple, name='user_modify_multiple'),

    path('department/list/', department.department_list, name='department_list'),
    path('department/list-read/', department.department_list_read, name='department_list_read'),
    path('department/edit/<int:aid>/', department.department_edit, name='department_edit'),
    path('department/delete/', department.department_delete, name='department_delete'),
    path('department/add-multiple/', department.department_add_multiple, name='department_add_multiple'),
    path('department/modify-multiple/', department.department_modify_multiple, name='department_modify_multiple'),

    path('sequenceType/list/', sequenceType.sequenceType_list, name='sequenceType_list'),
    path('sequenceType/valid/', sequenceType.sequenceType_valid, name='sequenceType_valid'),
    path('sequenceType/edit/<int:aid>/', sequenceType.sequenceType_edit, name='sequenceType_edit'),
    path('sequenceType/delete/', sequenceType.sequenceType_delete, name='sequenceType_delete'),
    path('sequenceType/add-multiple/', sequenceType.sequenceType_add_multiple, name='sequenceType_add_multiple'),
    path('sequenceType/modify-multiple/', sequenceType.sequenceType_modify_multiple, name='sequenceType_modify_multiple'),
    path('sequenceType/pdf/', sequenceType.download_sequenceTypes_pdf, name='download_sequenceTypes_pdf'),

    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)