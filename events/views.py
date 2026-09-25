from rest_framework import viewsets, permissions
from .models import Event, Registration, Review, Category
from .serializers import EventSerializer, RegistrationSerializer, ReviewSerializer, CategorySerializer
from django.shortcuts import render

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Автоматичне призначення поточного користувача організатором
        serializer.save(organizer=self.request.user)


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Автоматичне прив'язування реєстрації до поточного користувача
        serializer.save(user=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

def event_list_view(request):
    events = Event.objects.all()  # Отримування події з бази даних
    return render(request, 'events/event_list.html', {'events': events})