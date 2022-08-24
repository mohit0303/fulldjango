from email import message
from gettext import install
import profile
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm , ProfileForm, SkillForm
from .utils import searchProfiles , paginatenProfiles



def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username do not exist!')
        
        user = authenticate(request,username=username,password=password) #this will chck the name and pwd in the db

        #now if the user is there 
        if user is not None:
            login(request,user) #this login fun will create a session for the user in the db i.e in the session table & will add it in the browser cookies
            return redirect('profiles')
        else:
            messages.error(request, "Username or pwd is incorrect")

    return render(request,'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.error(request, 'User logged Out!')
    return redirect('login') #this logout function will delet the user session as well

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    #form = UserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        #form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request,'User Account is Created !!')

            login(request,user)
            return redirect('edit-account')
        else:
            messages.error(request, 'An error has occurred')


    context = {'page':page,'form':form}
    return render (request,'users/login_register.html',context)


def profiles(request):
    profiles,search_query = searchProfiles(request) #calling the search function
    custom_range , profiles = paginatenProfiles(request,profiles,3) #calling the pagination function

    context={'profiles':profiles,'search_query':search_query,'custom_range':custom_range}  #to let the searched word be present in the search bar pass it also in context so tht u can hav it in profile.html page
    return render(request,'users/profiles.html',context)


def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context={'profile':profile,'topSkills':topSkills,'otherSkills':otherSkills}
    return render(request,'users/user-profile.html',context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile':profile,'skills':skills,'projects':projects}
    return render(request,'users/account.html',context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request,'users/profile_form.html',context)


#doing to add a skill
@login_required(login_url="login")
def createSkill(request):
    profile = request.user.profile                #get the user
    form = SkillForm()                            #get the form
#onc user click the submit button
    if request.method == "POST":

        form = SkillForm(request.POST)            #getting the data entered
        
        if form.is_valid():
            skill = form.save(commit=False)       #save the data
            skill.owner=profile                   #attach/link the skill data entered to the owner of the account
            skill.save()
            messages.success(request,'Skill is added')
            return redirect('account')            #onc done submitting redirect user to its account page

    context = {'form':form}                       #now here is where we pass the detail of form from above variable form to our render html page skill_form.html
    return render(request,'users/skill_form.html',context)



#doing same now to update a skill
@login_required(login_url="login")
def updateSkill(request,pk):   #we need skill by its id to edit it os pk as id holder is used
    profile = request.user.profile                
    skill = profile.skill_set.get(id=pk)  #ths will gv the skill we r modifying
    form = SkillForm(instance=skill)                     #instace=skill set the instance of the skill we r editing// autofill the existing skill in form

    if request.method == "POST":
        form = SkillForm(request.POST,instance=skill)  #instance=skill used to say which skill we r working on             
        if form.is_valid():
            form.save()
            messages.success(request,'Skill is edited')
            return redirect('account')            

    context = {'form':form}                       
    return render(request,'users/skill_form.html',context)

def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        messages.success(request,'Skill is deleted')
        return redirect('account')
    context = {'object':skill}
    return render(request,'delete_template.html',context)
