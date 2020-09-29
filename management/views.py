from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from .forms import DoctorsForm, UsercreateForm, PatientForm, CreateForm
from .models import Doctors, passhash, profile_background, patients,verifycode, test
from django.contrib import messages
from django.contrib.auth.models import User, auth
import bcrypt
from django.views.generic import DeleteView, View, TemplateView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.generic import ListView,DetailView,DeleteView, CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date
from random import randint
import requests
from requests.exceptions import HTTPError
from django import template
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator

'''# Create your views here.
class remove_patients(DeleteView):
    model = patients
    
    template_name = 'patients.html'
    success_url = 'doctors'

    def delete(self,request,slug):
        return self.destroy(request,slug)

    def get_object(self):
        id_ = self.kwargs.get("slug")
        return get_object_or_404(patients,slug=id_)


    def get_success_url(self):
        return reverse('patientview')
'''

def edit_patients(request,slug):
    return render(request,'blank-page.html')

'''@login_required()
def remove_patients(request,slug):
    if request.user.is_superuser:
        
        query = patients.objects.get(slug=slug)
        query.delete()
        messages.success(request,'Successfully Removed')
        return redirect('/patientview')
    else:
        messages.info(request, 'You do not have permission')
        return redirect('/patientview')
'''
@method_decorator(csrf_exempt, name='dispatch')
class RemovePatientsView(LoginRequiredMixin, DeleteView):
    model = patients
    success_message = 'Patient Successfully Removed'
    success_url = '/patientview'
    permission_denied_message = 'You do not have permission'
    def dispatch(self, request, *args, **kwargs):
        # maybe do some checks here for permissions ...
        if request.user.is_superuser:
            messages.success(self.request, self.success_message)
            response_data = {"result": self.success_url}
            resp = super(RemovePatientsView, self).dispatch(request, *args, **kwargs)
            return JsonResponse(response_data)
        else:
            messages.error(self.request, self.permission_denied_message)
            response_data = {"result": self.success_url}
            return JsonResponse(response_data)

@method_decorator(csrf_exempt, name='dispatch')
class RemoveDoctorsView(LoginRequiredMixin, DeleteView):
    model = Doctors
    success_message = 'Doctor Successfully Removed'
    success_url = '/doctors'
    permission_denied_message = 'You do not have permission'
    def dispatch(self, request, *args, **kwargs):
        # maybe do some checks here for permissions ...
        if request.user.is_superuser:
            messages.success(self.request, self.success_message)
            response_data = {"result": self.success_url}
            resp = super(RemoveDoctorsView, self).dispatch(request, *args, **kwargs)
            return JsonResponse(response_data)
        else:
            messages.error(self.request, self.permission_denied_message)
            response_data = {"result": self.success_url}
            return JsonResponse(response_data)

'''@login_required()   
def remove_doctors(request,slug):
    if request.user.is_superuser:
        query = Doctors.objects.get(slug=slug)
        query.delete()
        messages.success(request,'Successfully Removed')
        return redirect('/doctors')
    else:
        messages.info(request, 'You do not have permission')
        return redirect('/doctors')'''

@login_required()
def verify(request):
    if request.method == 'POST':
        code = request.POST['code']
        test = verifycode.objects.get(user_id=request.user.id)
        if str(code) == str(test.code):
            test.verified = True
            test.save()
            return redirect('/')
        else:
            messages.info(request, 'Invalid Verification Code')
            return redirect('/verify')
    else:
        if request.user.is_superuser:
            return redirect('/')
        else:
            test = verifycode.objects.get(user_id=request.user.id)
            if test.verified is True:
                return redirect('/')
            else:
                return render(request, 'verify.html')

class HomeView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        request.session.clear_expired()
        count = Doctors.objects.all().count()
        count1 = patients.objects.all().count()
        doctorsdata = Doctors.objects.all()
        patientsdata = patients.objects.order_by("-created_at")
        today = date.today
        context = { 
            "Dashboard" : "active",
            'count': count,
            'count1':count1,
            'doctorsdata':doctorsdata,
            'patientsdata':patientsdata,
            'today': today
        }
        return render(request, 'index.html', context)

