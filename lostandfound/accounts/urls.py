from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import MysubmittedView


from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home , name='home'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('delete/<post_id>',views.delete_post,name='delete'),
    path('search/<int:id>/', views.post_detail, name='detail'),
    path('mysubmitted/', MysubmittedView.as_view(),  name='mysubmitted'),
    path('dashboard/', views.dashboard, name='dashboard'),
	path('register/', views.register , name='register'),
	path('login/',views.login,name='login'),
	path('logout/',views.logout,name='logout'),
	path('change-password/',auth_views.PasswordChangeView.as_view(template_name='change-password.html',success_url='/laf/home'),name='change-password'),
	path('reset_password/',auth_views.PasswordResetView.as_view(template_name="forgot-password.html"),
     name="reset_password"),

    path('chat', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>', views.message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),
    path('api/users/<int:pk>', views.user_list, name='user-detail'),
    path('api/users', views.user_list, name='user-list'),

    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
     name="password_reset_confirm"),

    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
        name="password_reset_complete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)