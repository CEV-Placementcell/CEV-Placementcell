from django.db import models
from registration.models import student


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    question_number = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    time = models.PositiveIntegerField()
    solution = models.FileField(upload_to='solution', null=True, blank=True)
    status = models.BooleanField(default=False)
    qprint = models.PositiveIntegerField()
    
    def __str__(self):
        return self.course_name


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    question = models.CharField(max_length=600)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    cat = (('Option1', 'Option1'), ('Option2', 'Option2'),
           ('Option3', 'Option3'), ('Option4', 'Option4'))
    answer = models.CharField(max_length=200, choices=cat)


class Result(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
