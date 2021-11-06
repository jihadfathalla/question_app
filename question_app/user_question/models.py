from typing import no_type_check
from django.db import models
from django.conf import settings
from django.db import models
from datetime import date
from django_countries.fields import CountryField



# Create your models here.


class CustomUser(models.Model):
    gender_list = [("M","ذكر"), ("F", "أنثى")]

    name = models.CharField(max_length=50, verbose_name= 'الاسم بالكامل')
    mobile = models.CharField(max_length=11, verbose_name='رقم الموبيل')
    address= models.CharField(max_length=255, blank=True, null=True, verbose_name='العنوان')
    country =CountryField(blank_label='(اختر  الجنسية)',blank=True, null=True)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name='تاريخ الميلاد')
    gender = models.CharField(max_length=5, choices=gender_list, blank=True, null=True,verbose_name='النوع')                                 
            
    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.TextField(verbose_name='السؤال')                                 
    
    def __str__(self):
        return self.question 

class QuestionAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True,related_name='answers')   
    answer = models.TextField(verbose_name='الإجابة')                              
    
    def __str__(self):
        return self.answer       

class UserQuestionAnswer(models.Model):
     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='users')
     question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='users')  
     answer_one = models.ForeignKey(QuestionAnswer,blank=True, null=True, on_delete=models.CASCADE,related_name='answer_one')
     answer_two = models.ForeignKey(QuestionAnswer, blank=True, null=True,on_delete=models.CASCADE,related_name='answer_two')   
     answer_three = models.ForeignKey(QuestionAnswer, blank=True, null=True,on_delete=models.CASCADE,related_name='answer_three')   

     def __str__(self):
          return self.user.name




