from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField('Название', max_length=50)
    preview = models.ImageField('Превью', upload_to='lms/photo', blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

class Lesson(models.Model):
    name = models.CharField('Название', max_length=50)
    description = models.TextField('Описание', blank=True, null=True)
    preview = models.ImageField('Превью', upload_to='lms/photo', blank=True, null=True)
    video = models.URLField('Ссылка на видео', max_length=100, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
    