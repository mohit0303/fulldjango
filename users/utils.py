from django.db.models import Q
from .models import Profile,Skill
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


#adding pagination in user profile page
def paginatenProfiles(request,profiles,results):
    page = request.GET.get('page')                  #ths we getting which page to be shown 1st page or 2nd page or 3rd page dynamically from browser
    #results = 3 #bcz we r results in the view so no need to declare here now
    paginator = Paginator(profiles,results)         #projects is total no of projects, result is how much projects to be shown in one page

    try:
        profiles = paginator.page(page)             #now lets paginate the project,bcz above rt now ALL the projects are listed out so we need to index d project list and only get 3 in each page
    except PageNotAnInteger:
        page = 1                                    #if page not there show the first page
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages                  #if we dont hav more pages plz show the last page we hav
        profiles = paginator.page(page)             #so ths line will set the page to the last page we hav and gv the result

    leftindex = (int(page)-4)
    if leftindex < 1:
        leftindex = 1

    rightindex = (int(page) + 5)
    if rightindex > paginator.num_pages:
        rightindex = paginator.num_pages + 1

    custom_range = range(leftindex,rightindex)

    return custom_range,profiles




def searchProfiles(request):
    search_query = '' #ths variable will be used to search the value stored in it in our DB but if no value thn it shld be empty

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')  #if there is any value in search query thn put tht value insd search_quer varbl

    skills = Skill.objects.filter(name__icontains=search_query) #search the skill asked in the skill db (thst y we imported skill at top)

    #profiles = Profile.objects.all()
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
        )
    return profiles,search_query
