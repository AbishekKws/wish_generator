from .models import Wish, MusicLibrary, CelebrationTemplate
from .models import Wish, MusicLibrary
from django import forms


class WishForm(forms.ModelForm):
    images = forms.FileField(
        required=False,
        widget=forms.FileInput()
    )

    class Meta:
        model = Wish
        fields = ['sender_name', 'receiver_name', 'message', 'selected_music', 'custom_music']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your sweet message...'}),
            'sender_name': forms.TextInput(attrs={'placeholder': 'Your Name/Nickname'}),
            'receiver_name': forms.TextInput(attrs={'placeholder': 'His/Her Name/Nickname'}),
        }

    def __init__(self, *args, **kwargs):
        wish_type = kwargs.pop('wish_type', None)
        super(WishForm, self).__init__(*args, **kwargs)

        self.fields['selected_music'].empty_label = "Select Music"
        
        # Multiple images upload 
        self.fields['images'].widget.attrs.update({'multiple': True})
        
        # Filter music library
        if wish_type:
            self.fields['selected_music'].queryset = MusicLibrary.objects.filter(category__name__icontains=wish_type)

        self.fields['selected_music'].label_from_instance = lambda obj: f"{obj.title}"
        
        # Adding Tailwind classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:border-pink-500 outline-none transition'
            })

class MusicLibraryForm(forms.ModelForm):
    class Meta:
        model = MusicLibrary
        fields = ['title', 'category', 'audio_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'audio_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class TemplateForm(forms.ModelForm):
    class Meta:
        model = CelebrationTemplate
        fields = ['template_id', 'name', 'preview_image']
        widgets = {
            'template_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'preview_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
