from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

'''
class Question(models.Model):
    objects = models.Manager()
    
    number = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20, default="")
    question = models.CharField(max_length=100, default="")

    def __str__(self):
        return (str(self.number)+"."+str(self.title))

class Answer(models.Model):
    objects = models.Manager()

    authuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'qanda', null=True, default=None)
    questionTitle = models.ForeignKey(Question, on_delete=models.CASCADE, related_name = 'question', null=True, default=None)
    answer = models.CharField(max_length=500)
    dateAnswered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (str(self.questionTitle)+"--answered by--"+str(self.authuser)+"--on "+str(self.created))
'''