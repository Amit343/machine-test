from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
#import pyotp
from rest_framework.response import Response
from rest_framework.views import APIView
#from .models import phoneModel
import base64
#from phonenumber_field.modelfields import PhoneNumberField
'''
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"

# Time after which OTP will expire
EXPIRY_TIME = 50 # seconds

class getPhoneNumberRegistered_TimeBased(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            phoneModel.objects.create(
                Mobile=phone,
            )
            Mobile = phoneModel.objects.get(Mobile=phone)  # user Newly created Model
        Mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)  # TOTP Model for OTP is created
        print(OTP.now())
        print(Mobile)
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        return Response({"OTP": OTP.now()}, status=200)  # Just for demonstration

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)  # TOTP Model
        if OTP.verify(request.data["otp"]):  # Verifying the OTP
            Mobile.isVerified = True
            Mobile.save()
            return Response("You are authorised", status=200)
     '''   #return Response("OTP is wrong/expired", status=400)


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile ,Comment
import random
from django.http import HttpResponse
import http.client
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.views.generic import View,DetailView,DeleteView
from django.http import HttpResponseRedirect
from .models import communitypost,community_comment
from django.urls.base import reverse_lazy
from rest_framework.permissions import IsAuthenticated
#from .import View

# Create your views here


def send_otp(mobile , otp):
    print("FUNCTION CALLED")
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY
    headers = { 'content-type': "application/json" }
    url = "http://control.msg91.com/api/sendotp.php?otp="+otp+"&message="+"Your otp is "+otp +"&mobile="+mobile+"&authkey="+authkey+"&country=91"
    conn.request("GET", url , headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    return None



def login_attempt(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')

        user = Profile.objects.filter(mobile = mobile).first()

        if user is None:
            context = {'message' : 'User not found', 'class' : 'danger' }
            return render(request,'login.html', context)

        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.save()
        send_otp(mobile , otp)
        request.session['mobile'] = mobile
        return redirect('login_otp')
    return render(request,'login.html')  #here we have to use teemplate name


def login_otp(request):
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()

        if otp == profile.otp:
            user = User.objects.get(id = profile.user.id)
            login(request , user)
            return redirect('cart') #here comes our home page
        else:
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'login_otp.html' , context)

    return render(request,'login_otp.html' , context)





def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')

        check_user = User.objects.filter(email = email).first()
        check_profile = Profile.objects.filter(mobile = mobile).first()

        if check_user or check_profile:
            context = {'message' : 'User already exists' , 'class' : 'danger' }
            return render(request,'register.html' , context)

        user = User(email = email , first_name = name)
        user.save()
        otp = str(random.randint(1000 , 9999))
        profile = Profile(user = user , mobile=mobile , otp = otp)
        profile.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('otp')
    return render(request,'register.html')

def otp(request):
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()

        if otp == profile.otp:
            return redirect('cart')
        else:
            print('Wrong')

            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'otp.html' , context)


    return render(request,'otp.html' , context)

#resend otp function

def resend_otp(request):
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    attempt=0
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        attempt+=1

        if attempt<3:
            if otp == profile.otp:
                return redirect('cart')
            else:
                print('Wrong')
        else:
            return HttpResponse('ca;t send otp')

            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'otp.html' , context)


    return render(request,'otp.html' , context)


#  Adding the function comment likes and comment_dislikes

class Addcomment_likes(LoginRequiredMixin,View):
    def vedio_comment(self,request, id,pk,*args,**kwargs): #id is vedio id ,pk is comment id
        comment=Comment.objects.get(pk=pk)
        is_dislike=False
        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike=True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like=False
        for like in comment.like.all():
            if like==request.user:
                is_like=True
                break

        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)


        next= request.POST.get('next','/')
        return HttpResponseRedirect(next)


#Add the function comment_dislikes
class Add_dislikecomment(LoginRequiredMixin,View):
    def vedio_comment(self,request,id,pk,*awargs,**kwargs):
        comment=Comment.objects.get(pk=pk)

        is_like=False
        for like in comment.likes.all():
            if like==request.user:
                is_like=True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike=False

        for dislike in comment.dislikes.all():
            if dislike==request.user:
                is_dislike=True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .models import test
from .serializers import *

class testapiview(APIView):
    def get(self,request):
        event=test.objects.all()
        serializer=testserializer(event,many=True)
        return Response(serializer.data)

    def post(self,request,*args,**kwars):
        serializer=testserializer(data=request.data)
        if serializer.is_valid():
            time=request.data.get('time')
            #time=str(a)
            if time=="10:00-12:30":
                serializer.save()
                return Response({'status':'C-Contact S-SharingT-Team'})
            elif time=='14:00-15:30':
                 return Response({'C-contact'})
            else:
              #serializer.save()
              return Response({'status':'success','data':serializer.data})