'''@login_required()
def index(request):
    count = Doctors.objects.all().count()
    count1 = patients.objects.all().count()
    doctorsdata = Doctors.objects.all()
    patientsdata = patients.objects.order_by("-created_at")
    today = date.today
    #patientsdata = patients.objects.order_by("created_at").reverse()
    #for data in patientsdata:
        #print(data)
    

    request.session.clear_expired()
    context = { 
        "Dashboard" : "active",
        'count': count,
        'count1':count1,
        'doctorsdata':doctorsdata,
        'patientsdata':patientsdata,
        'today': today
    }
    return render(request, 'index.html', context)
    '''




'''
@login_required()
def profile(request):
    context = { 'Profile' : 'active'}
    return render(request, 'profile.html', context)

@login_required()
def patientview(request):
    data = patients.objects.all()
    context = { 
        "Patients" : "active",
        "data": data }
    return render(request, 'patients.html', context)


'''
def reset_password(request):
    if request.method == 'POST':
        new1 = request.POST['new_password1']
        new2 = request.POST['new_password2']
        if new1 == new2:
            request.session.clear_expired()
            username = request.session.get('username')
            code = request.session.get('code')
            if username is not None:
                user_data = User.objects.get(username=username)
                user = auth.authenticate(username=username, password=code)
                if user is not None:
                    salt= bcrypt.gensalt()
                    salt1 = salt.decode('utf-8')
                    hashed = bcrypt.hashpw(new1.encode('utf-8'), salt)
                    user_data.set_password(hashed)
                    user_data.save()
                    saltsave = passhash.objects.get(user_id=user_data.pk)
                    saltsave.salt = salt1
                    saltsave.save()
                    request.session.flush()
                    
                    subject = 'Password Updated'
                    message = 'Congratulations, your password has been updated successfully'
                    from_email = 'prabinoiid@gmail.com'
                    recipient_list = [user_data.email]
                    fail_silently = False
                    send_mail(subject, message, from_email, recipient_list, fail_silently)
                    messages.info(request, 'Password changed successfully')
                    return redirect('/')
                else:
                    messages.info(request, 'Internal Error')
                    return redirect('/')

            else:
                messages.info(request, 'Session Expired')
                return redirect('/password_code')

        else:
            messages.info(request, 'Incorrect Password')
            return redirect('/password_code')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            request.session.clear_expired()
            if request.session.get('username') is not None:
                print(request.session.get('username'))
                return render(request, 'forgotchange_password.html')
            else:
                messages.info(request, 'Session Expired')
                return redirect('/password_code')

def password_code(request):
    if request.method == 'POST':
        username = request.POST['username']
        code = request.POST['code']
        if User.objects.filter(username=username).exists():
            user = auth.authenticate(username=username, password=code)
            if user is not None:
                request.session.clear_expired()
                request.session['username'] = username
                request.session['code'] = code
                request.session.set_expiry(150)
                messages.info(request, 'Please set a new password')
                return redirect('/reset_password')
            else:
                messages.info(request, 'Incorrect reset code')
                return redirect('/password_code')

    
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'password-code.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user_data = User.objects.get(email=email)
            psw = str(randint(100000, 999999))
            
            salt = bcrypt.gensalt()
            salt1 = salt.decode('utf-8')
            hashed = bcrypt.hashpw(psw.encode('utf-8'), salt)
            user_data.set_password(hashed)
            user_data.save()
            
            user_salt = passhash.objects.get(user_id=user_data.pk)
            user_salt.salt = salt1
            user_salt.save();
            subject = 'Password Recovery'
            message = 'Please enter the following code to change the password for username - ' + str(user_data.username) + ': ' + hashed.decode('utf-8')
            from_email = 'prabinoiid@gmail.com'
            recipient_list = [email]
            fail_silently = False
            send_mail(subject, message, from_email, recipient_list, fail_silently)
            messages.info(request, "Code send to the email address")
            return render(request, 'password-code.html')

        else:
            messages.info(request, 'Email does not exists')
            return redirect('/forward_password')
        
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'forgot-password.html')

