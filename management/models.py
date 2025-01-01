from django.db import models
from registration.models import *

# Create your models here.


class job(models.Model):
    d_no = models.IntegerField(primary_key=True)
    j_pos = models.CharField(max_length=50)
    c_name = models.CharField(max_length=50)
    l_date = models.CharField(max_length=20)
    j_dis = models.CharField(max_length=2500)
    req_s = models.CharField(max_length=500)
    qual = models.CharField(max_length=100)
    sal = models.CharField(max_length=50)
    link = models.CharField(max_length=100)
    poster = models.FileField(default='NULL',upload_to="poster")
    program = models.CharField(max_length=5)


    def __str__(self):
        return self.d_no

class event(models.Model):
    e_id=models.CharField(max_length=50,primary_key=True)
    e_name = models.CharField(max_length=50)
    date= models.DateField()
    time = models.TimeField()
    l_date = models.DateField()
    venue = models.CharField(max_length=100)
    fee = models.IntegerField(default='NULL')

    def __str__(self):
        return self.e_name


class notification(models.Model):
    date = models.DateField()
    notify = models.CharField(max_length=500)

    def __str__(self):
        return self.e_name