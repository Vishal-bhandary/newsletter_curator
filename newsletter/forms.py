from django import forms
from .models import Subscriber

class SubscriberForm(forms.ModelForm):
    categories = forms.MultipleChoiceField(
        choices=Subscriber.CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Choose your categories of interest"
    )
    frequency = forms.ChoiceField(
        choices=Subscriber.FREQUENCY_CHOICES,
        widget=forms.RadioSelect,
        label="Newsletter frequency"
    )

    class Meta:
        model = Subscriber
        fields = ['email', 'categories', 'frequency']
