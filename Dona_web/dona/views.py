from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
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
from dona.models import User, region, help_board, messages, messages_Container, region_board
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.db import connection
from django.views.generic import ListView
from .forms import PostForm, RegionPostForm
from .forms import CommentForm, messagesForm, RegionCommentForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages as msgs

def handler400(request):
    return render(request,'400.html',status=400)
def handler403(request):
    return render(request,'403.html',status=403)
def handler404(request):
    return render(request,'404.html',status=404)
def handler500(request):
    return render(request,'500.html',status=500)

#메인 페이지 - / - index.html
def index(request):  
    return render(request,'index.html')

@login_required
def message_make(request,id):  
    if request.method == 'POST': 
        user = request.user
        board = help_board.objects.get(pk=id)
        samedata=messages_Container.objects.filter(userone=board.writer,usertwo=user,title=board.title)
        if(samedata):
            msgs.error(request,'이미 존재하는 메세지 입니다.')
            return redirect('detail',id)
        if(board.writer==user):
            return redirect('detail',id)

        new_message = messages_Container(
            userone=board.writer,
            usertwo=user,
            title=board.title,
            message_region=board.region
        )
        new_message.save()
        return redirect('message')
    else:
        return redirect('index')

@login_required
def region_message_make(request,id):  
    if request.method == 'POST': 
        user = request.user
        board = region_board.objects.get(pk=id)
        samedata=messages_Container.objects.filter(userone=board.writer,usertwo=user,title=board.title)
        if(samedata):
            msgs.error(request,'이미 존재하는 메세지 입니다.')
            return redirect('region_detail',id)
        if(board.writer==user):
            return redirect('region_detail',id)
        new_message = messages_Container(
            userone=board.writer,
            usertwo=user,
            title=board.title,
            message_region=board.region
        )
        new_message.save()
        return redirect('message')
    else:
        return redirect('index')

@login_required
def message(request):
    form = messagesForm()
    msg = request.GET.get('msg', None)
    user=request.user
    helper_id=None
    use_complete=0
    if(msg is not None):
        check_val=messages_Container.objects.get(Q(id=msg)&(Q(userone=user)|Q(usertwo=user))) # 비인가 user 접속 확인
        if not check_val:
            return redirect('message')
        if((datetime.now()- check_val.userone.recent_help).days>=1):
            use_complete=1
        helper_id=check_val.userone_id
        msg=int(msg)
        read_box=messages_Container.objects.get(Q(id=msg))
        # 읽지 않은 msg 처리
        if(read_box.userone_id==user.id):
            read_box.userone_unread=0
            read_box.save()
        else:
            read_box.usertwo_unread=0
            read_box.save()
    
    msg_container=messages_Container.objects.filter(Q(userone=user)|Q(usertwo=user))
    msg_content=messages.objects.filter(Q(message_id=msg))
    context={
        'msg_container': msg_container,
        'msg_content': msg_content,
        'form':form,
        'msg_id':msg,
        'helper_id':helper_id,
        'use_complete':use_complete
    }
    return render(request, 'message.html',context)

def person_ranking(request):  
    person_rank=User.objects.filter(is_superuser=0).order_by('-helping')[:20]
    return render(request, 'person_ranking.html',{'person_rank':person_rank})

def region_ranking(request):   
    region_rank=region.objects.all().order_by('-region_help')[:20]
    return render(request, 'region_ranking.html',{'region_rank':region_rank})

@login_required 
def mypage(request):   
    person_rank= User.objects.filter(helping__gt=request.user.helping).count()
    return render(request, 'mypage.html',{'person_rank':person_rank+1})


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
            return render(request, 'signup.html', {'form': f})

    else:
        f = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': f})

#게시판
class HelpListView(LoginRequiredMixin,ListView):
    model = help_board
    paginate_by = 12
    template_name = 'help_board_list.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'help_board_list'        #DEFAULT : <model_name>_list
    def get_queryset(self):
        user=self.request.user
        help_board_list = help_board.objects.filter(Q(region=user.region1)|Q(region=user.region2)).order_by('help_date') 
        return help_board_list    

#게시판
class RegionListView(LoginRequiredMixin,ListView):
    model = region_board
    paginate_by = 12
    template_name = 'region_board_list.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'region_board_list'        #DEFAULT : <model_name>_list
    def get_queryset(self):
        user=self.request.user
        region_board_list = region_board.objects.filter(Q(region=user.region1)|Q(region=user.region2)).order_by('-id')
        return region_board_list  

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
            return redirect('help_board_list')
    else:
        form = PostForm()
    return render(request, 'post.html', {'form': form })

@login_required
def region_new_post(request):
    if request.method == 'POST':
        form = RegionPostForm(request.POST)
        if form.is_valid():
            user = request.user
            get_region = request.POST.get('region')
            mini_region = get_region.split(" ")[-1]
            new_board = region_board(
                title = form.cleaned_data['title'],
                content = form.cleaned_data['content'],
                region = get_region,
                region_last = mini_region,
                writer = user
            )
            new_board.save()
            return redirect('region_board_list')
    else:
        form = RegionPostForm()
    return render(request, 'region_post.html', {'form': form })

