from django import forms

from .models import (
    Resource,
    Workspace
)


class ResourceForm(forms.ModelForm):

    class Meta:
        model = Resource
        fields = '__all__'


class WorkspaceForm(forms.ModelForm):

    class Meta:
        model = Workspace
        fields = '__all__'