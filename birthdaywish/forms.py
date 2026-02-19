from django import forms
from .models import BirthdayWish

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

class WishCreationForm(forms.ModelForm):
    images = MultipleFileField(required=False, label="Select Multiple Memories")

    class Meta:
        model = BirthdayWish
        fields = ['sender_name', 'receiver_name', 'message']
