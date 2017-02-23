from django import forms

from video.models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = '__all__'

# class SearchForm(forms.Form):
#     query = forms.CharField()
#     max_results = forms.IntegerField(required=False, min_value=1)
