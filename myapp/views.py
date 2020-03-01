from django.shortcuts import render ,get_object_or_404
# Create your views here.
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Question,Choice
from django.urls import reverse
from django.views import generic

class HomeView(generic.ListView):
    template_name = 'myapp/home.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'myapp/detail.html'


class ResultView(generic.DetailView):
    model = Question
    template_name = 'myapp/results.html'



def vote(request, question_id):
    question = get_object_or_404(Question,pk = question_id)
    try:
        # get the choice that entered through the form
        selected_choice = question.choice_set.get(pk = request.POST['choice'])

    # it will enter the except case if no choice picked
    except (KeyError, Choice.DoesNotExist):
        return render(request,"myapp/detail.html",{
            "question" : question,
            'error_message' : " you didn't selected a choice "
        })
    else:
        # increase the votes for that choice by 1 inside the DB
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('myapp:results', args=(question.id,)))

