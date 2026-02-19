from django import forms
from .models import InteractiveWish

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class WishCreateForm(forms.ModelForm):
    images = MultipleFileField(
        label="Upload 3-6 Memories",
        required=True,
        widget=MultipleFileInput(attrs={'multiple': True, 'class': 'form-control'})
    )
    
    class Meta:
        model = InteractiveWish
        fields = ['sender_name', 'receiver_name', 'message', 'music']
