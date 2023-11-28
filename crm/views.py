from django.shortcuts import render,redirect

from . forms import CreateUserForm, LoginForm, ThoughtForm, UpdateUserForm, UpdateProfileForm

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required 

from django.contrib import messages

from . models import Thought, Profile#Importing thought from model.py

from django.contrib.auth.models import User

import boto3
from django.conf import settings
from django.http import HttpResponse


# Create your views here.


    
sns = boto3.client(
    "sns",
    region_name="eu-west-1",  # Replace 'your_region' with your AWS region
    aws_access_key_id="ASIATUYJP7SUH2F3ZJWA",  # Replace 'your_access_key' with your AWS access key
    aws_secret_access_key="y7xq33gtzkmbClcdNzvCp+kaliNpn70GAIXBEBiz",  # Replace 'your_secret_key' with your AWS secret key
    aws_session_token = "IQoJb3JpZ2luX2VjEG0aCXVzLWVhc3QtMSJHMEUCIFWIEYC36CMSDM9ZQr0RU7cW/7tPcpzgDKiusROaMpiSAiEAzNvq3b3exdfbRBDD4LXc4LQvA/uJz02pyAydM9eFgtAqhAQIxv//////////ARADGgwyNTA3Mzg2Mzc5OTIiDIrZ4mQtnSbG7ySWRyrYA66WRGJp4bZzFzXyavHqfmugRkjf2iGuGTNxsmgL6rkZmT9GKjsgvmHVwjofTyDFU9wq59kEivLX7gIsXwRmW7rzKAG29DtB/g0kTdLl09tCMcmcvY2YiXPpwVKBJ7RmE+FsjHXHH0FqoxUV1bgU7i4/LhE2C/itAwD/UrZ7/jBwqD9sJepwIK+6syiHYxitg4RT8LTRXxw45VpV1BNyC2QIpRvQRuEThgL+Vqm+Ww4qhichng1zv4NuQsRfAbT1A91bcXYRKFUz3v0nceS2AV25WKb3pyLgFI0VSJsdLz/R6f8wz/MLGAM31ib+yeNqI91uQ969eDu3hAWc1bJTGojRw1eMQZrE+bGYQWhKP7e3yoTTxLCXSOJeSQZyzVBwA1F9Csmx3K4BtF0ubGklpyzUrVhPm/7QpwyHQsbGUWhovzCrDH4sAodAkrS70ZsRtI+kcFWWBMQMOf0CFLw6xTYZLhsiju8FhcS+SC5UlVYUEPdzBt7j3NMM/XN7p8bYtL7RH5ShlfFs6CBjyssOXjQi4yqAUu3yQQHwqc9j54H9ZiqCGUmiYkQcawSXoTk+VnqpxSNaYYR85GU8xGeE0x6L0YkQZyrwMS7ZIELz/SJoglJcvOP1Gx0ws6GZqwY6pgFp6Sn34/8P1klJyVvxl1QGbBUmP8re7dX39ewXc7EZejd4DXcYW0BrYjeoj9I5NgcjFUuaEIfrqF8iPsG8tnemLDdjj3y7J/3PLUx8r2/uobljj8JgV1BvGak1zkc6pWz+LX4rMLwQmNI3rM0mgCgkEa+6TwxFMyx2Uh3k1Y07jkO0lNqyXBRKuSKr3xT0UWfM5CKrQIvIEefDkAklVrUmydGb5DqJ"
)

SNS_TOPIC_ARN = "arn:aws:sns:eu-west-1:250738637992:23119489-sns"

def homepage(request):

    return render(request, 'crm/index.html')

def register(request):

    form = CreateUserForm() #Assign your model form to a variable

    if request.method == 'POST':

        form = CreateUserForm(request.POST) #Posting the valid things i.e usrname,email,password to the form

        if form.is_valid(): #Check if the form is valid or not

            current_user = form.save(commit= False) #this will not save the file immediately to our database

            form.save()

            # Send SMS notification on successful registration
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=f"New User added",
            )

            profile = Profile.objects.create(user = current_user) #Create a profile model and bind it to the newly created user

            #This profile we have used for uploading images to the newly created user

            messages.success(request, 'User Created!') #Setting up message based on successful user creation, messages need to be imported at the top

            return redirect('my-login') #For this redirect needs to be added at the top, redirecting back to my login page

    context = {'RegistrationForm': form} #Context dictionary

    return render(request, 'crm/register.html', context)