class patientview(LoginRequiredMixin, ListView):
    model = patients
    paginated_by = 12
    
    template_name = 'patients.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(patientview, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        today = date.today()
        context['Patients'] = "active" 
        context['today'] = today
        return context

@login_required()
def change_password(request):
    if request.method == 'POST':
        old = request.POST['old_password']
        new1 = request.POST['new_password1']
        new2 = request.POST['new_password2']
        
        
        if request.user.is_superuser:
            user = auth.authenticate(username=request.user.username, password=old)
            if user is not None:
                if new1 == new2:
                    user_data = User.objects.get(username=request.user.username)
                    user_data.set_password(new1)
                    user_data.save()
                    messages.info(request, 'Password changed successfully')
                    return redirect('/')
                else:
                    messages.info(request, 'New password did not matched')
                    return redirect('/change_password')
            else:
                messages.info(request, 'Old password did not matched')
                return redirect('/change_password')
        else:
            pdata = passhash.objects.get(user_id=request.user.pk)
                
            p1 = bcrypt.hashpw(old.encode('utf-8'), pdata.salt.encode('utf-8'))
            user = auth.authenticate(username=request.user.username, password=p1)
            if user is not None:
                if new1 == new2:
                    
                    user_data = User.objects.get(username=request.user.username)
                    
                    hashed = bcrypt.hashpw(new1.encode('utf-8'), pdata.salt.encode('utf-8'))
                    user_data.set_password(hashed)
                    user_data.save()
                    subject = 'Password Updated'
                    message = 'Congratulations, your password has been updated successfully'
                    from_email = 'info@theyatri.com'
                    recipient_list = [user_data.email]
                    fail_silently = False
                    send_mail(subject, message, from_email, recipient_list, fail_silently)
                    messages.info(request, 'Password changed successfully')
                    return redirect('/')
                    
                else:
                    messages.info(request, 'New password did not matched')
                    return redirect('/change_password')
            else:
                messages.info(request, 'Old password did not matched')
                return redirect('/change_password')
    else:
        context = {
            'Change_password': 'active'
        }
        return render(request, 'change-password.html', context)



@login_required()
def edit_profile(request, slug):
    profile = get_object_or_404(Doctors, slug=slug)
    background = profile_background.objects.get(user_id=profile.id)
    if request.method == 'POST':
        data = DoctorsForm(request.POST, request.FILES)
     
        if data.is_valid():
           
            first_name = data.cleaned_data['first_name']
            last_name = data.cleaned_data['last_name']
            dob = data.cleaned_data['dob']
            print(dob)
            gender = data.cleaned_data['gender']
            address = data.cleaned_data['address']                
            state = data.cleaned_data['state']               
            country = data.cleaned_data['country']               
            postalcode = data.cleaned_data['postalcode']
            phone = data.cleaned_data['phone']
            photo = data.cleaned_data['photo']
            if not photo:
                photo = profile.photo

            institution = request.POST['institution']
            subject = request.POST['subject']
            startingdate = request.POST['startingdate']
            #print(startingdate)
            if not startingdate:
                a = None
            else:
                a = datetime.strptime(startingdate, '%d/%m/%Y')
                a.strftime('%Y-%m-%d')
            completedate = request.POST['completedate']
            if not completedate:
                b = None
            else:
                b = datetime.strptime(completedate, '%d/%m/%Y')
                b.strftime('%Y-%m-%d')
            degree = request.POST['degree']
            grade = request.POST['grade']
            companyname = request.POST['companyname']
            location = request.POST['location']
            jobposition = request.POST['jobposition']
            periodfrom = request.POST['periodfrom']
            if not photo:
                pass
            if not periodfrom:
                c = None
            else:
                c = datetime.strptime(periodfrom, '%d/%m/%Y')
                c.strftime('%Y-%m-%d')
            periodto = request.POST['periodto']
            if not periodto:
                d = None
            else:
                d = datetime.strptime(periodto, '%d/%m/%Y')
                d.strftime('%Y-%m-%d')
            data1 = Doctors.objects.get(id=profile.id)

            data1.first_name = first_name
            data1.last_name = last_name
            
            
            data1.dob = dob
            data1.gender = gender
            data1.address = address
            data1.state = state
            data1.country = country
            data1.postalcode = postalcode
            data1.phone = phone
            data1.photo = photo
            
            data1.save()
            
            data5 = User.objects.get(username=slug)
            data5.first_name = data1.first_name
            data5.last_name = data1.last_name
            data5.save()
            
           
            
            
            #if background.exists():
            background.institution = institution
            background.subject = subject
            background.startingdate = a
            background.completedate = b
            background.degree= degree
            background.grade =grade
            background.companyname = companyname
            background.location = location
            background.jobposition =jobposition
            background.periodfrom = c
            background.periodto = d
            
            background.save()
            messages.info(request,"Changed data")
            return redirect('/profile/' + slug)
        
        else:
            messages.info(request, 'Data not valid')
            return redirect('/profile/' + slug)
            #else:
               # data3 =profile_background.objects.create(id=profile.id,institution=institution,subject=subject,startingdate=startingdate,completedate=completedate,degree=degree,grade=grade,companyname=companyname,location=location,jobposition=jobposition,periodfrom=periodfrom,periodto=periodto)
                #data3.save()
               # messages.info(request,"Created data")
                #return render(request, 'doctors.html')
    else:
        
        context = { 
            'Profile' : 'active',
            'data': profile,
            'background': background,
            'slug': slug

        }
        return render(request, 'edit-profile.html', context)

