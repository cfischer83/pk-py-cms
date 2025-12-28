from django.contrib import admin
from django_quill.widgets import QuillWidget
from .models import Category, Tag, Post, Page


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'created_at')
    list_filter = ('parent',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


class ContentBaseAdmin(admin.ModelAdmin):
    """Base admin class for content types."""
    list_display = ('title', 'author', 'status', 'published_at', 'created_at')
    list_filter = ('status', 'author', 'created_at')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Publishing', {
            'fields': ('author', 'status', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(ContentBaseAdmin):
    list_display = ('title', 'author', 'status', 'allow_comments', 'published_at', 'created_at')
    list_filter = ('status', 'author', 'categories', 'tags', 'allow_comments', 'created_at')
    filter_horizontal = ('categories', 'tags')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Organization', {
            'fields': ('categories', 'tags')
        }),
        ('Publishing', {
            'fields': ('author', 'status', 'published_at', 'allow_comments')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Page)
class PageAdmin(ContentBaseAdmin):
    list_display = ('title', 'template', 'parent', 'show_in_menu', 'menu_order', 'status', 'created_at')
    list_filter = ('status', 'template', 'show_in_menu', 'author', 'created_at')
    list_editable = ('menu_order', 'show_in_menu')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Page Settings', {
            'fields': ('template', 'parent')
        }),
        ('Menu Settings', {
            'fields': ('show_in_menu', 'menu_order')
        }),
        ('Publishing', {
            'fields': ('author', 'status', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
