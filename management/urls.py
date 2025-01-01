from django.urls import path,include
from .import views

urlpatterns = [
    path('techlogin',views.techlogin,name='techlogin'),
    path('techlogout',views.techlogout,name='techlogout'),
    path('techinterface',views.techinterface,name='techinterface'),
    path('drivecontent',views.drivecontent,name='drivecontent'),
    path('eventcontent',views.eventcontent,name='eventcontent'),
    path('posterupload',views.posterupload,name='posterupload'),
    path('notificationupload',views.notificationupload,name='notificationupload'),
    path('notificationdelete/<str:id>',views.notificationdelete,name='notificationdelete'),
    path('techsupport',views.techsupport,name='techsupport'),
    path('techmoreinfo/<str:id>',views.techmoreinfo,name='techmoreinfo'),
    path('tsupportmoreinfo/<str:id>/<str:dno>',views.tsupportmoreinfo,name='tsupportmoreinfo'),
    path('posterview/<str:dno>',views.posterview,name='posterview'),
    path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
    path('teacher-exam', views.teacher_exam_view,name='teacher-exam'),
    path('teacher-view-exam', views.teacher_view_exam_view,name='teacher-view-exam'),
    path('teacher-add-exam', views.teacher_add_exam_view,name='teacher-add-exam'),
    path('delete-exam/<str:pk>', views.delete_exam_view,name='delete-exam'),
    path('teacher-question', views.teacher_question_view,name='teacher-question'),
    path('teacher-add-question', views.teacher_add_question_view,name='teacher-add-question'),
    path('teacher-view-question', views.teacher_view_question_view,name='teacher-view-question'),
    path('see-question/<str:pk>', views.see_question_view,name='see-question'),
    path('remove-question/<str:pk>', views.remove_question_view,name='remove-question'),
    path('teacher-update-course/<str:course_id>/', views.teacher_update_course_view, name='teacher_update_course'),
    
]