from django.contrib import admin

from .models import Board, Comments


# Register your models here.
# @admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id','title','user','date')
    search_fields = ('title','content','user__username')

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('board_comment','user_comment','date_comment')
    search_fields = ('content_comment','user_comment__username','board_comment__title')


admin.site.register(Board, BoardAdmin)