def profileview(request):
    data = User.objects.get(username=request.user.username)
    context = {
        'Profile': 'active',
        'object': data
    }
    return render(request, 'profile.html', context)



class DoctorsView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Doctors
    
    template_name = 'doctors.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DoctorsView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        
        context['Doctors'] = "active" 
        return context


class DoctorsDataView(LoginRequiredMixin, DetailView):

    model = Doctors
    template_name = 'profile.html'
           
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DoctorsDataView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        doc = Doctors.objects.get(username=self.kwargs['slug'])
        #usr = User.objects.get(username=self.kwargs['slug'])
        data = profile_background.objects.get(user_id=doc.id)
        context['Profile'] = "active" 
        context['data'] = data
        #context['object'] = usr
        return context
    


@login_required()
def add_doctor(request):
    data = DoctorsForm()
    if request.method == 'POST':
        data = DoctorsForm(request.POST, request.FILES)
        password1 = request.POST['password1']
        password2= request.POST['password2']
        
        
        if data.is_valid():
            username = data.cleaned_data['username']
            email = data.cleaned_data['email']
            first_name = data.cleaned_data['first_name']
            last_name = data.cleaned_data['last_name']
            
            if User.objects.filter(email=email).exists():
                #print("username taken")
                resp = {
                    'sent': 'email_taken'
                }
                return JsonResponse(resp)
            elif User.objects.filter(username=username).exists():
                #print('email taken')
                resp = {
                    'sent': 'username_taken'
                }
                return JsonResponse(resp)
            else:
                if password1:
                    if password1 == password2:
                    
                        data.save()
                        
                        salt= bcrypt.gensalt()
                        salt1 = salt.decode('utf-8')
                        hashed = bcrypt.hashpw(password1.encode('utf-8'), salt)

                        
                        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=hashed)
                        user.save()
                        docdata = Doctors.objects.get(username=username)
                        background = profile_background.objects.create(user_id=docdata.id)
                        background.save()
                        verify = verifycode.objects.create(user_id=user.pk, verified=True)
                        verify.save()
                        saltsave = passhash.objects.create(user_id=user.pk, salt=salt1)
                        saltsave.save()
                        subject = 'New Doctor account Registration'
                        message = 'Congratulations doctor for joining us.'
                        from_email = 'prabinoiid@gmail.com'
                        recipient_list = [email]
                        fail_silently = False
                        send_mail(subject, message, from_email, recipient_list, fail_silently)
                        messages.info(request, 'Doctor Created')
                        resp = {
                            'sent': 'saved'
                        }
                        return JsonResponse(resp)
                        
                    else:
                        resp = {
                            'sent': 'pass_not_matched'
                        }
                        return JsonResponse(resp)
                else:
                    resp = {
                        'sent': 'no_valid_pass'
                    }
                    return JsonResponse(resp)
            
        else:
            resp = {
                'sent': 'data_not_valid'
            }
            return JsonResponse(resp)
    else:
        data = DoctorsForm()
  
        context = { 
            "Doctors" : "active",
            "form" : data
        }
        return render(request, 'add_doctor.html', context)

