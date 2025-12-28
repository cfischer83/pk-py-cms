from django.contrib import admin
from .models import Media


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'filename', 'uploaded_by', 'created_at')
    list_filter = ('media_type', 'created_at', 'uploaded_by')
    search_fields = ('title', 'alt_text', 'caption')
    readonly_fields = ('media_type', 'mime_type', 'file_size', 'width', 'height', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('file', 'title', 'alt_text', 'caption')
        }),
        ('File Information', {
            'fields': ('media_type', 'mime_type', 'file_size', 'width', 'height'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        
        # Set file size
        if obj.file:
            obj.file_size = obj.file.size
        
        super().save_model(request, obj, form, change)
