from django.shortcuts import render
from django.views import View
import json
from django.utils.encoding import force_str
from django.contrib.auth import login
from django.urls import reverse
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email 
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str  # Use `force_str` instead of `force_text` in newer Django
from .utils import account_activation_token
from django.contrib import auth
import threading
from  django.contrib.auth.tokens import PasswordResetTokenGenerator



# Create your views here.   

#sending the email fast for activation and for password reset
class EmailThread(threading.Thread):
     
     def __init__(self, email):
         self.email = email
         threading.Thread.__init__(self)
      
     def run(self):
         self.email.send(fail_silently=False)

         

class EmailValidationView(View):  # Validating the email
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email')  # Safer than data['email']

        if not validate_email(email):
            return JsonResponse(
                {'email_error': 'Enter a valid email address'},
                status=400
            )

        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {'email_error': 'Email is already taken'},
                status=400
            )

        return JsonResponse({'email_valid': True})

 
class UsernameValidationView(View):  # Validating the username
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        
        if not str(username).isalnum():
            return JsonResponse(
                {'username_error': 'Username should only contain alphanumeric characters'},
                status=400
            )

        if User.objects.filter(username=username).exists():  # ✅ Fixed here: lowercase `username` and `exists()`
            return JsonResponse(
                {'username_error': 'Username already taken'},
                status=400
            )

        return JsonResponse({'username_valid': True})
    
    

class RegistrationView(View): 
    def get(self, request): 
        return render(request, 'authentication/register.html')

    def post(self, request):
        #get user data
        #validate it
        #create user acount
        
        username = request.POST["username"]
        email = request.POST ["email"]
        password = request.POST["password"]
        
        
        context = {
            "fieldValues": request.POST
        }
        
        
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'password too shor put altleast six characters')    
                    return render(request, 'authentication/register.html', context)    
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active= False
                user.save()
                
                email_subject = "Account Activation"
                
                #path to view
                  #-getting the domain we are in 
                  #-relative url to verifcation
                  #-encode uid
                  #- token
                uid64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                       'uid64': uid64,
                        'token': account_activation_token.make_token(user)
                    })

                activate_url = f'http://{domain}{link}'

                email_body = f"Hi {user.username},\nPlease use this link to activate your account:\n{activate_url}"        
                
                send_mail(
                email_subject, 
                email_body,
                "",  # Replace with your actual email in settings
                [email],
                
                
               )
                
                EmailThread(email).start()
                
                messages.success(request, 'User created ')
                return render(request, 'authentication/register.html' )
         
        return render(request, 'authentication/register.html' )
   
     

class VerificationView(View):
    def get(self, request, uid64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=user_id)

            if user.is_active:
                messages.info(request, 'User already activated. Please log in.')
                return redirect('login')

            if not account_activation_token.check_token(user, token):
                messages.error(request, 'Invalid or expired activation link.')
                return redirect('login')

            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully. You can now log in.')
            return redirect('login')

        except Exception as ex:
            messages.error(request, 'Activation failed. Please try again later.')
            return redirect('login')

    
    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        context = {
        'fieldValues': {
            'username': username
        }
       }
          
        if username and password:
            user = auth.authenticate(username=username, password=password)
            
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f"Welcome {user.username}, you are logged in.")
                    return redirect("expenses")
                messages.error(request, "Account is not active, please check your email.")
                return render(request, 'authentication/login.html', context)
            
            messages.error(request, "Invalid credentials, try again.")
            return render(request, "authentication/login.html", context)
        
        messages.error(request, "Please fill in all the fields.")
        return render(request, "authentication/login.html", context)
    

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been loged out")
        return redirect("login")

class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'Authentication/reset-password.html')  # Capital A here

    def post(self, request):
        email = request.POST.get('email')
        context = {
            'values': request.POST
        }

        if not validate_email(email):
            messages.error(request, 'Please supply a valid email')
            return render(request, 'Authentication/reset-password.html', context)

        users = User.objects.filter(email=email)
        if users.exists():
            user = users[0]
            uid64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            token = PasswordResetTokenGenerator().make_token(user)
            link = reverse('reset-user-password', kwargs={'uid64': uid64, 'token': token})
            reset_url = f'http://{domain}{link}'

            email_subject = 'Password Reset Request'
            email_body = f"""
Hi {user.username},

We received a request to reset your password.

Please use the link below to set a new password:
{reset_url}

If you didn’t request this, please ignore this email.

Thanks,
Your Website Team
"""

            send_mail(
                email_subject,
                email_body,
                '',
                [email],
                
            )
            
            EmailThread(email).start()

            messages.success(request, 'We have sent you an email to reset your password.')
            return redirect('login')

        else:
            messages.error(request, 'No account found with that email address')
            return render(request, 'Authentication/reset-password.html', context)


class CompletePasswordReset(View):
    def get(self, request, uid64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=uid)

            # Debug print
            print(f"[DEBUG] UID: {uid}, User: {user.username}")

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.error(request, 'Password reset link is invalid or has expired.')
                return redirect('request-password')

            return render(request, 'Authentication/set-new-password.html', {
                'uid64': uid64,
                'token': token
            })

        except User.DoesNotExist:
            messages.error(request, 'User not found. Please enter your email to get a new reset link.')
            return redirect('request-password')

        except Exception as e:
            print("Error during password reset GET:", str(e))
            messages.error(request, 'Something went wrong. Try again.')
            return redirect('request-password')

    def post(self, request, uid64, token):
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'Authentication/set-new-password.html', {
                'uid64': uid64,
                'token': token
            })

        try:
            uid = force_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=uid)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.error(request, 'Token is invalid or has expired.')
                return redirect('request-password')

            user.set_password(password)
            user.save()

            messages.success(request, 'Password reset successful. You can now log in.')
            return redirect('login')

        except Exception as e:
            print("Error during password reset POST:", str(e))
            messages.error(request, 'Something went wrong. Please try again.')
            return render(request, 'Authentication/set-new-password.html', {
                'uid64': uid64,
                'token': token
            }) 
