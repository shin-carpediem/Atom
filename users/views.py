from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# from django.contrib.sites.shortcuts import get_current_site
# from django.core.signing import BadSignature, SignatureExpired, loads, dumps
# from django.template.loader import render_to_string
# from django.views import generic
from email.mime.text import MIMEText
import smtplib
from .forms import CustomUserCreationForm
from atom.settings import DEFAULT_FROM_EMAIL


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            input_email = form.changed_data['email']
            input_password = form.changed_data['password']
            new_user = authenticate(email=input_email, password=input_password)
            if new_user is not None:
                # アクティベーションURLの送付
                # current_site = get_current_site(request)
                # domain = current_site.domain
                # ctx = {
                #     'protocol': request.scheme,
                #     'domain': domain,
                #     # 'token': dumps(new_user.pk),
                #     'user': new_user,
                # }
                # # need to change name
                # subject = render_to_string('user/email/subject.txt', ctx)
                # message = render_to_string('user/email/message.txt', ctx)
                # new_user.email_user(subject, message)
                # send mail for is_active false to true
                EMAIL = DEFAULT_FROM_EMAIL
                PASSWORD = 'wgrlfgkazekswvjl'
                TO = form.cleaned_data['email']

                msg = MIMEText(
                    'Hello.\n'
                    'Welcome to Djamazon.\n'
                    '\n'
                    'You created your own account on Djamazon.\n'
                    'From now on, you will get awesome experience!\n'
                    '\n'
                    'http://127.0.0.1:8000/signup/done/\n'
                    '\n'
                    'If you have a question, feel free to contact with us.\n'
                    '\n'
                    '\n'
                    'Sincerely,\n'
                    '\n'
                    '---------------------------------------------\n'
                    'Djamazon.Corporation\n'
                    '\n'
                    'Email: buru.aoshin@gmail.com\n'
                    '---------------------------------------------\n'
                )
            msg['Subject'] = '【Djamazon】Your account is created now'
            msg['From'] = DEFAULT_FROM_EMAIL
            msg['To'] = TO

            # access to the socket
            s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            s.starttls()
            s.sendmail(EMAIL, TO, msg.as_string())
            s.quit()
            return render(request, 'users/pls_activate.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


def pls_activate(request):
    return render(request, 'users/pls_activate.html')


def signup_done(request):
    user = request.user
    user.is_active = True
    login(request, user)
    return render(request, 'users/activate_done.html')


# def signup(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             input_email = form.changed_data['email']
#             input_password = form.changed_data['password']
#             new_user = authenticate(email=input_email, password=input_password)
#             if new_user is not None:
#                 login(request, new_user)
#                 # should change later
#                 return redirect('users:index')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'users/signup.html', {'form': form})


def index(request):
    return render(request, 'users/index.html')
