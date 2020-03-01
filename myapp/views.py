from django.shortcuts import render ,get_object_or_404

# Create your views here.

from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Question,Choice

from django.urls import reverse


def home(request):
    try :
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
    except:
        raise Http404

    template = ('myapp/home.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request,template,context)



def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'myapp/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'myapp/results.html', {'question': question})

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

