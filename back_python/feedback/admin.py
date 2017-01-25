from django.contrib import admin

# Register your models here.
from feedback.models import *
from org.models import Profile
# Register your models here.
class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 0

class FeedBackAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(FeedBack)
admin.site.register(Post)
admin.site.register(Comment)
