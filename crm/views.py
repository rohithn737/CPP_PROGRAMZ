from django.shortcuts import render,redirect

from . forms import CreateUserForm, LoginForm, ThoughtForm, UpdateUserForm, UpdateProfileForm

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required 

from django.contrib import messages

from . models import Thought, Profile#Importing thought from model.py

from django.contrib.auth.models import User



# Create your views here.

def homepage(request):

    return render(request, 'crm/index.html')

def register(request):

    form = CreateUserForm() #Assign your model form to a variable

    if request.method == 'POST':

        form = CreateUserForm(request.POST) #Posting the valid things i.e usrname,email,password to the form

        if form.is_valid(): #Check if the form is valid or not

            current_user = form.save(commit= False) #this will not save the file immediately to our database

            form.save()

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



