from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventDetailView, CategoryViewSet, RegistrationViewSet, ReviewViewSet, event_list_view, event_create_view, register_to_event, profile_view
from django.contrib.auth.views import LoginView

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'registrations', RegistrationViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', event_list_view, name='event-list'),
    path('create/', event_create_view, name='event-create'),
    path('accounts/login/', LoginView.as_view(template_name='events/login.html'), name='login'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:pk>/register/', register_to_event, name='event-register'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('profile/', profile_view, name='profile'),
]