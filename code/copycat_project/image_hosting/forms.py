__author__ = 'Daniil'

from django import forms
from image_hosting.models import Image, Category


class UploadForm(forms.ModelForm):
    caption = forms.CharField(max_length=128, help_text="Caption:")
    CAT_CHOICES = (
        ('Funny', 'Professional', 'Other'),
    )
    #category = forms.ChoiceField(choices=CAT_CHOICES, required=True)
    image = forms.ImageField()
    url_image_name = forms.CharField(widget=forms.HiddenInput(), initial='')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    up_votes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    down_votes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Image