def my_login(request):

    form = LoginForm() #Assign your model form to a variable

    if request.method == 'POST':
    
        form = LoginForm(request, data=request.POST) #the post request is stored in the form

        if form.is_valid(): #Check if the form is valid or not

            username = request.POST.get('username') #Getting the username and password that has been entered
            password = request.POST.get('password')

            user = authenticate(request, username=username, password= password) #Matching the password and username with the stored in database creds

            if user is not None: #If user is valid in the database

                auth.login (request, user)

                return redirect('dashboard')
    
    context = {'LoginForm': form}

    return render(request, 'crm/my-login.html', context)

def user_logout(request):

    auth.logout(request)

    return redirect('') #Redirecting to our homepage

@login_required(login_url = 'my-login')
def dashboard(request):

    #Adding profile pic of logged in user in dashboard

    profile_pic = Profile.objects.get(user=request.user) #User asking request 

    context = {'profilePic': profile_pic }

    return render(request, 'crm/dashboard.html', context)

@login_required(login_url = 'my-login')
def create_tasks(request):

    form = ThoughtForm()

    if request.method == 'POST':

        form = ThoughtForm(request.POST, request.FILES)


        if form.is_valid(): #Check if the form is valid or not

            thought = form.save(commit = False) #Adding the form to thought variable. 
            #Commit = False as asking the django to wait till the user details are added

            thought.user = request.user #Making the post request to the person who is logged in , basically matching the correct person

            thought.save() #Now asking the database after matching the user to save it to the database

            return redirect ('my-tasks')

           

    context = {'CreateThoughtForm': form}

    return render(request, 'crm/create-task.html', context)



@login_required(login_url = 'my-login')
def my_tasks(request):

    current_user = request.user.id #request the id if the user whi is currently logged in

    thought = Thought.objects.all().filter(user=current_user) #we are trying to fetch the thought objects of the current logged in user
    #when the user is trying to click on my-thouhts button/link

    context = {'AllThoughts': thought}


    return render(request, 'crm/my-tasks.html', context)


@login_required(login_url = 'my-login')
def update_tasks(request, pk):

    #the try and except usecase is to handle the users trying to login into other users account
    try:
        
        thought = Thought.objects.get(id=pk, user=request.user) #check id with the place holder value
        #user=request.user will check the id the logged in user ---- Correct logged in user can only change the details
    
    except:

        return redirect('my-tasks')

    form = ThoughtForm(instance = thought)#Gettting the instance of the thought which has been validated above
    if request.method == 'POST':
        
        form = ThoughtForm(request.POST, instance =thought, files= request.FILES) #instance = thought

        if form.is_valid(): #Check if the form is valid or not

            form.save()

        return redirect('my-tasks')

    context = {'UpdateThought': form}

    return render(request, 'crm/update-task.html', context)

@login_required(login_url = 'my-login')
def delete_tasks(request, pk):

    try:
        
        thought = Thought.objects.get(id=pk, user=request.user) #check id with the place holder value
        #user=request.user will check the id the logged in user ---- Correct logged in user can only change the details
    
    except:

        return redirect('my-tasks')

    if request.method == 'POST':

        thought.delete()

        return redirect('my-tasks')


    return render(request, 'crm/delete-task.html')


@login_required(login_url = 'my-login')
def profile_management(request):

    form = UpdateUserForm(instance=request.user) #this -- "instance=request.user" will pre upload the existing data

    profile = Profile.objects.get(user = request.user) #To get the objects 

    
    form_2 = UpdateProfileForm(instance = profile)

    if request.method == 'POST':

        form = UpdateUserForm(request.POST, instance=request.user)

        form_2 = UpdateProfileForm(request.POST, request.FILES,instance=profile) #If someone wants to send a file , 
        #then a post request will be sent with logged user getting matched.


        if form.is_valid(): #Check if the form is valid or not

            form.save()#Then save the form to database

            return redirect('dashboard')

        if form_2.is_valid(): #Check if the form is valid or not

            form_2.save()#Then save the form to database

            return redirect('dashboard')

        
    context = {'UserUpdateForm': form, 'ProfileUpdateForm': form_2}

    return render(request, 'crm/profile-management.html', context)

@login_required(login_url = 'my-login')
def delete_account(request):

    if request.method == 'POST':

        #from django.contrib.auth.models import User -- need to import this model before proceeding further
        deleteUser = User.objects.get(username=request.user) #Checking the username before deleting the account

        deleteUser.delete()

        return redirect('')

    return render(request, 'crm/delete-account.html')



