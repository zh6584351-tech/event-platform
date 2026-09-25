from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва категорії")
    description = models.TextField(blank=True, verbose_name="Опис")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва події")
    description = models.TextField(verbose_name="Опис")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='events', verbose_name="Категорія")
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events', verbose_name="Організатор")
    
    location = models.CharField(max_length=255, verbose_name="Місце проведення / Посилання")
    start_time = models.DateTimeField(verbose_name="Час початку")
    end_time = models.DateTimeField(verbose_name="Час завершення")
    
    max_participants = models.PositiveIntegerField(verbose_name="Максимальна кількість учасників")
    current_participants = models.PositiveIntegerField(default=0, verbose_name="Поточна кількість учасників")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return self.title

    @property
    def is_full(self):
        # Перевірка місць на подію
        return self.current_participants >= self.max_participants

    class Meta:
        verbose_name = "Подія"
        verbose_name_plural = "Події"
        ordering = ['start_time']


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations', verbose_name="Учасник")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations', verbose_name="Подія")
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата реєстрації")

    class Meta:
        unique_together = ('user', 'event')  # Щоб один користувач не міг зареєструватися на одну подію двічі
        verbose_name = "Реєстрація"
        verbose_name_plural = "Реєстрації"

    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"


class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews', verbose_name="Подія")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="Автор відгуку")
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Оцінка (1-5)")
    comment = models.TextField(verbose_name="Коментар")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"

    def __str__(self):
        return f"Відгук від {self.user.username} на {self.event.title}"