@login_required()
def add_doctor_merge(request):
    data = DoctorsForm()
    if request.method == 'POST':
        data = DoctorsForm(request.POST, request.FILES)
        
        
        if data.is_valid():
            email = data.cleaned_data['email']
            user = User.objects.get(email=email)
            data.username = user.username
            data.first_name = user.first_name
            data.last_name = user.last_name
            data.email = user.email
            data.save()
            #verify = verifycode.objects.get(user_id=user.pk)           
            #verify.save() 
            subject = 'New Doctor account Registration'
            message = 'A user account has been created. An old account associated with email: ' + email + ' has been detected and merged as per your request.'
            from_email = 'prabinoiid@gmail.com'
            recipient_list = [email]
            fail_silently = False
            send_mail(subject, message, from_email, recipient_list, fail_silently)
            messages.info(request, 'Accounts merged')
            resp = {
                'sent': 'saved'
            }
            return JsonResponse(resp)          
        else:
            resp = {
                'sent': 'data_not_valid'
            }
            return JsonResponse(resp)
    else:
        messages.info(request, 'Internal error')
        return redirect('/doctors')

class test(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = test
    template_name = 'test.html'
    form_class = CreateForm
    success_message = 'Done'
    success_url = '/'
    


@login_required()
def add_patient(request):
    data = PatientForm()
    if request.method == 'POST':
        data = PatientForm(request.POST, request.FILES)
        password1 = request.POST['password1']
        password2= request.POST['password2']
        
        
        if data.is_valid():
            username = data.cleaned_data['username']
            email = data.cleaned_data['email']
            first_name = data.cleaned_data['first_name']
            last_name = data.cleaned_data['last_name']
            
            if User.objects.filter(email=email).exists():
                resp = {
                    'sent': 'email_taken'
                }
                return JsonResponse(resp)
            elif User.objects.filter(username=username).exists():

                resp = {
                    'sent': 'username_taken'
                }
                return JsonResponse(resp)
            
            else:

                if password1:
                    if password1 == password2:
                        
                        data.save()
                        
                        salt= bcrypt.gensalt()
                        salt1 = salt.decode('utf-8')
                        hashed = bcrypt.hashpw(password1.encode('utf-8'), salt)

                        
                        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=hashed)
                        user.save()
                        verify = verifycode.objects.create(user_id=user.pk, verified=True)
                        verify.save()
                        
                        saltsave = passhash.objects.create(user_id=user.pk, salt=salt1)
                        saltsave.save()
                        subject = 'New Patient account Registration'
                        message = 'A user account has been created to receive reports online and send us your queries.'
                        from_email = 'prabinoiid@gmail.com'
                        recipient_list = [email]
                        fail_silently = False
                        send_mail(subject, message, from_email, recipient_list, fail_silently)
                        messages.info(request, 'Patient Created')
                        resp = {
                            'sent': 'saved'
                        }
                        return JsonResponse(resp)
                        
                        #return redirect('/patientview')
                            
                    else:
                        resp = {
                            'sent': 'pass_not_matched'
                        }
                        return JsonResponse(resp)
                        #messages.info(request,'Password does not match')
                        #return redirect('/add_patient')
                else:
                    resp = {
                        'sent': 'no_valid_pass'
                    }
                    return JsonResponse(resp)
                    #messages.info(request, 'No valid password entered')
                    #return redirect('/add_patient')
            
        else:
            resp = {
                'sent': 'data_not_valid'
            }
            return JsonResponse(resp)
            #messages.info(request, 'Data not valid')
            #return redirect('/add_patient')
    else:
        data = PatientForm()
  
        context = { 
            "Patients" : "active",
            "form" : data
        }
        return render(request, 'add_patient.html', context)

