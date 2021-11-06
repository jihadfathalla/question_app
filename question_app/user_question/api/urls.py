from django.urls import path, include
from user_question.api import views

app_name = 'user_question'

urlpatterns = [
    ######################### API URLs ###################################
    path('user/create', views.create_user, name='create-user'),
    path('get/question/<int:user_id>', views.get_question, name='get_question'),
    path('answer/create', views.create_user_question_answer, name='create-answers'),
    path('pie_chart/<int:question_id>', views.pie_chart, name='pie_chart'), 

        
]