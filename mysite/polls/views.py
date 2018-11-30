from django.shortcuts import render
from polls.models import Question,Choice,Goods
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#把参数传给html
def index(request):
    latest_qustion_list=Question.objects.all()
    print(latest_qustion_list)
    context={
        'latest_question_list':latest_qustion_list
    }
    return render(request,"polls/index.html",context)
    # template=loader.get_template("polls/index.html")
    # return HttpResponse(template.render(context,request))



def goods(request,kw):
    good_list=Goods.objects.filter(keyword=kw)
    print(good_list)
    context = {
        'goods': good_list
    }
    return render(request,'polls/goods.html',context)




def detail(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
