from django.urls import path
from profiles import views

urlpatterns = [
    path('profiles/register/', views.UserProfileView.as_view(),),
    path('profile/list/', views.UserProfileView.as_view(),),
    path('profiles/update/<int:id>/', views.ProfileView.as_view(),),
    path('profiles/delete/<int:id>/', views.ProfileView.as_view(),),
]