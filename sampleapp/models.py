from django.db import models


class Class(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey('sampleapp.Teacher', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'classes'

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=255)
    cclass = models.ForeignKey('sampleapp.Class', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
