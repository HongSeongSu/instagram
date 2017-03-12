from django.conf.urls import url

from . import views

app_name = 'member'
urlpatterns = [
    url(r'^login/$', views.logins, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^signup/$', views.signup_fbv, name='signup'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^change_profile_image/$', views.change_profile_image, name='change_profile_image'),

]