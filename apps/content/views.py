from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Post, Page, Category, Tag


class PostListView(ListView):
    """List all published blog posts."""
    model = Post
    template_name = 'content/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(excerpt__icontains=search) |
                Q(content__icontains=search)
            )
        
        return queryset.select_related('author', 'featured_image').prefetch_related('categories', 'tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['search'] = self.request.GET.get('search', '')
        return context


class PostDetailView(DetailView):
    """Display a single blog post."""
    model = Post
    template_name = 'content/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        # Show drafts to authors/editors, published to everyone else
        if self.request.user.is_authenticated and self.request.user.is_editor:
            return Post.objects.all()
        return Post.objects.filter(status=Post.Status.PUBLISHED)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get related posts
        post = self.object
        related_posts = Post.objects.filter(
            status=Post.Status.PUBLISHED
        ).exclude(pk=post.pk)
        
        if post.categories.exists():
            related_posts = related_posts.filter(
                categories__in=post.categories.all()
            ).distinct()
        
        context['related_posts'] = related_posts[:3]
        return context


class PageDetailView(DetailView):
    """Display a static page."""
    model = Page
    context_object_name = 'page'
    
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_editor:
            return Page.objects.all()
        return Page.objects.filter(status=Page.Status.PUBLISHED)
    
    def get_template_names(self):
        """Return template based on page's template setting."""
        page = self.get_object()
        return [
            f'content/pages/{page.template}.html',
            'content/pages/default.html',
            'content/page_detail.html',
        ]


class CategoryDetailView(ListView):
    """List posts in a category."""
    template_name = 'content/category_detail.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            status=Post.Status.PUBLISHED,
            categories=self.category
        ).select_related('author', 'featured_image')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagDetailView(ListView):
    """List posts with a tag."""
    template_name = 'content/tag_detail.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(
            status=Post.Status.PUBLISHED,
            tags=self.tag
        ).select_related('author', 'featured_image')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context
