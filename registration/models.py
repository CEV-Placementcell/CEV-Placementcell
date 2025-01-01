from django.db import models
from management.models import job,event
# Create your models here.

class student(models.Model):
    ad_no = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=50)
    dob = models.DateField()
    sslc = models.CharField(max_length=20)
    yo_add = models.IntegerField()
    dept = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    prog = models.CharField(max_length=50)
    photo=models.ImageField(default='NULL',upload_to="img")
    area_int = models.CharField(max_length=200)
    skill = models.CharField(max_length=200)
    stud_ph = models.CharField(max_length=20)
    password = models.CharField(default="NULL",max_length=20)
    tech_mem = models.BooleanField(default=False)
    aadhar = models.CharField(max_length=15)
    hsc = models.CharField(max_length=15)
    send= models.BooleanField(default=False)
    
    def __str__(self):
        return self.name



class contact(models.Model):
    ad_no= models.OneToOneField(student,on_delete=models.CASCADE)
    adr=models.CharField(max_length=200)
    st=models.CharField(max_length=20)
    dist=models.CharField(max_length=20)
    pin=models.IntegerField()
    email=models.EmailField()
    f_name = models.CharField(max_length=50)
    m_name = models.CharField(max_length=50)
    gua_ph = models.CharField(max_length=20)

    def __str__(self):
        return str(self.ad_no)



class events_applied(models.Model):
    e_id = models.ForeignKey(event,on_delete=models.CASCADE)
    ad_no = models.ForeignKey(student,on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return str(self.e_id)
    
class jobs_applied(models.Model):
    d_no= models.ForeignKey(job,on_delete=models.CASCADE)
    ad_no = models.ForeignKey(student,on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return str(self.d_no)
    

class query(models.Model):
    ad_no= models.ForeignKey(student,on_delete=models.CASCADE)
    d_no= models.ForeignKey(job,on_delete=models.CASCADE)
    d_title = models.CharField(max_length=50)
    d_descr = models.CharField(max_length=1000)
    d_ss = models.FileField(default='NULL',upload_to="screenshort")
    d_replay=models.CharField(default='NOT RESPONDED',max_length=750)
    
    def __str__(self):
        return self.d_title

class placements(models.Model):
    ad_no= models.ForeignKey(student,on_delete=models.CASCADE)
    d_no= models.ForeignKey(job,on_delete=models.CASCADE)
    # offletter=models.FileField(default='NULL',upload_to="offerletter")
    # sal = models.CharField(max_length=10)
    def __str__(self):
        return self.ad_no
    