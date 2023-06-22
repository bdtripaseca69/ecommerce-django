from django import forms
from .models import ReviewRating

#203 creacion del form de review
class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']