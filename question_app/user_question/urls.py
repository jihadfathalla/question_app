from django.urls import path, include
from user_question import views

app_name = 'question'

urlpatterns = [
    ######################### BusinessGroup URLs ###################################
    path('', views.create_user_question, name='create-user-question'),
    path('user/data/', views.save_user_date, name='user-data'),
    path('user/answers/', views.save_user_answers, name='user-answers'),
    path('pie-chart/', views.pie_chart, name='pie-chart'),



       
]