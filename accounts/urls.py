from django.urls import path, include
from .import views

app_name = 'accounts'
urlpatterns = [
  path('signup', views.signup, name='signup'),

  path('profile/<slug:slug>/', views.profile, name='profile'),
  path('profile/<slug:slug>/edit/', views.profile_edit, name='profile_edit'),
  path('product_favorite/<int:pro_id>', views.product_favorite, name='product_favorite')
]