from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from datetime import timedelta
from django.template import loader, RequestContext
import pickle
import joblib
import re
from collections import OrderedDict
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
#from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from dona.models import User
from dona.models import region
from dona.models import help_board
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.db import connection
from django.views.generic import ListView
from .forms import PostForm


#메인 페이지 - / - index.html
def index(request):  
    return render(request,'index.html')

@login_required
def message(request):   
    return render(request, 'message.html')

def monthly_ranking(request):   
    return render(request, 'monthly_ranking.html')
    
def mypage(request):   
    return render(request, 'mypage.html')

@method_decorator(csrf_exempt, name='dispatch')
def townsearch(request):
    town_input = request.POST.get('town_input', None)
    result = region.objects.filter(region_name__icontains=town_input).values('region_name')
    results=[]
    for i in result.values_list('region_name'):
        results.append(i[0])
    context = {'town_input': results}
    return HttpResponse(json.dumps(context), content_type="application/json")

@method_decorator(csrf_exempt, name='dispatch')
def townenroll(request):
    town_input = request.POST.get('town_input', None)
    btnToken= request.POST.get('btnToken')
    if(btnToken=='1'):
        user = request.user
        user.region1=town_input
        user.save()
    elif(btnToken=='2'):
        user = request.user
        user.region2=town_input
        user.save()
    context={}
    return HttpResponse(json.dumps(context), content_type="application/json")


# 로그인
class UserLoginView(LoginView):           
    template_name = 'login.html'
    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)

#회원가입
def signup(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            return render(request, 'index.html',{'messages' : '회원가입에 성공했습니다.'})
    else:
        f = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': f})
    
class HelpListView(ListView):
    model = help_board
    paginate_by = 15
    template_name = 'help_board_list.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'help_board_list'        #DEFAULT : <model_name>_list
    def get_queryset(self):
        help_board_list = help_board.objects.order_by('help_date') 
        return help_board_list    

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    paginator = context['paginator']
    page_numbers_range = 5
    max_index = len(paginator.page_range)

    page = self.request.GET.get('page')
    current_page = int(page) if page else 1

    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range
    if end_index >= max_index:
        end_index = max_index

    page_range = paginator.page_range[start_index:end_index]
    context['page_range'] = page_range

    return context

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            user = request.user
            get_region = request.POST.get('region')
            tume = request.POST.get('datetimepicker')
            mini_region = get_region.split(" ")[-1]
            new_board = help_board(
                title = form.cleaned_data['title'],
                content = form.cleaned_data['content'],
                help_date = tume,
                region = get_region,
                region_last = mini_region,
                writer = user
            )
            new_board.save()
            return render(request, 'index.html',{'messages' : '글 올리기 성공'})
    else:
        form = PostForm()
    return render(request, 'post.html', {'form': form})

def detail(request, id):
    try:
        board = help_board.objects.get(pk=id)
    except Board.DoesNotExist:
        raise Http404("Does not exist!")
    return render(request, 'detail.html', {'board': board})

def help(request):   
    return render(request, 'help.html')
def contact(request):   
    return render(request, 'contact.html')
def yearly_ranking(request):   
    return render(request, 'yearly_ranking.html')