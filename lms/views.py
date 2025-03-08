from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.paginators import CustomPaginator
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import Moderator, Owner


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = CustomPaginator
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
    pagination_class = CustomPaginator

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


class SubView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        course = get_object_or_404(Course, pk=self.request.data.get('course_id'))

        subs_item = Subscription.objects.filter(user=user, course=course).first()

        if subs_item:
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'подписка добавлена'
        return Response({"message": message})