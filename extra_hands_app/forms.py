from django import forms
from models import Event, Available_Time, User, Teacher, Client
from datetimewidget.widgets import DateTimeWidget
import datetime
from django.utils import timezone

class EventForm(forms.ModelForm):
    dateTimeOptions={
        'format': 'mm/dd/yyyy hh:ii'
    }

    start_time = forms.DateTimeField(widget=DateTimeWidget(bootstrap_version=3, options=dateTimeOptions))
    end_time = forms.DateTimeField(widget=DateTimeWidget(bootstrap_version=3, options=dateTimeOptions))
    client = forms.CharField(widget=forms.HiddenInput(), required = False)
    teacher = forms.CharField(widget=forms.HiddenInput(), required = False)
    is_open = forms.BooleanField(widget=forms.HiddenInput(), required = False)
    in_progress = forms.BooleanField(widget=forms.HiddenInput(), required = False)
    comments = forms.CharField(widget=forms.Textarea())
    token = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    is_on_call = forms.BooleanField(required=False)
    event_class = forms.CharField(widget=forms.HiddenInput(), required=False)

    # My thought is to make all events one color by default and force the on-call event to be red or yellow
    # Otherwise the different options may be a bit confusing to the users
    # event_class_choices = (
    #     ('event-important', 'important'),
    #     ('success', 'event-success'),
    #     ('warning', 'event')
    # )

    def is_valid(self):
        valid = super(EventForm, self).is_valid()


        if not valid:
            return valid

        if self.cleaned_data['end_time'] <= self.cleaned_data['start_time']:
            self._errors['invalid_entry'] = 'The end time must be after the start time'
            return False

        if self.cleaned_data['start_time'] <= datetime.datetime.now():
            self._errors['invalid_entry'] = 'The event cannot begin in the past'
            return False

        return True

    class Meta:
        model = Event
        fields=('start_time', 'end_time', 'is_on_call', 'comments', 'token' )


class AvailableTimeForm(forms.ModelForm):
    dateTimeOptions={
        'format': 'mm/dd/yyyy hh:ii'
    }

    start_time = forms.DateTimeField(widget=DateTimeWidget(bootstrap_version=3, options=dateTimeOptions))
    end_time = forms.DateTimeField(widget=DateTimeWidget(bootstrap_version=3, options=dateTimeOptions))
    teacher = forms.CharField(widget=forms.HiddenInput(), required=False)
    event_class = forms.CharField(widget=forms.HiddenInput(), required=False)

    def is_valid(self):
        valid = super(AvailableTimeForm, self).is_valid()

        if not valid:
            return valid

        if self.cleaned_data['end_time'] <= self.cleaned_data['start_time']:
            self._errors['invalid_entry'] = 'The end time must be after the start time'
            return False

        return True

    class Meta:
        model = Available_Time
        fields=('start_time', 'end_time', )


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


