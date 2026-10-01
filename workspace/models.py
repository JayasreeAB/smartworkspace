from django.db import models
from django.contrib.auth.models import User


class Resource(models.Model):
    RESOURCE_TYPES = [
        ('Equipment', 'Equipment'),
        ('Projector', 'Projector'),
        ('Computer', 'Computer'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    description = models.TextField()
    previous_uses = models.TextField(blank=True)
    image = models.ImageField(upload_to='resources/', blank=True, null=True)
    department = models.CharField(max_length=100, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Workspace(models.Model):
    WORKSPACE_TYPES = [
        ('Meeting Room', 'Meeting Room'),
        ('Seminar Hall', 'Seminar Hall'),
        ('Workstation', 'Workstation'),
        ('Conference Room', 'Conference Room'),
    ]

    name = models.CharField(max_length=100)
    workspace_type = models.CharField(max_length=50, choices=WORKSPACE_TYPES)
    description = models.TextField()
    capacity = models.IntegerField(default=1)
    location = models.CharField(max_length=150)
    image = models.ImageField(upload_to='workspaces/', blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ResourceBooking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    purpose = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resource.name} - {self.user.username}"


class WorkspaceBooking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)

    purpose = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.workspace.name} - {self.user.username}"


class MaintenanceComplaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    description = models.TextField()
    image = models.ImageField(
        upload_to='complaints/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Maintenance complaint - {self.user.username}"


class GeneralComplaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    subject = models.CharField(max_length=200)
    description = models.TextField()

    status = models.CharField(
        max_length=30,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject