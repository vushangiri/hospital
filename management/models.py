from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.shortcuts import reverse
from autoslug import AutoSlugField




TYPE_SELECT = [
        ('female', 'Female'),
        ('male', 'Male')
]
STATUS_SELECT = [
        ('inactive', 'Inactive'),
        ('active', 'Active')
]


STATE=[
    ('01', '01'),
    ('02', '02'),
    ('03', '03'),
    ('04', '04'),
    ('05', '05'),
    ('06', '06'),
    ('07', '07')
]

# Create your models here.


class Doctors(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    dob = models.DateField()
    gender = models.CharField(max_length=20, choices=TYPE_SELECT)
    address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=10, choices=STATE)
    postalcode = models.IntegerField()
    phone = models.BigIntegerField()
    photo = models.ImageField(upload_to='pics', blank=True, null=True)
    bio = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_SELECT)
    expertise = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='username', unique=True)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse("management:profile", kwargs={
            'slug': self.slug
        })
    def get_url(self):
        return reverse("management:edit_profile", kwargs={
            'slug': self.slug
        })
    def get_remove_url(self):
        return reverse("management:remove_doctors", kwargs={
            'slug': self.slug
        })

class passhash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    salt = models.CharField(max_length=100)

class patients(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    dob = models.DateField()
    gender = models.CharField(max_length=20, choices=TYPE_SELECT)
    address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=10, choices=STATE)
    postalcode = models.IntegerField()
    phone = models.BigIntegerField()
    photo = models.ImageField(upload_to='pics')
    symptom = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from='username', unique=True)
    
    status = models.CharField(max_length=20, choices=STATUS_SELECT)
    def __str__(self):
        return self.first_name

    def get_remove_url(self):
        return reverse("management:remove_patients", kwargs={
            'slug': self.slug
        })
    def get_edit_url(self):
        return reverse("management:edit_patients", kwargs={
            'slug': self.slug
        })
class profile_background(models.Model):
    user = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    
    institution = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True, default='None')
    startingdate = models.DateField(blank=True, null=True)
    completedate = models.DateField(blank=True, null=True)
    degree = models.CharField(max_length=100, blank=True, null=True)
    grade = models.CharField(max_length=100, blank=True, null=True)
    companyname = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    jobposition = models.CharField(max_length=100, blank=True, null=True)
    periodfrom = models.DateField(blank=True, null=True)
    periodto = models.DateField(blank=True, null=True)

    def __str__(self):
        
        return self.subject


class verifycode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField(blank=True, null=True)
    verified = models.BooleanField(default=False)

