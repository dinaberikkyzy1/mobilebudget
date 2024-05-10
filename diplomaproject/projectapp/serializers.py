from rest_framework import serializers
from .models import Question, UserResponse

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'ans', ]
        depth = 2

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ['id', 'question', 'user', 'response']
        