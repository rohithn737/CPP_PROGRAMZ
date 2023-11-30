#************IMPORTANT********************

#For migrations of the models use the below command

#python manage.py makemigrations

#To apply the migrations of the models to the database use the below command --

#python manage.py migrate

#After creating the models and migrate the model we need to update here

from django.db import models

from django.contrib.auth.models import User

class Thought(models.Model):

    title = models.CharField(max_length=150)
    content = models.CharField(max_length=1000)
    date_posted = models.DateTimeField(auto_now_add=True) #This is will automatically set created date for our conetnts stored in the database
    image = models.ImageField(null = True, blank = True, default = 'Default1.png', upload_to='media/')
    price = models.IntegerField(null = True)
    house_details = models.CharField(null = True, max_length=300)
    
    #FOREIGN KEY
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null = True) 
    #If the uer is deleted then thought will also be deleted
    #Foreign key will linked to the user module

#This model is to upload a pic to our user model
class Profile(models.Model):

    profile_pic = models.ImageField(null = True, blank = True, default = 'Default1.png', upload_to='media/') # (null = True)It will keep null value in the database
    #(null = True) will allow you to keep blank value in the form, (default = '') will keep a default pic untill u change it

     #FOREIGN KEY
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null = True) 
    #If the uer is deleted then thought will also be deleted
    #Foreign key will linked to the user module
