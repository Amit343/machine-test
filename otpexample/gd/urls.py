from django.urls import path, include
#from gd  import  FollowUnfollowView


from .views import *
from django.urls import path
from django.views.generic import TemplateView
from .import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('allauth.urls')),
    path('test',views.testapiview.as_view())



    #path('' , login_attempt , name="login"),
    #path('register' , register , name="register"),
    #path('otp' , otp , name="otp"),
    #path('login-otp', login_otp , name="login_otp"),
    #path('vedio/<int:vedio_pk>/comment/<int:pk>/like', Addcomment_likes.as_view(), name='comment-like'),

]