from django.shortcuts import render,redirect
from django.contrib import messages
from registration.models import *
from management.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.http import FileResponse
from django.urls import reverse
import datetime , csv



def adminlogin(request):
    if request.method=="POST":
            user_name= request.POST['Username']
            pass_word= request.POST['Password']
            if (user_name=="Admin" and pass_word=="Admin"):
                request.session['admin']=user_name
                return redirect('admininter')
            else:
                messages.info(request,"Invalid Username or password")
                return redirect('adminlogin')
    return render(request,'admlog.html')

def adminlogout(request):
    if 'admin' in request.session:
        request.session.flush()
    return redirect(adminlogin)

def admininter(request):
    if 'admin' in request.session:
        tot_drive=job.objects.all().count()
        tot_stud=student.objects.all().count()
        tot_pending=job.objects.filter(poster='NULL').count()
        placement=placements.objects.all().count()

        return render(request,'admininter.html',{"tot_drive":tot_drive,"tot_stud":tot_stud,"tot_pending":tot_pending,"placement":placement})
    return redirect(adminlogin)


def addrive(request):
    if 'admin' in request.session:
        jobs=job.objects.order_by("-d_no").all()
        return render(request,'addrive.html',{"jobs":jobs})
    return redirect(adminlogin)


def moreinfo(request,id):
    if 'admin' in request.session:
      info=job.objects.get(d_no=id)
      return render(request,'moreinfo.html',{"info":info})
    return redirect(adminlogin)

def adminposterview(request,dno):
    if 'admin' in request.session:
        livedrives=job.objects.get(d_no=dno)
        if livedrives.poster == "NULL":
            messages.info(request,"No Poster Uploaded")
            return redirect('moreinfo',dno)
        else:
            posterpath=livedrives.poster.path
            return FileResponse(open(posterpath,'rb'))

def drivecontentadm(request):
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
        return render(request,'drive-contentadm.html',{'jobs':jobs,'driveno':driveno})
    return redirect(adminlogin)

# def placed(request,id,dno):
#     if 'ad_no' in request.session and request.session['ad_no']==id :
#         stud=student.objects.get(ad_no=id)
#         jobs=job.objects.get(d_no=dno)
#         if request.method=="POST":
#             ad_no= request.POST['adno']
#             d_no= request.POST['dno']
#             offletter= request.FILES['offlett']
#             sal= request.POST['sal']
#             p=placements(ad_no_id=ad_no,d_no_id=d_no,offletter=offletter,sal=sal)
#             p.save()
        

#         return render(request,'Placed.html',{"stud":stud,"jobs":jobs})
#     return redirect(adminlogin)


def eventcontentadm(request):
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
    return render(request,'event-contentadm.html',{'events':events,"eno":eno})
  return redirect(adminlogin)


def posteruploadadm(request):
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

    return render(request,'postersuploadadm.html',{"posteruploaded":posteruploaded})
  return redirect(adminlogin)


def totalplacements(request):
    if 'admin' in request.session:
      placement=placements.objects.all()
      info=job.objects.order_by("-d_no").exclude(poster='NULL')
      details = []
      for j in info:
          row = {
              "d_no" : j.d_no,
              "l_date" : j.l_date,
              "c_name" : j.c_name
          }
          count = 0
          for aj in placement:
              if aj.d_no_id == j.d_no:
                  count+=1
          row['count'] = count
          details.append(row)
      return render(request,'adminplacements.html',{"placement":placement,"info":info,"details":details})
    return redirect(adminlogin)


def placedreport(request,dno):
    if 'admin' in request.session:
        stud=student.objects.order_by("dept").all()
        jobs=job.objects.get(d_no=dno)
        placed=placements.objects.filter(d_no=dno)
        return render(request,'ApplicantReport.html',{"stud":stud,"jobs":jobs,"placed":placed})
    return redirect(adminlogin)

# excel download function
def placedexcelview(request,dno):
    stud=student.objects.order_by("dept").all()
    jobs=job.objects.get(d_no=dno)
    placed=placements.objects.filter(d_no=dno)
    response= HttpResponse(
            content_type="text/csv",
            headers={"content-Disposition": 'attachment; filename="placedstudents.csv"'},
        )

    writer = csv.writer(response)
    writer.writerow(["Placed Students Drive No"+str(dno)+" Company "+str(jobs.c_name)])
    writer.writerow(["Admission No","Register Number","Name","Department","Program","Number","E-mail"])
    for s in stud:
        for p in  placed:
            if s.ad_no == p.ad_no_id:
                writer.writerow([s.ad_no,s.regno,s.name,s.dept,s.prog,s.stud_ph,s.contact.email])

    return response

def regstudents(request):
    if 'admin' in request.session:
      stud=student.objects.order_by("dept").all()
      return render(request,'adminregstudents.html',{"stud":stud})
    return redirect(adminlogin)

def regstudentsexcelview(request):
    stud=student.objects.order_by("dept").all()
    response= HttpResponse(
            content_type="text/csv",
            headers={"content-Disposition": 'attachment; filename="registredstudents.csv"'},
        )

    writer = csv.writer(response)
    writer.writerow(["Regitered Students"])
    writer.writerow(["Admission Number","Register Number","Name","Department","Program","Phone Number","E-mail"])
    for s in stud:
        writer.writerow([s.ad_no,s.regno,s.name,s.dept,s.prog,s.stud_ph,s.contact.email])

    return response

