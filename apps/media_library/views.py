from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Media
from .forms import MediaUploadForm


class MediaListView(LoginRequiredMixin, ListView):
    """List all media files."""
    model = Media
    template_name = 'media_library/media_list.html'
    context_object_name = 'media_items'
    paginate_by = 24
    
    def get_queryset(self):
        queryset = Media.objects.all()
        
        # Filter by media type
        media_type = self.request.GET.get('type')
        if media_type:
            queryset = queryset.filter(media_type=media_type)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        return queryset.select_related('uploaded_by')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_types'] = Media.MediaType.choices
        context['current_type'] = self.request.GET.get('type', '')
        context['search'] = self.request.GET.get('search', '')
        return context


class MediaDetailView(LoginRequiredMixin, DetailView):
    """Display media details."""
    model = Media
    template_name = 'media_library/media_detail.html'
    context_object_name = 'media'


class MediaUploadView(LoginRequiredMixin, CreateView):
    """Upload new media."""
    model = Media
    form_class = MediaUploadForm
    template_name = 'media_library/media_upload.html'
    success_url = reverse_lazy('media_library:media_list')
    
    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        form.instance.file_size = form.cleaned_data['file'].size
        messages.success(self.request, 'Media uploaded successfully!')
        return super().form_valid(form)


class MediaDeleteView(LoginRequiredMixin, DeleteView):
    """Delete media."""
    model = Media
    template_name = 'media_library/media_confirm_delete.html'
    success_url = reverse_lazy('media_library:media_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Media deleted successfully!')
        return super().delete(request, *args, **kwargs)
