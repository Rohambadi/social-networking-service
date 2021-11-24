from django import forms
from .models import Image
from django.utils.text import slugify
from urllib import request
from django.core.files.base import ContentFile


class ImagePostForm(forms.ModelForm):

    class Meta:
        model = Image
        fields =('title', 'description', 'image')
        '''widgets = {
            'title': forms.HiddenInput,
            'description': forms.HiddenInput,
        }'''


class ComImagePostForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'description')


class ImageCreateForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['png', 'jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('the given URL does not'
                                        'match valid image extension.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        extension = image_url.rsplit('.', 1)[1].lower()
        name = slugify(image.title)
        image_name = f'{name}.{extension}'

        # Download image
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()),
                         save=False)
        if commit:
            image.save()
        return image