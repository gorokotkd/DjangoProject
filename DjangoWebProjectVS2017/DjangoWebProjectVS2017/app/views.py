"""
Definition of views.
"""

from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from django.template.loader import render_to_string
from datetime import datetime
from django.http.response import HttpResponse, Http404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Question,Choice,User
from django.template import loader
from django.core.urlresolvers import reverse
from app.forms import QuestionForm, ChoiceForm,UserForm
from django.shortcuts import redirect
from django.http import JsonResponse
import json


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Autor de la web',
            'message':'Datos de contacto',
            'year':datetime.now().year
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year
        }
    )
def index(request):
    if request.method == "POST":
        form = request.POST
        latest_question_list = Question.objects.filter(topic=form.get("topicSelect", "")).order_by('-pub_date')
    else:
        latest_question_list = Question.objects.order_by('-pub_date')
        
    question_topic_list = list(Question.objects.values('topic').distinct())
    template = loader.get_template('polls/index.html')
    context = {
                'title':'Lista de preguntas de la encuesta',
                'year' : datetime.now().year,
                'latest_question_list': latest_question_list,
                'question_topic_list' : question_topic_list,
              }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
     question = get_object_or_404(Question, pk=question_id)
     return render(request, 'polls/detail.html', {'title':'Respuestas asociadas a la pregunta:','question': question, 'year' : datetime.now().year})

def results(request, question_id, choice_id):
    question = get_object_or_404(Question, pk=question_id)
    choice = get_object_or_404(Choice, pk=choice_id)
    #return render(request, 'polls/results.html', {'title':'Resultados de la pregunta:','question': question, 'year':datetime.now().year, 'choice' : choice})
    html = render_to_string('polls/results.html', {'title':'Resultados de la pregunta:','question': question, 'year':datetime.now().year, 'choice' : choice})
    return HttpResponse(html)

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/detail.html', {
            'title' : 'pagina de votacion',
            'question': p,
            'error_message': "ERROR: No se ha seleccionado una opcion",
            'year':datetime.now().year
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Siempre devolver un HttpResponseRedirect despues de procesar
        # exitosamente el POST de un form. Esto evita que los datos se
        # puedan postear dos veces si el usuario vuelve atras en su browser.
        #return HttpResponseRedirect(reverse('results', args=(p.id, selected_choice.id,)))
        question = get_object_or_404(Question, pk=question_id)
        choice = get_object_or_404(Choice, pk=selected_choice.id)
        html = render_to_string('polls/results.html', {'title':'Resultados de la pregunta:','question': question, 'year':datetime.now().year, 'choice' : choice})
        return HttpResponse(html)
  #      return JsonResponse(
   #             {
    #                'content':{
     #                       'url' : '/'+str(p.id)+'/'+str(selected_choice.id)+'/results'
      #                  }
       #             }
        #    )

def question_new(request):
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.pub_date=datetime.now()
                question.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = QuestionForm()
        return render(request, 'polls/question_new.html', {
                                                            'form': form,
                                                            'title' : 'Pagina para añadir un apregunta',
                                                            'message' : 'Pregunta lo que sea.',
                                                            'year' : datetime.now().year})

def choice_add(request, question_id):
        question = Question.objects.get(pk = question_id)
        if request.method =='POST':
            form = ChoiceForm(request.POST)
            if form.is_valid():
                choice = form.save(commit = False)
                choice.question = question
                choice.vote = 0
                choice.save()         
                #form.save()
        else: 
            form = ChoiceForm()
        #return render_to_response ('choice_new.html', {'form': form, 'poll_id': poll_id,}, context_instance = RequestContext(request),)
        return render(request, 'polls/choice_new.html', {'title':'Pregunta:'+ question.question_text,'form': form , 'year' : datetime.now().year, 'question' : question})

def chart(request, question_id):
    q=Question.objects.get(id = question_id)
    qs = Choice.objects.filter(question=q)
    dates = [obj.choice_text for obj in qs]
    counts = [obj.votes for obj in qs]
    context = {
        'title' : 'grafico de resultados',
        'dates': json.dumps(dates),
        'counts': json.dumps(counts),
        'year':datetime.now().year
    }

    return render(request, 'polls/grafico.html', context,)

def user_new(request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = UserForm()
        return render(request, 'polls/user_new.html', {'title' : 'Registro de usuario','form': form, 'year':datetime.now().year})

def users_detail(request):
    latest_user_list = User.objects.order_by('email')
    template = loader.get_template('polls/users.html')
    context = {
                'title':'Lista de usuarios',
                'latest_user_list': latest_user_list,
                'year':datetime.now().year
              }
    return render(request, 'polls/users.html', context)