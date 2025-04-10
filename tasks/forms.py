from django import forms
from .models import Task, Comment


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "priority",
            "due_date"
        ]

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Назва задачі',
                                            'class': 'input-field',
                                            'label': 'Назва задачі'
                }
            ),
            'description': forms.TextInput(attrs={'placeholder': 'Опис задачі',
                                                 'class': 'input-field'
                }
            ),
            'status': forms.Select(attrs={'class': 'input-field'
                }
            ),
            'priority': forms.Select(attrs={'class': 'input-field'
                }
            ),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local',
                                                   'class': 'input-field'
                }
            )
        }

        labels = {
            'title': 'Назва задачі',
            'description': 'Опис задачі',
            'status': 'Статус',
            'priority': 'Пріоритет',
            'due_date': 'Термін виконання',
        }


class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ("", "Всі"),
        ("todo", "To Do"),
        ("in_progress", "В прогресі"),
        ("done", "Виконано"),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Статус")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 
                  'media']
        
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Коментар',
                                             'class': 'input-field',
                                             'label': 'Коментар'
                }
            ),
            'media': forms.FileInput()
        }

        labels = {
            'content': 'Коментар',
            'media': 'Медіа'
        }