@login_required
def detail(request, id):
    try:
        board = help_board.objects.get(pk=id)
        form = CommentForm()
    except board.DoesNotExist:
        raise Http404("Does not exist!")
    return render(request, 'detail.html', {'board': board,'form':form})

@login_required
def region_detail(request, id):
    try:
        board = region_board.objects.get(pk=id)
        form = RegionCommentForm()
    except board.DoesNotExist:
        raise Http404("Does not exist!")
    return render(request, 'regiondetail.html', {'board': board,'form':form})

@login_required
def delete(request, id):
    try:
        user=request.user
        board = help_board.objects.get(Q(pk=id)&Q(writer_id=user.id))
        board.delete()
    except board.DoesNotExist:
        raise Http404("Does not exist!")
    return redirect('help_board_list')

@login_required
def region_delete(request, id):
    try:
        user=request.user
        board = region_board.objects.get(Q(pk=id)&Q(writer_id=user.id))
        board.delete()
    except board.DoesNotExist:
        raise Http404("Does not exist!")
    return redirect('region_board_list')


def help(request):   
    return render(request, 'help.html')

def contact(request):   
    return render(request, 'contact.html')

@login_required
def add_content_to_msg(request, msg_id):
    user=request.user
    comments = request.POST.get('content', None)
    if messages_Container.objects.filter(id=msg_id,userone=user):
        flag=1
    else:
        flag=0
    if request.method == "POST":
        form=messagesForm(request.POST)
        if form.is_valid():
            make_unread=messages_Container.objects.get(id=msg_id)
            if(flag==1):
                make_unread.usertwo_unread+=1
                make_unread.save()
            else:
                make_unread.userone_unread+=1
                make_unread.save()
            messages=form.save(commit=False)
            messages.message_id=msg_id
            messages.content=comments
            messages.user_send=flag
            messages.save()
            return HttpResponseRedirect('/%s?msg=%s' % ('message', msg_id))
    return redirect('message')

# 메시지에 도움 1이 추가되었습니다. 이거 넣으면 좋을듯 완료정보는 message_container에 너두고 메세지 맨 위에 {}}이렇게 사용하면 좋을듯
# 추가로 user에 도움횟수만 추가하지말고 지역 정보에 +해야 region 왕 뽑을 수 있음
# form : message/help_clear/10?help_day=2 이렇게 들어가려고 참고로 help_day는 1 이상으로 해야하고
# 글을 올릴때 help_day가 도움 받은 횟수 /2 면 안됨 userone=board_writer /two= 도운 이
@login_required
def help_clear(request, msg_id):
    
    #help_day = request.GET.get('help_day', None)
    help_day=1
    helped_user=request.user 
    if((datetime.now()-helped_user.recent_help).days<1):
        return redirect('message')
    if(msg_id is None):
        return redirect('message')
    check_help=messages_Container.objects.get(Q(id=msg_id) & Q(userone=helped_user))
    if not check_help:
        return redirect('message')

    #도움 준 사람 도움 준 횟수 +1
    helping_user=check_help.usertwo
    tmp_helping=helping_user.helping
    helping_user.helping=tmp_helping+help_day
    helping_user.save()

    #도움 받은 사람 도움 받은 횟수 +1
    tmp_helped=helped_user.helped
    helped_user.helped=tmp_helped+help_day
    helped_user.recent_help=datetime.now()
    helped_user.save()

    #도움 지역 +1
    help_region=check_help.message_region
    check_region=region.objects.get(Q(region_name=help_region))
    tmp_count=check_region.region_help
    check_region.region_help=tmp_count+help_day
    check_region.save()

    #msg에 추가
    thanks_message=messages()
    thanks_message.message_id=msg_id
    thanks_message.content="도움을 주셔서 감사합니다. 도움 횟수 + 1"
    thanks_message.user_send=1
    thanks_message.save()
    return HttpResponseRedirect('/%s?msg=%s' % ('message', msg_id))



@login_required
def add_comment_to_post(request, help_board_id):
    board=get_object_or_404(help_board, pk=help_board_id)
    if request.method == "POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=board
            comment.author_id= request.user.id
            comment.save()
            return redirect('detail',help_board_id)

@login_required
def add_comment_to_region_post(request, region_board_id):
    board=get_object_or_404(region_board, pk=region_board_id)
    if request.method == "POST":
        form=RegionCommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=board
            comment.author_id= request.user.id
            comment.save()
            return redirect('region_detail',region_board_id)

@login_required
def message_delete(request,msg_id):
    user=request.user
    check_val=messages_Container.objects.filter(Q(id=msg_id)&(Q(userone=user)|Q(usertwo=user)))
    if(check_val):
        messages.objects.filter(message_id=msg_id).delete()
        messages_Container.objects.filter(id=msg_id).delete()
        return redirect('message')
    else:
        return redirect('message')


