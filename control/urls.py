from django.urls import path
from .import views
urlpatterns = [
     path('admininter',views.admininter,name='admininter'),
     path('adminlogin',views.adminlogin,name='adminlogin'),
     path('adminlogout',views.adminlogout,name='adminlogout'),
     path('addrive',views.addrive,name='addrive'),
     path('drivecontentadm',views.drivecontentadm,name='drivecontentadm'),
     path('eventcontentadm',views.eventcontentadm,name='eventcontentadm'),
     path('posteruploadadm',views.posteruploadadm,name='posteruploadadm'),
     path('moreinfo/<str:id>',views.moreinfo,name='moreinfo'),
     path('adminposterview/<str:dno>',views.adminposterview,name='adminposterview'),
     path('studinfo/<str:id>',views.studinfo,name='studinfo'),
     path('totalplacements',views.totalplacements,name='totalplacements'),
     path('placedreport/<str:dno>',views.placedreport,name='placedreport'),
     path('regstudents',views.regstudents,name='regstudents'),
     path('pendingtask',views.pendingtask,name='pendingtask'),
     path('ongoingdrive',views.ongoingdrive,name='ongoingdrive'),
     path('ongoingreport/<str:dno>',views.ongoingreport,name='ongoingreport'),
     path('excelview/<str:dno>',views.excelview,name='excelview'),
     path('regstudentsexcelview',views.regstudentsexcelview,name='regstudentsexcelview'),
     path('placedexcelview/<str:dno>',views.placedexcelview,name='placedexcelview'),
     path('techteam',views.techteam,name='techteam'),
     path('selectech/<str:id>',views.selectech,name='selectech'),
     path('deletetech/<str:id>',views.deletetech,name='deletetech'),
     path('adminnotification',views.adminnotification,name='adminnotification'),
     path('notificationdeleteadmin/<str:id>',views.notificationdeleteadmin,name='notificationdeleteadmin'),
     path('eventslist',views.eventslist,name='eventslist'),
     path('eventreport/<str:eid>',views.eventreport,name='eventreport'),
     path('eventexcelview/<str:eid>',views.eventexcelview,name='eventexcelview'),
     # path('placed/<str:ad_no>/<int:d_no>/', views.placed, name='placed'),



]
 