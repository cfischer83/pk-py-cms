from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from apps.content.models import Post, Page


class HomeView(TemplateView):
    """Home page view."""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.filter(
            status=Post.Status.PUBLISHED
        ).select_related('author', 'featured_image')[:6]
        context['featured_pages'] = Page.objects.filter(
            status=Page.Status.PUBLISHED,
            show_in_menu=True
        )[:4]
        return context


class SearchView(ListView):
    """Search across all content."""
    template_name = 'core/search.html'
    context_object_name = 'results'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if not query:
            return Post.objects.none()
        
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query),
            status=Post.Status.PUBLISHED
        ).select_related('author')
        
        return posts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        
        # Also search pages
        query = self.request.GET.get('q', '')
        if query:
            context['pages'] = Page.objects.filter(
                Q(title__icontains=query) |
                Q(excerpt__icontains=query) |
                Q(content__icontains=query),
                status=Page.Status.PUBLISHED
            )[:5]
        
        return context
