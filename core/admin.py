from django.contrib import admin
from .models import Profile, SkillOffered, SkillWanted, SwapRequest, Feedback

# Register your models here.
admin.site.register(Profile)
admin.site.register(SkillOffered)
admin.site.register(SkillWanted)
admin.site.register(SwapRequest)
admin.site.register(Feedback)