def studinfo(request,id):
    stud=student.objects.get(ad_no=id)
    email=contact.objects.get(ad_no=id)
    jobinfo=job.objects.all()
    appliedjob=placements.objects.filter(ad_no=id)
    return render(request,'adminregstudapplicantprofile.html',{"stud":stud,"email":email,"jobinfo":jobinfo,"appliedjob":appliedjob})



def pendingtask(request):
    if 'admin' in request.session:
       return render(request,'adminpendingtask.html')
    return redirect(adminlogin)

def ongoingdrive(request):
    if 'admin' in request.session:
      jobs=job.objects.order_by("-d_no").exclude(poster='NULL')
      stud=student.objects.all()
      tot_applicant=jobs_applied.objects.all()
      details = []
      for j in jobs:
          row = {
              "d_no" : j.d_no,
              "l_date" : j.l_date,
              "c_name" : j.c_name
          }
          count = 0
          for aj in tot_applicant:
              if aj.d_no_id == j.d_no:
                  count+=1
          row['count'] = count
          details.append(row)
      return render(request,'adminongoingdrives.html',{"jobs":jobs,"stud":stud,"tot_applicant":tot_applicant,"details":details})
    return redirect(adminlogin)

def ongoingreport(request,dno):
    if 'admin' in request.session:
      stud=student.objects.all()
      jobs=job.objects.get(d_no=dno)
      applied=jobs_applied.objects.filter(d_no=dno)
      return render(request,'ongoingreport.html',{"stud":stud,"jobs":jobs,"applied":applied})
    return redirect(adminlogin)

def excelview(request,dno):
    stud=student.objects.all()
    jobs=job.objects.get(d_no=dno)
    applied=jobs_applied.objects.filter(d_no=dno)
    response= HttpResponse(
            content_type="text/csv",
            headers={"content-Disposition": 'attachment; filename="ongoing.csv"'},
        )

    writer = csv.writer(response)
    writer.writerow(["Drive number :"+str(jobs.d_no)])
    writer.writerow(["Admission","Register Number","Name","Department","Number","E-mail"])
    for a in applied:
        for s in stud:
            if s.ad_no == a.ad_no_id:
                writer.writerow([s.ad_no,s.regno,s.name,s.dept,s.stud_ph,s.contact.email])

    return response




def techteam(request):
    if 'admin' in request.session:
       stud=student.objects.order_by("dept").filter(tech_mem=False)
       tech=student.objects.filter(tech_mem=True)
       return render(request,'Admintechteam.html',{'stud':stud,'tech':tech})
    return redirect(adminlogin)

def selectech(request,id):
    stud=student.objects.get(ad_no=id)
    stud.tech_mem=True
    stud.save()
    return  HttpResponseRedirect(reverse('techteam'))

def deletetech(request,id):
    stud=student.objects.get(ad_no=id)
    stud.tech_mem=False
    stud.save()
    return  HttpResponseRedirect(reverse('techteam'))


def adminnotification(request):
    if 'admin' in request.session:
        if request.method=="POST":
           date = datetime.date.today()
           notify = request.POST['notification']

           n= notification(date=date,notify=notify)
           n.save()

        note = notification.objects.order_by("-date").all()
        return render(request,'admintechnotification.html',{"note":note})
    return redirect(adminlogin)

def notificationdeleteadmin(request,id):
    if 'admin' in request.session:
        n = notification.objects.get(id=id)
        n.delete()
        return HttpResponseRedirect(reverse('adminnotification'))
    return redirect(adminlogin)
    
    

def eventslist(request):
    if 'admin' in request.session:
        events=event.objects.all()
        stud=student.objects.all()
        tot_applicant=events_applied.objects.all()
        details = []
        for j in events:
            row = {
                "e_id" : j.e_id,
                "l_date" : j.l_date,
                "e_name" : j.e_name
            }
            count = 0
            for aj in tot_applicant:
                if aj.e_id_id == j.e_id:
                    count+=1
            row['count'] = count
            details.append(row)
        return render(request,'eventongoing.html',{"events":events,"stud":stud,"tot_applicant":tot_applicant,"details":details})
    return redirect(adminlogin)
    

def eventreport(request,eid):
    if 'admin' in request.session:
      stud=student.objects.all()
      events=event.objects.get(e_id=eid)
      applied=events_applied.objects.filter(e_id=eid)
      return render(request,'eventreport.html',{"stud":stud,"events":events,"applied":applied})
    return redirect(adminlogin)

def eventexcelview(request,eid):
    stud=student.objects.all()
    events=event.objects.get(e_id=eid)
    applied=events_applied.objects.filter(e_id=eid)
    response= HttpResponse(
            content_type="text/csv",
            headers={"content-Disposition": 'attachment; filename="eventregistration.csv"'},
        )

    writer = csv.writer(response)
    writer.writerow([str(events.e_name)+" Registration"])
    writer.writerow(["Admission No","Register Number","Name","Department","Program","Number","E-mail"])
    for s in stud:
        for a in  applied:
            if s.ad_no == a.ad_no_id :
                writer.writerow([s.ad_no,s.regno,s.name,s.dept,s.prog,s.stud_ph,s.contact.email])

    return response