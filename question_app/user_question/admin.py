from django.contrib import admin
from user_question.models import *
from django.contrib.admin import site

# Register your models here.
site.register(CustomUser)

site.register(Question)
site.register(QuestionAnswer)

site.register(UserQuestionAnswer)