from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
import ast
from django.template.defaultfilters import slugify

# Create your models here.
# User class contains username, password, email address, first name, last name

class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)



class Client(models.Model):
    user = models.OneToOneField(User)
    ##
    organization = models.CharField(max_length=128)
    street = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    phone_number = models.CharField(max_length=15)
    description = models.CharField(max_length=600)
    client_slug = models.SlugField(unique=True)
    campus = models.IntegerField(default=1)
    # token = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.client_slug = slugify(self.organization)
        # if self.token is None:
        #     self.token = random.randint(100000,999999)
        super(Client, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.organization


class Teacher(models.Model):
    user = models.OneToOneField(User)
    ##
    street = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    phone_number = models.CharField(max_length=15)
    ect_qualified = models.BooleanField(default=False)
    cpr_first_aid = models.BooleanField(default=False)
    universal_precautions = models.BooleanField(default=False)
    qualifications = models.CharField(max_length =300)
    degree = models.CharField(max_length=30)
    major = models.CharField(max_length=100)
    is_available = models.BooleanField(default=False)
    on_call = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    clicks = models.IntegerField(default=0)
    # token = models.IntegerField(default=0)
    regular_rate = models.DecimalField(max_digits=6, decimal_places=2, default = 11.00)
    extra_rate = models.DecimalField(max_digits=6, decimal_places=2, default = 13.00)
    time_between_events = models.DecimalField(max_digits = 6, decimal_places = 2, default = 1)



    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.get_full_name())
        # if self.token is None:
        #     self.token = random.randint(100000,999999)
        super(Teacher, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.get_full_name()


class Event(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    teacher = models.ForeignKey(Teacher, blank=True, null=True, default=None)
    client = models.ForeignKey(Client)
    is_open = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=False)
    # token = models.IntegerField(default=0)
    comments = models.CharField(max_length=500, blank=True, default ='')
    is_on_call = models.BooleanField(default=False)
    event_class = models.CharField(max_length=100, default='event-info')
    times_available = ListField(default = [])
    times_emailed = ListField(default = [])


    def save(self, *args, **kwargs):
        # if statement required to not overwrite token on editing
        # if self.token is None:
        #     self.token = random.randint(100000,999999)
        super(Event, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.start_time)


class Available_Time(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    teacher = models.ForeignKey(Teacher)
    event_class = models.CharField(max_length=100, default='event-warning')
    active = models.BooleanField(default=True)




class Email_List(models.Model):
    email = models.EmailField()


class Click(models.Model):
    event = models.IntegerField()
    teacher = models.IntegerField()

class Account(models.Model):
    client = models.ForeignKey(Client)
    good_standing = models.BooleanField(default = True)
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')


class Receipt(models.Model):
    account = models.ForeignKey(Account)
    event = models.ForeignKey(Event)
    teacher = models.ForeignKey(Teacher)
    hours = models.FloatField()
    rate = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    admin_email = models.EmailField()
    admin_percentage = models.FloatField()
    tax_percentage = models.FloatField()
    tax = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    total = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    teacher_part = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    admin_part = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    date_due = models.DateField()








