from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
# User class contains username, password, email address, first name, last name
from django.template.defaultfilters import slugify


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

    def save(self, *args, **kwargs):
        self.client_slug = slugify(self.organization)
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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.get_full_name())
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

    def __unicode__(self):
        return str(self.start_time)


class Available_Time(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    teacher = models.ForeignKey(Teacher)


class Email_List(models.Model):
    email = models.EmailField()





