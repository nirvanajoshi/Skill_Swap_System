from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Root: send logged-in users to the app hub; anonymous users are
    # then redirected to the login page by the view's login_required.
    path('', RedirectView.as_view(pattern_name='swap_request_list'), name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile_edit, name='profile_edit'),

    path('skill-offered/', views.skill_offered_list, name='skill_offered_list'),
    path('skill-offered/create/', views.skill_offered_create, name='skill_offered_create'),
    path('skill-offered/<int:pk>/update/', views.skill_offered_update, name='skill_offered_update'),
    path('skill-offered/<int:pk>/delete/', views.skill_offered_delete, name='skill_offered_delete'),

    path('skill-wanted/', views.skill_wanted_list, name='skill_wanted_list'),
    path('skill-wanted/create/', views.skill_wanted_create, name='skill_wanted_create'),
    path('skill-wanted/<int:pk>/update/', views.skill_wanted_update, name='skill_wanted_update'),
    path('skill-wanted/<int:pk>/delete/', views.skill_wanted_delete, name='skill_wanted_delete'),

    path('swap-request/', views.swap_request_list, name='swap_request_list'),
    path('swap-request/create/', views.swap_request_create, name='swap_request_create'),
    path('swap-request/<int:pk>/accept/', views.swap_request_accept, name='swap_request_accept'),
    path('swap-request/<int:pk>/decline/', views.swap_request_decline, name='swap_request_decline'),
    path('swap-request/<int:pk>/delete/', views.swap_request_delete, name='swap_request_delete'),

    path('feedback/<int:swap_request_id>/', views.feedback_create, name='feedback_create'),
]