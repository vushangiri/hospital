from django.urls import path,include
from .views import DoctorsView,DoctorsDataView, patientview, RemovePatientsView, HomeView, RemoveDoctorsView, test
from . import views

app_name = 'management'

urlpatterns = [

    #path('', views.index,name="index"),
    path('', HomeView.as_view()),
    path('doctors', DoctorsView.as_view()),
    path('profile/<slug>/', DoctorsDataView.as_view(),name='profile'),
    path('profile/', DoctorsDataView.as_view(),name='profile'),
    path('profileview', views.profileview, name='profileview'),
    path('change_password', views.change_password, name='change_password'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('password_code', views.password_code, name='password_code'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('add_doctor', views.add_doctor, name='add_doctor'),
    path('add_doctor_merge', views.add_doctor_merge, name='add_doctor_merge'),
    path('patientview', patientview.as_view(), name='patientview'),
    #path('profile', views.profile, name='profile'),
    path('add_patient', views.add_patient, name='add_patient'),
    path('add_patient_merge', views.add_patient_merge, name='add_patient_merge'),
    path('edit_profile/<slug>/', views.edit_profile, name='edit_profile'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/logout/', views.logout, name='logout'),
    path('verify',views.verify,name = 'verify'),
    #path('remove_patients/<slug>', views.remove_patients, name='remove_patients'),
    path('remove_patients/<slug>', RemovePatientsView.as_view(), name='remove_patients'),
    path('edit_patients/<slug>',views.edit_patients,name='edit_patients'),
    #path('remove_doctors/<slug>', views.remove_doctors, name='remove_doctors'),
    path('remove_doctors/<slug>', RemoveDoctorsView.as_view(), name='remove_doctors'),
    path('test/<int:pk>', test.as_view(), name='test')

]


