from django.contrib import admin

from .models import Board, Comments, Image


# Register your models here.
class ImageInline(admin.TabularInline):
    model = Image

# @admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id','title','user','date')
    search_fields = ('title','content','user__username')
    inlines = [ImageInline,]

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('board_comment','user_comment','date_comment')
    search_fields = ('content_comment','user_comment__username','board_comment__title')


admin.site.register(Board, BoardAdmin)