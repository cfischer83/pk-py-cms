import os
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from PIL import Image


def media_upload_path(instance, filename):
    """Generate upload path for media files."""
    # Get file extension
    ext = filename.split('.')[-1].lower()
    
    # Generate safe filename
    name = slugify(os.path.splitext(filename)[0])
    
    # Organize by type
    if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']:
        folder = 'images'
    elif ext in ['mp4', 'webm', 'mov', 'avi']:
        folder = 'videos'
    elif ext in ['mp3', 'wav', 'ogg']:
        folder = 'audio'
    elif ext in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']:
        folder = 'documents'
    else:
        folder = 'files'
    
    return f'{folder}/{name}.{ext}'


class Media(models.Model):
    """Media library model for storing uploaded files."""
    
    class MediaType(models.TextChoices):
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'
        AUDIO = 'audio', 'Audio'
        DOCUMENT = 'document', 'Document'
        OTHER = 'other', 'Other'
    
    # File information
    file = models.FileField(upload_to=media_upload_path)
    title = models.CharField(max_length=255)
    alt_text = models.CharField(
        max_length=255, 
        blank=True,
        help_text='Alternative text for accessibility (images)'
    )
    caption = models.TextField(blank=True)
    
    # Type and metadata
    media_type = models.CharField(
        max_length=20,
        choices=MediaType.choices,
        default=MediaType.OTHER
    )
    mime_type = models.CharField(max_length=100, blank=True)
    file_size = models.PositiveIntegerField(default=0, help_text='File size in bytes')
    
    # Image dimensions (for images only)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    
    # Ownership and timestamps
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_media'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'media'
        verbose_name_plural = 'media'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-set title from filename if not provided
        if not self.title and self.file:
            self.title = os.path.splitext(os.path.basename(self.file.name))[0]
        
        # Determine media type from file extension
        if self.file:
            ext = self.file.name.split('.')[-1].lower()
            
            if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']:
                self.media_type = self.MediaType.IMAGE
            elif ext in ['mp4', 'webm', 'mov', 'avi']:
                self.media_type = self.MediaType.VIDEO
            elif ext in ['mp3', 'wav', 'ogg']:
                self.media_type = self.MediaType.AUDIO
            elif ext in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']:
                self.media_type = self.MediaType.DOCUMENT
            else:
                self.media_type = self.MediaType.OTHER
        
        super().save(*args, **kwargs)
        
        # Get image dimensions after save
        if self.media_type == self.MediaType.IMAGE and self.file:
            try:
                with Image.open(self.file.path) as img:
                    self.width, self.height = img.size
                    # Update without triggering save() again
                    Media.objects.filter(pk=self.pk).update(
                        width=self.width,
                        height=self.height
                    )
            except Exception:
                pass
    
    @property
    def url(self):
        """Return the file URL."""
        return self.file.url if self.file else ''
    
    @property
    def filename(self):
        """Return the filename."""
        return os.path.basename(self.file.name) if self.file else ''
    
    @property
    def extension(self):
        """Return the file extension."""
        return self.file.name.split('.')[-1].lower() if self.file else ''
    
    @property
    def is_image(self):
        return self.media_type == self.MediaType.IMAGE
    
    def get_size_display(self):
        """Return human-readable file size."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f'{size:.1f} {unit}'
            size /= 1024
        return f'{size:.1f} TB'
