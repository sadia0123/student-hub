from rest_framework import serializers
from .models import Subject, Task , Routine


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'teacher']

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'id',
            'subject',
            'title',
            'description',
            'deadline',
            'completed'
        ]        

class RoutineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Routine
        fields = [
            'id',
            'subject',
            'day',
            'start_time',
            'end_time',
            'room'
        ]