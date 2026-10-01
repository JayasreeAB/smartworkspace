from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

from .models import (Resource,Workspace,ResourceBooking,WorkspaceBooking,MaintenanceComplaint,GeneralComplaint)


def landing(request):
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'workspace/landing.html')

def contact(request):

    return render(
        request,
        'workspace/contact.html'
    )


def register_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect('home')

    return render(request, 'workspace/register.html')


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        login_type = request.POST.get('login_type')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if login_type == 'admin':

                if user.is_staff:

                    login(request, user)

                    return redirect('admin_home')

                else:

                    messages.error(
                        request,
                        'This account does not have administrator access.'
                    )

                    return redirect('login')

            else:

                # Normal user login
                login(request, user)

                return redirect('home')

        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

    return render(
        request,
        'workspace/login.html'
    )

def logout_view(request):
    logout(request)
    return redirect('landing')


@login_required
def home(request):

    return render(
        request,
        'workspace/home.html'
    )


@login_required
def profile(request):

    resource_bookings = ResourceBooking.objects.filter(
        user=request.user
    ).order_by('-booking_date')

    workspace_bookings = WorkspaceBooking.objects.filter(
        user=request.user
    ).order_by('-booking_date')

    return render(
        request,
        'workspace/profile.html',
        {
            'resource_bookings': resource_bookings,
            'workspace_bookings': workspace_bookings
        }
    )


@login_required
def resources(request):

    resource_list = Resource.objects.filter(
        available=True
    )

    return render(
        request,
        'workspace/resources.html',
        {
            'resources': resource_list
        }
    )


@login_required
def resource_detail(request, resource_id):

    resource = get_object_or_404(
        Resource,
        id=resource_id
    )

    bookings = ResourceBooking.objects.filter(
        resource=resource,
        status__in=['Pending', 'Approved']
    ).order_by(
        'booking_date',
        'start_time'
    )

    return render(
        request,
        'workspace/resource_detail.html',
        {
            'resource': resource,
            'bookings': bookings
        }
    )

