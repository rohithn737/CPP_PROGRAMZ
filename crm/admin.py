from django.contrib import admin

# Register your models here.

#After creating the models and migrate the model we need to update here
from .models import Thought, Profile

admin.site.register(Thought)
admin.site.register(Profile)