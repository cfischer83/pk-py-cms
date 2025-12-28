from django import forms
from django_quill.forms import QuillFormField
from .models import Post, Page, Category, Tag


class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts."""
    
    content = QuillFormField()
    
    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'excerpt', 'content',
            'featured_image', 'categories', 'tags',
            'status', 'published_at', 'allow_comments',
            'meta_title', 'meta_description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'published_at': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-input'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-input'}),
            'categories': forms.CheckboxSelectMultiple(),
            'tags': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        # Remove author from kwargs if passed
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Make slug optional for auto-generation
        self.fields['slug'].required = False
        
        # Limit status choices based on user role
        if self.user:
            if not self.user.is_editor:
                # Authors and Contributors can only save as Draft or Pending
                self.fields['status'].choices = [
                    (Post.Status.DRAFT, 'Draft'),
                    (Post.Status.PENDING, 'Pending Review'),
                ]
            
            if not self.user.is_author:
                # Contributors cannot publish
                self.fields['published_at'].disabled = True
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Set author to current user if creating new post
        if not instance.pk and self.user:
            instance.author = self.user
        
        if commit:
            instance.save()
            self.save_m2m()
        
        return instance


class PageForm(forms.ModelForm):
    """Form for creating and editing pages."""
    
    content = QuillFormField()
    
    class Meta:
        model = Page
        fields = [
            'title', 'slug', 'excerpt', 'content',
            'featured_image', 'template', 'parent',
            'show_in_menu', 'menu_order', 'status',
            'published_at', 'meta_title', 'meta_description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'published_at': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-input'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-input'}),
            'menu_order': forms.NumberInput(attrs={'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Make slug optional for auto-generation
        self.fields['slug'].required = False
        
        # Limit status choices based on user role
        if self.user:
            if not self.user.is_editor:
                self.fields['status'].choices = [
                    (Page.Status.DRAFT, 'Draft'),
                    (Page.Status.PENDING, 'Pending Review'),
                ]
            
            if not self.user.is_author:
                self.fields['published_at'].disabled = True
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Set author to current user if creating new page
        if not instance.pk and self.user:
            instance.author = self.user
        
        if commit:
            instance.save()
        
        return instance


class CategoryForm(forms.ModelForm):
    """Form for creating and editing categories."""
    
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False


class TagForm(forms.ModelForm):
    """Form for creating and editing tags."""
    
    class Meta:
        model = Tag
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
