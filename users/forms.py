from cProfile import label
from unicodedata import name
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile , Skill

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','email','username','password1','password2']
        labels = {
            'first_name': 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm,self).__init__(*args, **kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','email','username','location','bio','short_intro','profile_image','social_github','social_twitter','social_linkedin','social_youtube','social_website']

    def __init__(self, *args, **kwargs):
        super(ProfileForm,self).__init__(*args, **kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})    


#the class meta will hold the skill table for us in model,ths form class is just functionality for dealing wth the form logic which will show the user
#the page/form where thy will be redirected to add/edit skill
class SkillForm(ModelForm): 
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']
#this will help to just design or format the data alrdy in the pafe/form for user regarding skill
    def __init__(self, *args, **kwargs):
        super(SkillForm,self).__init__(*args, **kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})    

