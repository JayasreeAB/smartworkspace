from django.contrib import admin
from .models import (
    Resource,
    Workspace,
    ResourceBooking,
    WorkspaceBooking,
    MaintenanceComplaint,
    GeneralComplaint
)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'resource_type',
        'department',
        'available'
    )


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'workspace_type',
        'capacity',
        'location',
        'available'
    )


@admin.register(ResourceBooking)
class ResourceBookingAdmin(admin.ModelAdmin):
    list_display = (
        'resource',
        'user',
        'booking_date',
        'start_time',
        'end_time',
        'status'
    )

    list_filter = ('status', 'booking_date')


@admin.register(WorkspaceBooking)
class WorkspaceBookingAdmin(admin.ModelAdmin):
    list_display = (
        'workspace',
        'user',
        'booking_date',
        'start_time',
        'end_time',
        'status'
    )

    list_filter = ('status', 'booking_date')


@admin.register(MaintenanceComplaint)
class MaintenanceComplaintAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'resource',
        'workspace',
        'status',
        'created_at'
    )


@admin.register(GeneralComplaint)
class GeneralComplaintAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'subject',
        'status',
        'created_at'
    )