from django.contrib import admin
from .models import TiktokHashtagsORM
from .models import TiktokSongsORM
from .models import TiktokBreakoutSongsORM

@admin.register(TiktokHashtagsORM)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at') 
    list_filter = ('id', 'created_at', 'updated_at') 
    search_fields = ('name', 'value') 
    ordering = ('-created_at',) 

@admin.register(TiktokSongsORM)
class SongAdmin(admin.ModelAdmin):
    list_display = ('name',  'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'author')
    search_fields = ('name', 'author')
    ordering = ('-created_at',)

@admin.register(TiktokBreakoutSongsORM)
class BreakoutSongAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'author') 
    search_fields = ('name', 'author')
    ordering = ('-created_at',)