from django.contrib import admin
from .models import Doctors, passhash, profile_background,patients, test

# Register your models here.
admin.site.register(Doctors)
admin.site.register(passhash)
admin.site.register(profile_background)
admin.site.register(patients)
admin.site.register(test)