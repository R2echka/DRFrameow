from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import Moderator, Owner


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~Moderator,)
        elif self.action == "destroy":
            self.permission_classes = (~Moderator | Owner,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (Moderator | Owner,)
        return super().get_permissions()


class LessonCreateApi(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~Moderator, IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListApi(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonRetrieveApi(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [Moderator | Owner, IsAuthenticated]


class LessonUpdateApi(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [Moderator | Owner, IsAuthenticated]


class LessonDestroyApi(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [~Moderator | Owner, IsAuthenticated]
