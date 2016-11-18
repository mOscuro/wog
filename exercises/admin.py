from django.contrib import admin
from exercises.models import Exercise, Equipment, Muscle

# Register your models here.
admin.site.register(Exercise)
admin.site.register(Equipment)
admin.site.register(Muscle)