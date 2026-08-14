from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from study.models import Subject,Task,Routine
from study.serializer import SubjectSerializer, TaskSerializer,RoutineSerializer

class SubjectListView(ListCreateAPIView):

    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskListView(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(subject__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

class TaskDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            subject__user=self.request.user
        )
class RoutineListView(ListCreateAPIView):

    serializer_class = RoutineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Routine.objects.filter(
            subject__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save()   

class RoutineDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = RoutineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Routine.objects.filter(
            subject__user=self.request.user
        )      




from django.shortcuts import render

def subjects_page(request):
    subjects = Subject.objects.filter(
        user=request.user
    )

    return render(
        request,
        "study/subjects.html",
        {"subjects": subjects}
    )