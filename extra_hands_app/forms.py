from django import forms
from models import Event, Available_Time

class EventForm(forms.ModelForm):
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()
    client = forms.CharField(widget=forms.HiddenInput(), required = False)
    teacher = forms.CharField(widget=forms.HiddenInput(), required = False)
    is_open = forms.BooleanField(widget=forms.HiddenInput(), required = False)
    in_progress = forms.BooleanField(widget=forms.HiddenInput(), required = False)

    class Meta:
        model = Event
        fields=('start_time', 'end_time', )