@login_required
def book_resource(request, resource_id):

    resource = get_object_or_404(
        Resource,
        id=resource_id
    )

    if request.method == 'POST':

        booking_date = request.POST.get('booking_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        # Check that end time is after start time
        if start_time >= end_time:

            messages.error(
                request,
                'End time must be after start time.'
            )

            return redirect(
                'resource_detail',
                resource_id=resource.id
            )

        # Check for overlapping bookings
        overlapping_booking = ResourceBooking.objects.filter(
            resource=resource,
            booking_date=booking_date,
            status__in=['Pending', 'Approved'],
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if overlapping_booking:

            messages.error(
                request,
                'This resource is already booked during this time.'
            )

            return redirect(
                'resource_detail',
                resource_id=resource.id
            )

        ResourceBooking.objects.create(
            user=request.user,
            resource=resource,
            purpose=request.POST.get('purpose'),
            department=request.POST.get('department'),
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time
        )

        messages.success(
            request,
            'Resource booking request submitted.'
        )

        return redirect(
            'resource_detail',
            resource_id=resource.id
        )

    return redirect(
        'resource_detail',
        resource_id=resource.id
    )

@login_required
def workspaces(request):

    workspace_list = Workspace.objects.filter(
        available=True
    )

    return render(
        request,
        'workspace/workspaces.html',
        {
            'workspaces': workspace_list
        }
    )


@login_required
def workspace_detail(request, workspace_id):

    workspace = get_object_or_404(
        Workspace,
        id=workspace_id
    )

    bookings = WorkspaceBooking.objects.filter(
        workspace=workspace,
        status__in=['Pending', 'Approved']
        ).order_by(
            'booking_date',
            'start_time'
        )

    return render(
        request,
        'workspace/workspace_detail.html',
        {
            'workspace': workspace,
            'bookings': bookings
        }
    )

@login_required
def book_workspace(request, workspace_id):

    workspace = get_object_or_404(
        Workspace,
        id=workspace_id
    )

    if request.method == 'POST':

        booking_date = request.POST.get('booking_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        # Check that end time is after start time
        if start_time >= end_time:

            messages.error(
                request,
                'End time must be after start time.'
            )

            return redirect(
                'workspace_detail',
                workspace_id=workspace.id
            )

        # Check for overlapping bookings
        overlapping_booking = WorkspaceBooking.objects.filter(
            workspace=workspace,
            booking_date=booking_date,
            status__in=['Pending', 'Approved'],
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if overlapping_booking:

            messages.error(
                request,
                'This workspace is already booked during this time.'
            )

            return redirect(
                'workspace_detail',
                workspace_id=workspace.id
            )

        WorkspaceBooking.objects.create(
            user=request.user,
            workspace=workspace,
            purpose=request.POST.get('purpose'),
            department=request.POST.get('department'),
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time
        )

        messages.success(
            request,
            'Workspace booking request submitted.'
        )

        return redirect(
            'workspace_detail',
            workspace_id=workspace.id
        )

    return redirect(
        'workspace_detail',
        workspace_id=workspace.id
    )


@login_required
def maintenance(request):

    resources = Resource.objects.filter(
        available=True
    )

    workspaces = Workspace.objects.filter(
        available=True
    )

    if request.method == 'POST':

        resource_id = request.POST.get('resource')
        workspace_id = request.POST.get('workspace')

        resource = None
        workspace = None

        if resource_id:
            resource = Resource.objects.get(
                id=resource_id
            )

        if workspace_id:
            workspace = Workspace.objects.get(
                id=workspace_id
            )

        MaintenanceComplaint.objects.create(
            user=request.user,
            resource=resource,
            workspace=workspace,
            description=request.POST.get('description'),
            image=request.FILES.get('image')
        )

        messages.success(
            request,
            'Maintenance complaint submitted.'
        )

        return redirect('home')

    return render(
        request,
        'workspace/maintenance.html',
        {
            'resources': resources,
            'workspaces': workspaces
        }
    )


@login_required
def complaint(request):

    if request.method == 'POST':

        GeneralComplaint.objects.create(
            user=request.user,
            subject=request.POST.get('subject'),
            description=request.POST.get('description')
        )

        messages.success(
            request,
            'Complaint submitted successfully.'
        )

        return redirect('home')

    return render(
        request,
        'workspace/complaint.html'
    )

@staff_member_required
def admin_home(request):

    resource_count = Resource.objects.count()
    workspace_count = Workspace.objects.count()

    resource_booking_count = ResourceBooking.objects.count()
    workspace_booking_count = WorkspaceBooking.objects.count()

    maintenance_count = MaintenanceComplaint.objects.count()
    complaint_count = GeneralComplaint.objects.count()

    return render(
        request,
        'workspace/admin_home.html',
        {
            'resource_count': resource_count,
            'workspace_count': workspace_count,
            'resource_booking_count': resource_booking_count,
            'workspace_booking_count': workspace_booking_count,
            'maintenance_count': maintenance_count,
            'complaint_count': complaint_count,
        }
    )

@staff_member_required
def admin_workspaces(request):

    workspaces = Workspace.objects.all()

    workspace_bookings = WorkspaceBooking.objects.select_related(
        'workspace',
        'user'
    ).order_by(
        '-booking_date',
        '-start_time'
    )

    today = timezone.localdate()

    past_bookings = workspace_bookings.filter(
        booking_date__lt=today
    )

    future_bookings = workspace_bookings.filter(
        booking_date__gte=today
    )

    return render(
        request,
        'workspace/admin_workspaces.html',
        {
            'workspaces': workspaces,
            'past_bookings': past_bookings,
            'future_bookings': future_bookings,
        }
    )

@staff_member_required
def admin_resources(request):

    resources = Resource.objects.all()

    resource_bookings = ResourceBooking.objects.select_related(
        'resource',
        'user'
    ).order_by(
        '-booking_date',
        '-start_time'
    )

    today = timezone.localdate()

    past_bookings = resource_bookings.filter(
        booking_date__lt=today
    )

    future_bookings = resource_bookings.filter(
        booking_date__gte=today
    )

    return render(
        request,
        'workspace/admin_resources.html',
        {
            'resources': resources,
            'past_bookings': past_bookings,
            'future_bookings': future_bookings,
        }
    )

@staff_member_required
def admin_resource_add(request):

    from .forms import ResourceForm

    if request.method == 'POST':

        form = ResourceForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Resource added successfully.'
            )

            return redirect('admin_resources')

    else:

        form = ResourceForm()

    return render(
        request,
        'workspace/admin_resource_form.html',
        {
            'form': form,
            'title': 'Add Resource'
        }
    )


@staff_member_required
def admin_resource_edit(request, resource_id):

    from .forms import ResourceForm

    resource = get_object_or_404(
        Resource,
        id=resource_id
    )

    if request.method == 'POST':

        form = ResourceForm(
            request.POST,
            instance=resource
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Resource updated successfully.'
            )

            return redirect('admin_resources')

    else:

        form = ResourceForm(
            instance=resource
        )

    return render(
        request,
        'workspace/admin_resource_form.html',
        {
            'form': form,
            'title': 'Edit Resource'
        }
    )


@staff_member_required
def admin_resource_delete(request, resource_id):

    resource = get_object_or_404(
        Resource,
        id=resource_id
    )

    if request.method == 'POST':

        resource.delete()

        messages.success(
            request,
            'Resource deleted successfully.'
        )

    return redirect('admin_resources')


@staff_member_required
def admin_workspace_add(request):

    from .forms import WorkspaceForm

    if request.method == 'POST':

        form = WorkspaceForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Workspace added successfully.'
            )

            return redirect('admin_workspaces')

    else:

        form = WorkspaceForm()

    return render(
        request,
        'workspace/admin_workspace_form.html',
        {
            'form': form,
            'title': 'Add Workspace'
        }
    )

@staff_member_required
def admin_workspace_edit(request, workspace_id):

    from .forms import WorkspaceForm

    workspace = get_object_or_404(
        Workspace,
        id=workspace_id
    )

    if request.method == 'POST':

        form = WorkspaceForm(
            request.POST,
            instance=workspace
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Workspace updated successfully.'
            )

            return redirect('admin_workspaces')

    else:

        form = WorkspaceForm(
            instance=workspace
        )

    return render(
        request,
        'workspace/admin_workspace_form.html',
        {
            'form': form,
            'title': 'Edit Workspace'
        }
    )

@staff_member_required
def admin_workspace_delete(request, workspace_id):

    workspace = get_object_or_404(
        Workspace,
        id=workspace_id
    )

    if request.method == 'POST':

        workspace.delete()

        messages.success(
            request,
            'Workspace deleted successfully.'
        )

    return redirect('admin_workspaces')

@staff_member_required
def admin_cancel_resource_booking(request, booking_id):

    booking = get_object_or_404(
        ResourceBooking,
        id=booking_id
    )

    if request.method == 'POST':

        booking.status = 'Cancelled'
        booking.save()

        messages.success(
            request,
            'Resource booking cancelled.'
        )

    return redirect('admin_resources')

@staff_member_required
def admin_cancel_workspace_booking(request, booking_id):

    booking = get_object_or_404(
        WorkspaceBooking,
        id=booking_id
    )

    if request.method == 'POST':

        booking.status = 'Cancelled'
        booking.save()

        messages.success(
            request,
            'Workspace booking cancelled.'
        )

    return redirect('admin_workspaces')

@staff_member_required
def admin_delete_resource_booking(request, booking_id):

    booking = get_object_or_404(
        ResourceBooking,
        id=booking_id
    )

    if request.method == 'POST':

        booking.delete()

        messages.success(
            request,
            'Resource booking deleted.'
        )

    return redirect('admin_resources')

@staff_member_required
def admin_delete_workspace_booking(request, booking_id):

    booking = get_object_or_404(
        WorkspaceBooking,
        id=booking_id
    )

    if request.method == 'POST':

        booking.delete()

        messages.success(
            request,
            'Workspace booking deleted.'
        )

    return redirect('admin_workspaces')

@staff_member_required
def admin_maintenance(request):

    complaints = MaintenanceComplaint.objects.select_related(
        'user',
        'resource',
        'workspace'
    ).order_by('-id')

    return render(
        request,
        'workspace/admin_maintenance.html',
        {
            'complaints': complaints
        }
    )

@staff_member_required
def admin_complaints(request):

    complaints = GeneralComplaint.objects.select_related(
        'user'
    ).order_by('-id')

    return render(
        request,
        'workspace/admin_complaints.html',
        {
            'complaints': complaints
        }
    )

