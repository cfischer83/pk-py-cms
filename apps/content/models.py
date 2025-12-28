from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django_quill.fields import QuillField


class Category(models.Model):
    """Category model for organizing content."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='children'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('content:category_detail', kwargs={'slug': self.slug})


class Tag(models.Model):
    """Tag model for content tagging."""
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('content:tag_detail', kwargs={'slug': self.slug})


class ContentBase(models.Model):
    """Abstract base model for all content types."""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PENDING = 'pending', 'Pending Review'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    excerpt = models.TextField(
        blank=True, 
        help_text='A short summary of the content. Used in listings and SEO.'
    )
    content = QuillField()
    
    # Featured image
    featured_image = models.ForeignKey(
        'media_library.Media',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_featured'
    )
    
    # Author and status
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_posts'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    
    # SEO fields
    meta_title = models.CharField(
        max_length=70, 
        blank=True,
        help_text='SEO title (recommended: 50-60 characters)'
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text='SEO description (recommended: 150-160 characters)'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Set published_at when status changes to published
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def get_seo_title(self):
        """Return the SEO title or fall back to regular title."""
        return self.meta_title or self.title
    
    def get_seo_description(self):
        """Return the SEO description or fall back to excerpt."""
        return self.meta_description or self.excerpt[:160] if self.excerpt else ''
    
    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED


class Post(ContentBase):
    """Blog post model."""
    
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='posts'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts'
    )
    
    # Allow comments
    allow_comments = models.BooleanField(default=True)
    
    class Meta(ContentBase.Meta):
        verbose_name = 'post'
        verbose_name_plural = 'posts'
    
    def get_absolute_url(self):
        return reverse('content:post_detail', kwargs={'slug': self.slug})


class Page(ContentBase):
    """Static page model (like About, Contact, etc.)."""
    
    # Page template
    TEMPLATE_CHOICES = [
        ('default', 'Default'),
        ('full-width', 'Full Width'),
        ('sidebar-left', 'Sidebar Left'),
        ('sidebar-right', 'Sidebar Right'),
        ('landing', 'Landing Page'),
    ]
    template = models.CharField(
        max_length=50,
        choices=TEMPLATE_CHOICES,
        default='default'
    )
    
    # Page hierarchy
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )
    
    # Menu settings
    show_in_menu = models.BooleanField(
        default=False,
        help_text='Show this page in the main navigation menu'
    )
    menu_order = models.PositiveIntegerField(default=0)
    
    class Meta(ContentBase.Meta):
        verbose_name = 'page'
        verbose_name_plural = 'pages'
        ordering = ['menu_order', 'title']
    
    def get_absolute_url(self):
        return reverse('content:page_detail', kwargs={'slug': self.slug})
    
    def get_template_name(self):
        """Return the template file name based on template choice."""
        return f'pages/{self.template}.html'
