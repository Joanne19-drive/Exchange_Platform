from django import forms
from . import models


class ForeignForm(forms.ModelForm):
    class Meta:
        model = models.Foreign
        fields = ['away_apply', 'language_score', 'course_enroll',
                  'accommodation', 'atmosphere', 'club', 'away_scholarship']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'content', 'away_year', 'away_semester']