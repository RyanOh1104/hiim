from django.contrib import admin
from .models import Question, Answer

class AnswerAdmin(admin.ModelAdmin):
    readonly_fields = ('dateAnswered',)

admin.site.register(Question)
admin.site.register(Answer, AnswerAdmin)
