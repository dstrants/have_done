from django.urls import path

from profiles import views

app_name = 'profiles'
urlpatterns = [
    path('avatar/', views.AvatarUpdateview.as_view(), name='avatar'),
    path('refresh_token/', views.refresh_token, name='refresh_token'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('notification/<int:id>', views.visit_notification, name='notification')
]
