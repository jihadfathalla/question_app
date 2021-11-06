from django import forms
from crispy_forms.helper import FormHelper
from django.db.models import Q
from datetime import date
from user_question.models import *
from django_countries.widgets import CountrySelectWidget



class CustomUserForm(forms.ModelForm):
     class Meta:
          model = CustomUser
          fields = '__all__'

      

     def __init__(self, *args, **kwargs):
          super(CustomUserForm, self).__init__(*args, **kwargs)
          self.fields['date_of_birth'].widget.input_type = 'date'
          self.fields['country'].widget.attrs['required'] = 'required'
          self.fields['gender'].widget.attrs['required'] = 'required'
          self.fields['name'].widget.attrs['required'] = 'required'
          for field in self.fields:
               self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
          self.helper = FormHelper()
          self.helper.form_show_labels = True




class UserQuestionAnswerForm(forms.ModelForm):
     class Meta:
          model = UserQuestionAnswer
          fields = '__all__'


     def __init__(self, *args, **kwargs):
          super(UserQuestionAnswerForm, self).__init__(*args, **kwargs)
          for field in self.fields:
               self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
          self.helper = FormHelper()
          self.helper.form_show_labels = True



class QuestionForm(forms.ModelForm):
     class Meta:
          model = Question
          fields = '__all__'

     def __init__(self, *args, **kwargs):
          super(QuestionForm, self).__init__(*args, **kwargs)
          for field in self.fields:
               self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
          self.helper = FormHelper()
          self.helper.form_show_labels = True


class QuestionAnswerForm(forms.ModelForm):
     class Meta:
          model = QuestionAnswer
          exclude = ('question',)

     def __init__(self, *args, **kwargs):
          super(QuestionAnswerForm, self).__init__(*args, **kwargs)
          for field in self.fields:
               self.fields[field].widget.attrs['class'] = 'form-control parsley-validated'
          self.helper = FormHelper()
          self.helper.form_show_labels = True
