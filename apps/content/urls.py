from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    # Blog posts
    path('blog/', views.PostListView.as_view(), name='post_list'),
    path('blog/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # Categories
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Tags
    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
    
    # Pages (catch-all for page slugs - should be last)
    path('page/<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
]
