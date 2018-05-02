#from django.http import HttpResponse
#from django.template import loader
#from django.http import Http404
from django.shortcuts import get_object_or_404, render
'''get_object_or_404 is a common idiom to use get and raise http404'''
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
#the page design is hard coded in the views.
#we want to amend our index,detail and results views and use generic views instead.
'''def index (request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	#template= loader.get_template('polls/index.html')#this loads the template index.htmland passes it a context
	context={'latest_question_list':latest_question_list}
	return render(request,'polls/index.html',context)
	#output=','.join ([q.question_text for q in latest_question_list])
	a simpler way is to use render.you first import render  return render(request,'polls/index.html',context)'''
	#return HttpResponse(template.render(context, request))s
class IndexView(generic.ListView):#list view displays a list of objects
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'
	def get_queryset(self):
		"""Return the last five published questions(not including those set to be published in the future)"""
		return Question.objects.filter(pub_date=timezone.now()).order_by('-pub_date')[:5]

'''def detail(request,question_id):
	#try:
		#question = Question.objects.get(pk=question_id)
	#except Question.DoesNotExist:
		#raise Http404("question does not exist")
	question = get_object_or_404(Question,pk=question_id)
	return render(request,'polls/detail.html',{'question':question})'''
class DetailView(generic.DetailView):#detail page for a particular type of object
	model = Question #model generic view will act upon
	template_name = 'polls/detail.html'
#even though future questions do not appear in the index, users can still reach them if they know or guess the right url
	def get_queryset(self):
		"""excludes any questions that aren't published yet"""
		return Question.objects.filter(pub_date=timezone.now())

	
class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'
	def get_queryset(self):
		"""excludes any questions that aren't published yet"""
		return Question.objects.filter(pub_date=timezone.now())

def vote(request,question_id):
	question= get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])#request.post (values are always string)is a dic.like object that lets you access submitted data by key name
	except (KeyError, Choice.DoesNotExist):
		return render(request,'polls/detail.html', {'question':question,'error message':"you didn't select a choice. ",})
	else:
		selected_choice.votes += 1
		selected_choice.save()
	return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
	

