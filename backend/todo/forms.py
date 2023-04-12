from django import forms
from .models import Task

class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('created','is_complete')


class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('author',)



class DoneToggleForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('is_complete',)