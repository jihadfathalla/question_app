from django.urls.conf import path, re_path
from pkg_resources import require
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from user_question.models import *
from django_countries.fields import CountryField
from django_countries import countries





######################### User Question  ###################################
def check_user_already_exist(name,mobile):
    try:
        old_user = CustomUser.objects.get(name=name , mobile=mobile)  
        return old_user
    except CustomUser.DoesNotExist:
        return False    



class CountrySerializer(serializers.Serializer):
    country = CountryField()
    

class CustomUserSerializer(serializers.ModelSerializer):
    country = CountrySerializer(required=False)
    class Meta:
        model = CustomUser
        exclude = ['id',]

    def create(self, validated_data):
        custom_user_obj = CustomUser(**validated_data)
        if not custom_user_obj.name :
            raise ValidationError({'name' : 'من فضلك قم بإدخال الاسم'})
        if  len(custom_user_obj.name) > 50 :
            raise ValidationError({'name' : 'الاسم لا يجب ان يتعدى 50 حرف'})  
        
        if not custom_user_obj.mobile :
            raise ValidationError({'mobile' : 'من فضلك قم بإدخال رقم الموبيل'})       
    
        if  len(custom_user_obj.mobile) != 11 :
            raise ValidationError({'mobile' : 'رقم الموبيل يجب ان يكون 11 رقم '})
        old_user = check_user_already_exist(custom_user_obj.name,custom_user_obj.mobile)    
        if not old_user: 
            custom_user_obj.save() 
            return custom_user_obj
        else: 
            return old_user      


        

    def update(self ,instance, validated_data,*args ,**kwargs):
        if not instance.name :
            raise ValidationError({'name' : 'من فضلك قم بإدخال الاسم'})
        if  len(instance.name) > 50 :
            raise ValidationError({'name' : 'الاسم لا يجب ان يتعدى 50 حرف'})  
        
        if not instance.mobile :
            raise ValidationError({'mobile' : 'من فضلك قم بإدخال رقم الموبيل'})       
    
        if  len(instance.mobile) != 11 :
            raise ValidationError({'mobile' : 'رقم الموبيل يجب ان يكون 11 رقم '})   

        instance.name = validated_data.get('name',instance.name)
        instance.mobile = validated_data.get('mobile',instance.mobile)
        instance.address = validated_data.get('address',instance.address)
        instance.country = validated_data.get('country',instance.country)
        instance.date_of_birth = validated_data.get('date_of_birth',instance.date_of_birth)
        instance.gender = validated_data.get('gender',instance.gender)
        instance.save() 
        return instance   
         

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ['id',]
  

class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        exclude = ['id',]    



class UserQuestionAnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserQuestionAnswer
        exclude = ('id',)
    
  


