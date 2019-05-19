from django.contrib import admin
from django.urls import reverse
from .models import Comment

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'content', 'website', 'created_time')