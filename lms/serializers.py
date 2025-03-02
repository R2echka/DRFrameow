from rest_framework import serializers

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, instance):
        return instance.lessons.all().count()

    def create(self, validated_data):
        lessons = validated_data.pop("lessons")
        new_course = Course.objects.create(**validated_data)
        for lesson in lessons:
            Lesson.objects.create(**lesson, course=new_course)
        return new_course
