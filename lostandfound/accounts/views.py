from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.http.response import JsonResponse, HttpResponse
from django.contrib import messages
from .models import *
# from .models import Userregister
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from accounts.models import Message
from accounts.serializers import MessageSerializer
from accounts.serializers import UserSerializer

# from .forms import UserregisterForm
# Create your views here.
def home(request):
	return render(request,'index.html')
def contact(request):
	return render(request,'contact.html')

def search(request):
	qs= Userregister.objects.all()
	iteam_querry= request.GET.get('iteam')
	landmark_querry= request.GET.get('landmark')
	city_querry= request.GET.get('city')
	datetime_querry= request.GET.get('datetime')
	if iteam_querry !='' and iteam_querry is not None:
		qs=qs.filter(iteam__icontains=iteam_querry)
	if landmark_querry !='' and landmark_querry is not None:
		qs=qs.filter(landmark__icontains		=landmark_querry)
	if city_querry !='' and city_querry is not None:
		qs=qs.filter(Q(iteam__icontains=city_querry) | Q(city__icontains=city_querry)).distinct()
	if datetime_querry !='' and datetime_querry is not None:
		qs=qs.filter(datetime__gte=datetime_querry)

	contex ={
		'queryset':qs
	}
	return render(request, 'lost-search.html', contex)
def post_detail(request,id):
	obj = Userregister.objects.get(id=id)
	context ={
		"object":obj
	}
	return render(request, "Iteam-profile.html", context)


class MysubmittedView(ListView):
 	"""docstring for ClassName"""
 	template_name = 'mysubmitted.html'
 	context_object_name = 'mysubmitted.html'

 	def get_queryset(self):
 		return Userregister.objects.filter(postuser=self.request.user)

def delete_post(request,post_id=None):
    post_to_delete=Userregister.objects.get(id=post_id)
    post_to_delete.delete()
    return redirect('mysubmitted')




def dashboard(request):
	puser = request.user
	puer_id= puser.id
	first_name = request.user.get_full_name()
	if request.method == 'POST':

		messages.info(request , "in")
		saverecord = Userregister()
		saverecord.postuser_id = puer_id
		saverecord.fullname = first_name
		saverecord.iteam = request.POST.get('iteam')
		saverecord.landmark = request.POST.get('landmark')
		saverecord.phone = request.POST.get('phone')
		saverecord.city = request.POST.get('city')
		saverecord.location = request.POST.get('location')
		saverecord.state = request.POST.get('state')
		saverecord.datetime = request.POST.get('datetime')
		saverecord.content = request.POST.get('content')
		saverecord.iteam_pic = request.POST.get('iteam_pic')
		saverecord.save()
		messages.info(request,"inside post successfully")
		return redirect('dashboard')
	else:
		return render(request,'found-form.html')

def logout(request):
	auth.logout(request)
	return redirect('home')


def login(request):
	if request.method == 'POST':
		username = request.POST['email']
		password = request.POST['password']
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user)
			messages.info(request,"Logged in successfully")
			return redirect('home')
		else:
			messages.info(request,"Invalid Credential")
			return redirect('login')
	else:
		return render(request,'login1.html')

def register(request):
	if request.method ==  'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		email = request.POST['email']

		if password1==password2:
			# if User.objects.filter(username=username).exists():
			# 	messages.info(request,'Username taken')
			# 	return redirect('register')
			if User.objects.filter(email=email).exists():
				messages.info(request,'Email taken')
				return redirect('register')
			else:
				user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
				user.save()
				messages.info(request,'user created successfully')
				return redirect('login')
		else:
			messages.info(request, 'password is not matching')
			return render(request, 'register1.html')
	else:
		return render(request,'register1.html')


@csrf_exempt
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            user = User.objects.create_user(username=data['username'], password=data['password'])
            UserProfile.objects.create(user=user)
            return JsonResponse(data, status=201)
        except Exception:
            return JsonResponse({'error': "Something went wrong"}, status=400)


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)





def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': User.objects.exclude(username=request.user.username)})


def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})