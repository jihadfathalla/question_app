from django.shortcuts import render, redirect, HttpResponse
from datetime import date
from django.db.models import Q
from django.contrib import messages
from django.db.models import Count
from user_question.models import *
from user_question.forms import *
from django.http import JsonResponse
import random




# Create your views here.

def create_user_question(request):
    user_form = CustomUserForm()
    question = Question.objects.all().first()
    answers = QuestionAnswer.objects.filter(question=question)
    an_one , an_one_count, an_two,an_two_count,an_three,an_three_count = pie_chart()

    myContext = {
    "page_title":"سؤال app",
    "user_form": user_form,
    "question": question,
    "answers":answers,
    'an_one':an_one,
    'an_one_count':an_one_count,
    'an_two': an_two,
    'an_two_count':an_two_count,
    'an_three':an_three,
    'an_three_count':an_three_count,
    }
    return render(request, 'create-user-question.html', myContext)

def save_user_date(request):
    name = request.GET.get('name', None)
    mobile = request.GET.get('mobile', None)
    country = request.GET.get('nationality', None)
    date= request.GET.get('date', None)
    gender = request.GET.get('type', None)
    address = request.GET.get('address', None)
    answer_list=[]

    if name is None :
        message = 'من فضلك قم بإدخال الاسم'
        data = {'message': message}
        return JsonResponse(data)
    if mobile is None:  
        message = 'من فضلك قم بإدخال رقم الموبيل'
        data = {'message': message}
        return JsonResponse(data)
    if len(name) > 50  :
        message = 'يجب ان لا يتعدي الاسم ال 50 حرف'
        data = {'message': message}
        return JsonResponse(data)
    if len(mobile) != 11  :
        message = 'رقم الموبيل يجب ان يكون 11 رقم '
        data = {'message': message}
        return JsonResponse(data)          

    try:
        old_user = CustomUser.objects.get(name=name , mobile=mobile)  
        user_questions = UserQuestionAnswer.objects.filter(user = old_user).values_list('question', flat=True)
        if user_questions:
            all_questions = Question.objects.all().exclude(id__in=user_questions).values('id')
        else:
            all_questions = Question.objects.all().values('id')
        random_id = random.choice(all_questions)["id"]
        try:
            question = Question.objects.get(pk=random_id)
            answers = QuestionAnswer.objects.filter(question=question)
            for answer in answers:
                answer_list.append(str(answer.id)  +' : '+ answer.answer)
            my_array = ','.join(answer_list)
        except Question.DoesNotExist:
            question = question = Question.objects.get(pk=1)
            answers = ['1 : الإجابة الأولى']
        data = {'message': 'success','user':old_user.id,'question_name':question.question,'question_id':question.id,'answers':my_array }
        return JsonResponse(data)

    except CustomUser.DoesNotExist:
        try:
            user = CustomUser(
                name = name,
                mobile = mobile,
                address = address,
                country =country,
                date_of_birth =date,
                gender =gender,)
            user.save()
        except Exception as e:
            print(e)

        all_questions = Question.objects.all().values('id')
        random_id = random.choice(all_questions)["id"]
        try:
            question = Question.objects.get(pk=random_id)
            answers = QuestionAnswer.objects.filter(question=question)
            for answer in answers:
                answer_list.append(str(answer.id)  +' : '+ answer.answer)
            my_array = ','.join(answer_list)
        
        except Question.DoesNotExist:
            question = question = Question.objects.get(pk=1)
            answers = ['1 : الإجابة الأولى']
        data = {'message': 'success','user':user.id,'question_name':question.question,'question_id':question.id,'answers':my_array }

        return JsonResponse(data)


def save_user_answers(request):
    answers = request.GET.getlist("answers[]")
    user_id = request.GET.get('employee_id')
    question_id = request.GET.get('question_id')
    try:
        user = CustomUser.objects.get(id =user_id )
    except CustomUser.DoesNotExist:
        user = CustomUser.objects.get(id = 1 )
    try:
        question = Question.objects.get(id =question_id )
    except Question.DoesNotExist:
        question = Question.objects.get(id = 1 )        

    if len(answers) == 0:
        message= "من فضلك قم باختيار الإجابات "
    else:    
        if len(answers) == 3:
            answer_one = answers[0]
            answer_two = answers[1]
            answer_three = answers[2]

            user_question = UserQuestionAnswer(
                user = user,
                question = question,
                answer_one = QuestionAnswer.objects.get(id=answer_one),
                answer_two = QuestionAnswer.objects.get(id=answer_two),
                answer_three = QuestionAnswer.objects.get(id=answer_three)
            )
            user_question.save()

        if len(answers) == 2:
            answer_one = answers[0]
            answer_two = answers[1]
            user_question = UserQuestionAnswer(
                user = user,
                question = question,
                answer_one = QuestionAnswer.objects.get(id=answer_one),
                answer_two = QuestionAnswer.objects.get(id=answer_two),
            )
            user_question.save()
        if len(answers) == 1:
            answer_one = answers[0]
            user_question = UserQuestionAnswer(
                user = user,
                question = question,
                answer_one = QuestionAnswer.objects.get(id=answer_one),
            )
            user_question.save()    
        message = 'success'    
    pie_chart()    
    data = {'message': 'message'}
    return JsonResponse(data)


def pie_chart():
    question = UserQuestionAnswer.objects.all().last()
    answers = QuestionAnswer.objects.filter(question=question.question)
    
    answer_one_count = UserQuestionAnswer.objects.filter(question=question.question, answer_one=answers[0].id)
    if answer_one_count:
        # labels.append(answer_one_count.first().answer_one)
        # data.append(answer_one_count.count)
        an_one = answers[0]
        an_one_count = answer_one_count.count
    else :
        an_one = answers[0]
        an_one_count = 0


    answer_two_count = UserQuestionAnswer.objects.filter(question=question.question, answer_two=answers[1].id)
    if answer_two_count:
        # labels.append(answer_two_count.first().answer_one)
        # data.append(answer_two_count.count)
        an_two = answers[1]
        an_two_count = answer_two_count.count
    else :
        an_two = answers[1]
        an_two_count = 0

    answer_three_count = UserQuestionAnswer.objects.filter(question=question.question, answer_three =answers[2].id)
    if answer_three_count:
        # labels.append(answer_three_count.first().answer_one)
        # data.append(answer_three_count.count)
        an_three = answers[2]
        an_three_count = answer_three_count.count
    else :
        an_three = answers[2]
        an_three_count = 0    


    return an_one , an_one_count, an_two,an_two_count,an_three,an_three_count
