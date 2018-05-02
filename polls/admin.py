#customizing the admin site
from __future__ import unicode_literals

from django.contrib import admin
from .models import Question, Choice
#adding a bunch of choices directly when you create the question object.choice objects are edited on questions admin page
class ChoiceInLine(admin.TabularInline):
	#stalkedinline is vertical arrangement
	#tubularinline:table
	model = Choice
	extra = 3
class QuestionAdmin(admin.ModelAdmin):
	#creating of forms with dozen of fields(splitting form to fieldsets)
	fieldsets = [(None,{'fields':['question_text']}), ('Date information',{'fields':['pub_date'], 'classes':['collapse']}), ]
	inlines = [ChoiceInLine]
	list_display = ('question_text','pub_date','was_published_recently')
	list_filter =['pub_date']
	search_fields = ['question_text']

admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)
