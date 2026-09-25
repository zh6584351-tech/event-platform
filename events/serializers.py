from rest_framework import serializers
from .models import Event, Review, Registration, Category

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('current_participants', 'created_at', 'organizer')

    def validate(self, data):
        """Валідація часу події"""
        if data.get('start_time') and data.get('end_time'):
            if data['start_time'] >= data['end_time']:
                raise serializers.ValidationError("Час завершення події має бути пізніше за час її початку.")
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ('user', 'registered_at')

    def validate(self, data):
        # Перевірка наявності вільних місць та повторної реєстрації
        event = data.get('event')
        user = self.context['request'].user

        if event.is_full:
            raise serializers.ValidationError("Вільні місця відсутні.")

        if Registration.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError("Ви вже зареєстровані на цю подію.")

        return data