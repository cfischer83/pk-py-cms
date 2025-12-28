from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager for the User model."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model with email as the username field and role-based permissions."""
    
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Administrator'
        EDITOR = 'editor', 'Editor'
        AUTHOR = 'author', 'Author'
        CONTRIBUTOR = 'contributor', 'Contributor'
    
    # Remove username field, use email instead
    username = None
    email = models.EmailField('email address', unique=True)
    
    # Role-based permissions
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CONTRIBUTOR,
        help_text='User role determines their permissions in the CMS.'
    )
    
    # Profile fields
    bio = models.TextField(blank=True, help_text='A short biography about the user.')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.get_full_name() or self.email
    
    def get_display_name(self):
        """Return the user's display name."""
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.email.split('@')[0]
    
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser
    
    @property
    def is_editor(self):
        return self.role in [self.Role.ADMIN, self.Role.EDITOR] or self.is_superuser
    
    @property
    def is_author(self):
        return self.role in [self.Role.ADMIN, self.Role.EDITOR, self.Role.AUTHOR] or self.is_superuser
    
    @property
    def is_contributor(self):
        return True  # All authenticated users can at least contribute
    
    def can_edit_content(self, content):
        """Check if user can edit a specific piece of content."""
        if self.is_editor:
            return True
        if self.is_author and content.author == self:
            return True
        return False
    
    def can_publish_content(self):
        """Check if user can publish content."""
        return self.is_editor
    
    def can_delete_content(self, content):
        """Check if user can delete a specific piece of content."""
        if self.is_admin:
            return True
        if self.is_editor:
            return True
        return False
