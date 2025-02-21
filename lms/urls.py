from django.db import router
from django.urls import path
from lms.apps import LmsConfig
from rest_framework.routers import DefaultRouter

from lms.views import CourseViewSet, LessonCreateApi, LessonDestroyApi, LessonListApi, LessonRetrieveApi, LessonUpdateApi

app_name = LmsConfig.name
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create/', LessonCreateApi.as_view(), name='lesson_create'),
    path('lesson/', LessonListApi.as_view(), name='lessons'),
    path('lesson/<int:pk>', LessonRetrieveApi.as_view(), name='lesson'),
    path('lesson/update/<int:pk>', LessonUpdateApi.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>', LessonDestroyApi.as_view(), name='lesson_delete'),
] + router.urls