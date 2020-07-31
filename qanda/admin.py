from django.contrib import admin
from .models import AllQuestion, Answer, QuestionCategory

class AnswerAdmin(admin.ModelAdmin):
    readonly_fields = ('dateAnswered',)

admin.site.register(AllQuestion)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuestionCategory)
