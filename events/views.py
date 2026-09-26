from rest_framework import viewsets, permissions
from .models import Event, Registration, Review, Category
from django.contrib.auth.models import User
from .serializers import EventSerializer, RegistrationSerializer, ReviewSerializer, CategorySerializer
from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

def event_list_view(request):
    events = Event.objects.all()  # Отримування події з бази даних
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def event_create_view(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        category = Category.objects.filter(id=category_id).first() if category_id else None

        Event.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            category=category,
            organizer=request.user,
            location=request.POST.get('location'),
            start_time=request.POST.get('start_time') or None,
            end_time=request.POST.get('end_time') or None,
            max_participants=request.POST.get('max_participants') or 100
        )
        return redirect('event-list')

    categories = Category.objects.all()
    return render(request, 'events/event_form.html', {'categories': categories})

@login_required
def register_to_event(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    
    event = get_object_or_404(Event, pk=pk)
    
    # Використання серіалізатора для валідації та збереження
    serializer = RegistrationSerializer(
        data={'event': event.id}, 
        context={'request': request}
    )
    
    if serializer.is_valid():
        serializer.save(user=request.user, event=event)
        messages.success(request, "Реєстрація на подію пройшла успішно!")
    else:
        # Текст помилки
        error_msg = list(serializer.errors.values())[0][0]
        messages.error(request, error_msg)
        
    return redirect('event-detail', pk=event.pk)