@login_required()
def add_patient_merge(request):
    data = PatientForm()
    if request.method == 'POST':
        data = PatientForm(request.POST, request.FILES)
        
        
        if data.is_valid():
            email = data.cleaned_data['email']
            user = User.objects.get(email=email)
            data.username = user.username
            data.first_name = user.first_name
            data.last_name = user.last_name
            data.email = user.email
            data.save()
            #verify = verifycode.objects.get(user_id=user.pk)           
            #verify.save() 
            subject = 'New Patient account Registration'
            message = 'A user account has been created to receive reports online and send us your queries. An old account associated with email: ' + email + ' has been detected and merged as per your request.'
            from_email = 'prabinoiid@gmail.com'
            recipient_list = [email]
            fail_silently = False
            send_mail(subject, message, from_email, recipient_list, fail_silently)
            messages.info(request, 'Accounts merged')
            resp = {
                'sent': 'saved'
            }
            return JsonResponse(resp)          
        else:
            resp = {
                'sent': 'data_not_valid'
            }
            return JsonResponse(resp)
    else:
        messages.info(request, 'Internal error')
        return redirect('/patientview')



def logout(request):
    auth.logout(request)
    return redirect('/')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists()is False:
            messages.info(request,'Username not found.')
            return redirect('/accounts/login/')
        else:
            user1 = User.objects.get(username=username)
            if user1.is_superuser:
                user = auth.authenticate(username=username, password=password)

                if user is not None:
                    auth.login(request, user)
                    return redirect("/")
                else:
                    messages.info(request, 'Invalid Password')
                    return redirect('/accounts/login/')
            else:
                
                
                pdata = passhash.objects.get(user_id=user1.pk)
                
                p1 = bcrypt.hashpw(password.encode('utf-8'), pdata.salt.encode('utf-8'))
                user = auth.authenticate(username=username, password=p1)
                if user is not None:
                    auth.login(request, user)
                    return redirect('/')
                else:
                    messages.info(request, 'Invalid Password')
                    return redirect('/accounts/login/')

    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'login.html')

def register(request):
    data = UsercreateForm()
    if request.method == 'POST':
        data = UsercreateForm(request.POST)
        password1 = request.POST['password1']
        password2= request.POST['password2']
        if data.is_valid():
            username = data.cleaned_data['username']
            email = data.cleaned_data['email']
            first_name = data.cleaned_data['first_name']
            last_name = data.cleaned_data['last_name']
            if password1:
                if password1 == password2:
                    if User.objects.filter(username=username).exists():
                        #print("username taken")
                        messages.info(request,'username taken')
                        return redirect('/accounts/register/')
                    elif User.objects.filter(email=email).exists():
                        #print('email taken')
                        messages.info(request, 'email taken')
                        return redirect('/accounts/register/')
                    else:

                        salt = bcrypt.gensalt()
                        salt1 = salt.decode('utf-8')
                        hashed = bcrypt.hashpw(password1.encode('utf-8'), salt)

                        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name,password=hashed)
                        user.save();

                        user_salt = passhash.objects.create(salt= salt1,user_id=user.pk)
                        user_salt.save();

                        psw = str(randint(100000, 999999))
                        data = verifycode.objects.create(user_id=user.pk, code=psw)
                        data.save()
                        
                        subject = 'New Account Registration'
                        message = 'Congratulations for creating account with us, Your verification code is:' + str(psw)
                        from_email = 'prabinoiid@gmail.com'
                        recipient_list = [email]
                        fail_silently = False
                        send_mail(subject, message, from_email, recipient_list, fail_silently)
                        messages.info(request, "user created")
                        user = auth.authenticate(username=username, password=hashed)
                        auth.login(request,user)
                        return redirect('/verify')
                else:
                    #print('password matched')
                    messages.info(request, 'password not matched')
                    return redirect('/accounts/register/')
            else:
                messages.info(request, 'No valid password entered')
                return redirect('/accounts/register/')
        else:
            messages.info(request, 'No valid data entered')
            return redirect('/accounts/register/')

    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            data = UsercreateForm()
    
            context = { 
                "Doctors" : "active",
                "form" : data
            }
            return render(request,'register.html', context)
    

