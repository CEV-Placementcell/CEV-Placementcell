from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect,FileResponse
from django.urls import reverse
from django.contrib import messages
from registration.models import *
from .models import *
import datetime
from exam import forms as QFORM
from exam import models as QMODEL
from registration import models as SMODEL

# Create your views here.

def techlogin(request):
    if request.method=="POST":
        try:
            ad_no= request.POST['admission_no']
            password= request.POST['password']
            u=student.objects.get(ad_no=ad_no,password=password)
            if (u.tech_mem is True):
                request.session['ad_no']=u.ad_no
                return redirect('techinterface')
            else:
                messages.info(request,"Not a Tech member")
                return redirect('techlogin')

        except student.DoesNotExist as e:
            messages.info(request,"Invalid Admission number or password")
            return redirect('techlogin')

    return render(request,'techlog.html')

def techlogout(request):
    if 'ad_no' in request.session:
        request.session.flush()
    return redirect(techlogin)


def techinterface(request):
    if 'ad_no' in request.session :
        return render(request,'techinter.html')
    return redirect(techlogin)
    

def drivecontent(request):
    if 'ad_no' in request.session :
        if request.method=="POST":
            d_no = request.POST['drivenumber']
            j_pos = request.POST['jobposition']
            c_name = request.POST['companyname']
            l_date = request.POST['lastdate']
            j_dis = request.POST['jobdescription']
            req_s = request.POST['requiredskill']
            qual = request.POST['qualification']
            sal = request.POST['salary']
            link = request.POST['link']
            program=request.POST['program']

            j = job(d_no=d_no,j_pos=j_pos,c_name=c_name,l_date=l_date,
            j_dis=j_dis,req_s=req_s,qual=qual,sal=sal,link=link,program=program)

            j.save()

        jobs = job.objects.order_by("-d_no").all()
        try:
            driveno=int(jobs[0].d_no)+1
        except IndexError:
            driveno=1
        return render(request,'drive-content.html',{'jobs':jobs,'driveno':driveno})
    return redirect(techlogin)


def eventcontent(request):
  if 'ad_no' in request.session :  
    if request.method=="POST":
        e_id = request.POST['eventid']
        e_name = request.POST['eventname']
        date = request.POST['eventdate']
        time = request.POST['time']
        l_date = request.POST['lastdate']
        venue = request.POST['Venue']
        fee = request.POST['Fee']

        e = event(e_id=e_id,e_name=e_name,date=date,time=time,l_date=l_date,venue=venue,fee=fee)
        e.save()
    
    events = event.objects.order_by("-e_id").all()
    try:
        eno=int(events[0].e_id)+1
    except IndexError:
        eno=1
    return render(request,'event-content.html',{'events':events,"eno":eno})
  return redirect(techlogin)


def posterupload(request):
  if 'ad_no' in request.session : 
    if request.method=="POST":
        try:
            d_no = request.POST['d_no']
            poster = request.FILES['poster']

            jobs=job.objects.get(d_no=d_no,poster='NULL')
            jobs.poster = poster
            jobs.save()
        except job.DoesNotExist as e:
            messages.info(request,"Invalid drive number or poster already uploaded")


    posteruploaded=job.objects.order_by("-d_no").exclude(poster='NULL')

    return render(request,'postersupload.html',{"posteruploaded":posteruploaded})
  return redirect(techlogin)


def notificationupload(request):
    if 'ad_no' in request.session :  
     if request.method=="POST":
        date = datetime.date.today()
        notify = request.POST['notification']

        n= notification(date=date,notify=notify)
        n.save()
     note = notification.objects.all()
     return render(request,'technotiupload.html',{"note":note})
    return redirect(techlogin)
def notificationdelete(request,id):
   if 'ad_no' in request.session :  
    n = notification.objects.get(id=id)
    n.delete()
    return HttpResponseRedirect(reverse('notificationupload'))
   return redirect(techlogin)


def techsupport(request):
 if 'ad_no' in request.session :  
    doubt = query.objects.filter(d_replay='NOT RESPONDED')
    stud=student.objects.all()
    return render(request,'techsupport.html',{"doubt":doubt,"stud":stud})
 return redirect(techlogin)

def tsupportmoreinfo(request,id,dno):
 if 'ad_no' in request.session :   
  
    stud=student.objects.get(ad_no=id)
    doubt=query.objects.get(d_no_id=dno,ad_no_id=id)
    if request.method=="POST":
         d_replay=request.POST['replay']
         doubt.d_replay=d_replay
         doubt.save()
    return render(request,'trytechsupp.html',{"doubt":doubt,"stud":stud})
 return redirect(techlogin)



def techmoreinfo(request,id):
   if 'ad_no' in request.session : 
    info=job.objects.get(d_no=id)
    return render(request,'techmoreinfo.html',{"info":info})
   return redirect(techlogin)

def posterview(request,dno):
    if 'ad_no' in request.session :
        livedrives=job.objects.get(d_no=dno)
        if livedrives.poster == "NULL":
            messages.info(request,"No Poster Uploaded")
            return redirect('techmoreinfo',dno)
        else:
            posterpath=livedrives.poster.path
            return FileResponse(open(posterpath,'rb'))



def teacher_dashboard_view(request):
    dict = {
        'total_student': SMODEL.student.objects.all().count(),
        'total_course': QMODEL.Course.objects.all().count(),
        'total_question': QMODEL.Question.objects.all().count(),
    }
    return render(request, 'teacher/teacher_dashboard.html', context=dict)

def teacher_view_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request,'teacher/teacher_view_exam.html',{'courses':courses})

def teacher_exam_view(request):
    return render(request,'teacher/teacher_exam.html')

def teacher_add_exam_view(request):
    courseForm=QFORM.CourseForm()
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('teacher-view-exam')
    return render(request,'teacher/teacher_add_exam.html',{'courseForm':courseForm})




def delete_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher-view-exam')


def teacher_question_view(request):
    return render(request,'teacher/teacher_question.html')


def teacher_add_question_view(request):
    questionForm=QFORM.QuestionForm()
    if request.method=='POST':
        questionForm=QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=QMODEL.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('teacher-view-question')
    return render(request,'teacher/teacher_add_question.html',{'questionForm':questionForm})


def teacher_view_question_view(request):
    courses= QMODEL.Course.objects.all()
    return render(request,'teacher/teacher_view_question.html',{'courses':courses})


def see_question_view(request,pk):
    questions=QMODEL.Question.objects.all().filter(course_id=pk)
    return render(request,'teacher/see_question.html',{'questions':questions})

def teacher_update_course_view(request, course_id):
    course = get_object_or_404(QMODEL.Course, id=course_id)
    courseForm = QFORM.CourseForm(instance=course)
    if request.method == 'POST':
        courseForm = QFORM.CourseForm(
            request.POST, request.FILES, instance=course)
        if courseForm.is_valid():
            courseForm.save()
            return HttpResponseRedirect('/teacher-view-exam')
    return render(request, 'teacher/teacher_update_course.html', {'courseForm': courseForm})

def remove_question_view(request,pk):
    question=QMODEL.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher-view-question')
