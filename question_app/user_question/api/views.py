from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from rest_framework.decorators import api_view , permission_classes
from user_question.api.serializers import *
import random




@api_view(['POST',])
def create_user(request):
     """
     Purpose: create new custom user in custom user model,
     param : request,
     """
     if request.method == 'POST':
          user_serializer = CustomUserSerializer(data=request.data)
          if user_serializer.is_valid():
               user_serializer.save()
               data = {"success": True, "data": user_serializer.data}
               return Response(data, status=status.HTTP_201_CREATED)
          else:
               data = {"success": True, "data": user_serializer.errors}
               return Response(data, status=status.HTTP_201_CREATED)




@api_view(['GET',])
def get_question(request,user_id):
     try:
          old_user = CustomUser.objects.get(id=user_id) 
     except CustomUser.DoesNotExist:
          data = {"success": False, "data": "no user with this id"}
          return Response(data, status=status.HTTP_404_NOT_FOUND)

     user_questions = UserQuestionAnswer.objects.filter(user = old_user).values_list('question', flat=True)
     if user_questions:
          all_questions = Question.objects.all().exclude(id__in=user_questions).values('id')
     else:
          all_questions = Question.objects.all().values('id')
     random_id = random.choice(all_questions)["id"]
     question = Question.objects.get(pk=random_id)
     answers = QuestionAnswer.objects.filter(question=question)
     question_serializer =  QuestionSerializer(question)
     question_answer_serializer =  QuestionAnswerSerializer(answers,many=True)
     data = {"success": True, "question": question_serializer.data,'question_answers':question_answer_serializer.data }
     return Response(data, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST',])
def create_user_question_answer(request):
     """
     Purpose: create new custom user in custom UserQuestionAnswerSerializer model,
     param : request,
     """
     if request.method == 'POST':
          user_question_answer_serializer = UserQuestionAnswerSerializer(data=request.data)
          if user_question_answer_serializer.is_valid():
               user_question_answer_serializer.save()
               data = {"success": True, "data": user_question_answer_serializer.data}
               return Response(data, status=status.HTTP_201_CREATED)



@api_view(['GET',])
def pie_chart(request,question_id):
     labels=[]
     data=[]
     question = Question.objects.get(id=question_id)
     answers = QuestionAnswer.objects.filter(question=question)
    
     answer_one_count = UserQuestionAnswer.objects.filter(question=question, answer_one=answers[0].id)
     if answer_one_count:
          labels.append(answers[0].answer)
          data.append(answer_one_count.count())
      
     answer_two_count = UserQuestionAnswer.objects.filter(question=question, answer_two=answers[1].id)
     if answer_two_count:
        labels.append(answers[1].answer)
        data.append(answer_two_count.count())
       

     answer_three_count = UserQuestionAnswer.objects.filter(question=question, answer_three =answers[2].id)
     if answer_three_count:
        labels.append(answers[2].answer)
        data.append(answer_three_count.count())
     data_json = {"success": True, "labels": labels,'data':data}
     return Response(data_json, status=status.HTTP_201_CREATED)
   
      

