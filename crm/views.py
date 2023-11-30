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
    aws_access_key_id="ASIATUYJP7SUJTGDKSGL",  # Replace 'your_access_key' with your AWS access key
    aws_secret_access_key="yWjzJIsaEvX399DalDBd9hsw3b6hUiGAyj2r3vPh",  # Replace 'your_secret_key' with your AWS secret key
    aws_session_token = "IQoJb3JpZ2luX2VjEIn//////////wEaCXVzLWVhc3QtMSJHMEUCIQCWp3UGAti7GuXqIuM+2Y9SvsxEsqXWXz1POtOksLqi6AIgewG/tpBeSS9SS3S2gpo91qEe7h+LZo3dH0X9UQ1hhIcqhAQI4v//////////ARADGgwyNTA3Mzg2Mzc5OTIiDBONlic9ePLSDdl1TCrYA15Su4kgNwk5S86KeJDGRCkOD8AFcciUwvo7SJ7sXTN1rqbxa9ChicJWj25B1X9VXPQgMeI90kIl+DM0YrSr+dxNfBlxfySVndQZWHoRP8q/kdTy64MEOb76DPBZx6BG1ED+JNxGRRIzKUQ0NuT9ig1dnJOdaeGvzshYeQp07elUTXtH7T7nwINb19nmWSGAVXFWUUicGDMcF3O3IEZWQk83u9cDXGrbcJdTUh254cw70fxLPls7KRDelTw/B/QyQZhbq5VT+uO+o63uMc+q+8PzUNPdhCXCJXvz4JySKDN1CHxN+NJn5ccMl79+CC7JYpT6Ta1Yr82hwDHT2Z/e/SJIWqsBiiagFvSuQQdFvtQxwMH7BPHjJ2+sNIwi2ViOu8ECY29uosEj6/W9sNo0iFIlWZtKxOrwS2504i4uAiuf+rhN+c45pNvZomdQjSpSxFQgJ4btM/oCriWtLmCh9X6P4yVDZ9qjRaBL5A3f/y/KxI4sTFbG5DaXrydsEQIH7s2J5srdqBzo2Gk0ASko5bBGdqXeNUUpum3XP+jGXD+rcrqbyFhkPlAQqtgJUKA7uq/+EVaM5Ctw0fm3Mb+Hslpnnqm8g4lvKKmh6C1U4Cgrc18VAZ1JPP0wqrWfqwY6pgGcOS8Vvj/r1741hG4itlThkR5HmUzD29m6N/U3Qw2t3UVxvk4aCu9XNoiazCSM9AqDV266je52CKdZ/YuHidWi3gUxpZFRqWcyj/RWJyBTBG2pEEjr/w+Iobd8jNRJjf5MG2EZ8sQDAinFdOoJt+6cPnGwCGKhspRmsUQ40IbEMzq3ll1a/6aUA3ANENwwgLvrsrQVDwyGAa4GFp54Y2W0RlirZm+z"
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



