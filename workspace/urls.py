from django.urls import path
from . import views


urlpatterns = [

    path('', views.landing, name='landing'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact, name='contact'),

    path('home/', views.home, name='home'),

    path('profile/', views.profile, name='profile'),

    # User Resources
    path('resources/', views.resources, name='resources'),

    path(
        'resources/<int:resource_id>/',
        views.resource_detail,
        name='resource_detail'
    ),

    path(
        'resources/<int:resource_id>/book/',
        views.book_resource,
        name='book_resource'
    ),

    # User Workspaces
    path('workspaces/', views.workspaces, name='workspaces'),

    path(
        'workspaces/<int:workspace_id>/',
        views.workspace_detail,
        name='workspace_detail'
    ),

    path(
        'workspaces/<int:workspace_id>/book/',
        views.book_workspace,
        name='book_workspace'
    ),

    # User Complaints
    path(
        'maintenance/',
        views.maintenance,
        name='maintenance'
    ),

    path(
        'complaint/',
        views.complaint,
        name='complaint'
    ),

    # =========================
    # CUSTOM ADMIN
    # =========================

    path(
        'admin-home/',
        views.admin_home,
        name='admin_home'
    ),

    # Admin Workspaces
    path(
        'admin-home/workspaces/',
        views.admin_workspaces,
        name='admin_workspaces'
    ),

    path(
        'admin-home/workspaces/add/',
        views.admin_workspace_add,
        name='admin_workspace_add'
    ),

    path(
        'admin-home/workspaces/<int:workspace_id>/edit/',
        views.admin_workspace_edit,
        name='admin_workspace_edit'
    ),

    path(
        'admin-home/workspaces/<int:workspace_id>/delete/',
        views.admin_workspace_delete,
        name='admin_workspace_delete'
    ),

    path(
        'admin-home/workspaces/booking/<int:booking_id>/cancel/',
        views.admin_cancel_workspace_booking,
        name='admin_cancel_workspace_booking'
    ),

    path(
        'admin-home/workspaces/booking/<int:booking_id>/delete/',
        views.admin_delete_workspace_booking,
        name='admin_delete_workspace_booking'
    ),

    # Admin Resources
    path(
        'admin-home/resources/',
        views.admin_resources,
        name='admin_resources'
    ),

    path(
        'admin-home/resources/add/',
        views.admin_resource_add,
        name='admin_resource_add'
    ),

    path(
        'admin-home/resources/<int:resource_id>/edit/',
        views.admin_resource_edit,
        name='admin_resource_edit'
    ),

    path(
        'admin-home/resources/<int:resource_id>/delete/',
        views.admin_resource_delete,
        name='admin_resource_delete'
    ),

    path(
        'admin-home/resources/booking/<int:booking_id>/cancel/',
        views.admin_cancel_resource_booking,
        name='admin_cancel_resource_booking'
    ),

    path(
        'admin-home/resources/booking/<int:booking_id>/delete/',
        views.admin_delete_resource_booking,
        name='admin_delete_resource_booking'
    ),

    # Admin Maintenance
    path(
        'admin-home/maintenance/',
        views.admin_maintenance,
        name='admin_maintenance'
    ),

    # Admin General Complaints
    path(
        'admin-home/complaints/',
        views.admin_complaints,
        name='admin_complaints'
    ),

]