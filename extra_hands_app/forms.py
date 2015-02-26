from django import forms
from models import Event, Available_Time, User, Teacher, Client
from datetimewidget.widgets import DateTimeWidget

class EventForm(forms.ModelForm):
    dateTimeOptions={
        'format': 'mm/dd/yyyy HH:ii'
    }

    start_time = forms.DateTimeField(widget=DateTimeWidget(bootstrap_version=3, options=dateTimeOptions))
    end_time = forms.DateTimeField(widget=DateTimeWidget(bootstrap_version=3, options=dateTimeOptions))
    client = forms.CharField(widget=forms.HiddenInput(), required = False)
    teacher = forms.CharField(widget=forms.HiddenInput(), required = False)
    is_open = forms.BooleanField(widget=forms.HiddenInput(), required = False)
    in_progress = forms.BooleanField(widget=forms.HiddenInput(), required = False)
    comments = forms.CharField(widget=forms.Textarea())
    token = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    is_on_call = forms.BooleanField()

    class Meta:
        model = Event
        fields=('start_time', 'end_time', 'is_on_call', 'comments', 'token' )




##User/Client/Teacher forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ('on_call', 'is_available', 'slug', 'user', 'clicks', 'token')


class ClientForm(forms.ModelForm):
    class Meta:
        model= Client
        exclude= ('user', 'client_slug', 'campus', 'token')


