__author__ = 'Daniil'

from django import forms
from image_hosting.models import Image


class UploadForm(forms.ModelForm):
    caption = forms.CharField(max_length=128, help_text="Caption:")
    image = forms.ImageField()

    def clean_image(self):
        image_file = self.cleaned_data.get('image', False)
        if image_file:
            if image_file._size > 10 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 10mb )")
            return image_file
        else:
            raise forms.ValidationError("Couldn't read uploaded image")

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Image
        exclude = ('views', 'up_votes', 'down_votes', 'timestamp')
