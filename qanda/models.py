from django.db import models
from django.contrib.auth.models import User

class QuestionCategory(models.Model):
    category = models.CharField(max_length=20, default="", primary_key = True, db_column='category_id')
    categoryEng = models.CharField(max_length=50, default="")

    def __str__(self):
        return(str(self.category))

class Question(models.Model):
    number = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20, default="")
    question = models.CharField(max_length=1000, default="")
    category = models.ForeignKey(QuestionCategory, to_field='category', on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return (str(self.category)+" "+str(self.number)+". "+str(self.title))

class Answer(models.Model):
    authuser = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    
    # 아래처럼 forein key로 하지 않아도 되나? 지금 views.py의 instance[0].questionNumber = todaysQuestion.number로 하는 건 너무 주먹구구식 아닌가?
    # questionNumber = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, default=None)
    questionNumber = models.IntegerField(null=True, default=None)
    
    answer = models.CharField(max_length=500)
    dateAnswered = models.DateField(auto_now_add=True)

    def __str__(self):
        return (str(self.questionNumber)+"--answered by--"+str(self.authuser)+"--on "+str(self.dateAnswered)[:11])

