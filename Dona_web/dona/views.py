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
#from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
# Create your views here.

#메인 페이지 - / - index.html
def index(request):  
    return render(request,'index.html')

def monthly_ranking(request):   
    return render(request, 'monthly_ranking.html')
def yearly_ranking(request):   
    return render(request, 'yearly_ranking.html')