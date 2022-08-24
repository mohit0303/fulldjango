from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project    #we r importing the project model bcz we will be showing d user all the projects we r having




@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': 'api/projects'},
        {'GET': 'api/projects/id'}, 
        {'POST': 'api/projects/id/vote'},
        {'POST': 'api/users/token'},
        {'POST': 'api/users/token/refresh'},
    ]

    return Response(routes)

@api_view(['GET'])   #we r adding ths decorator bcz we r letting it know what type of call we r making in ths function. there is also a class way & a function way
@permission_classes([IsAuthenticated]) #is used for JWT token and for allowing only authenticated user to use our api to see all peoject list [ths is also called as restricted route]
def getProjects(request):
    print("USER---->",request.user)
    projects = Project.objects.all() #first getting all the list of projects we have in project variable
    serializer = ProjectSerializer(projects,many=True) #serializing the list of project we took in above line i.e converting it to json object
    return Response(serializer.data)  #onc all the peoject list is serialized/jsonified using inbuilt function .data and returning it

#the above function/view will gv us the list of all our project on front end, but we hav serialized the project not all its object so we will gt like tag id not tag nams,owner ids not name
#so we will create below single project function where we will pass a project id an will get all the data for tht singl project



@api_view(['GET']) 
def getProject(request,pk):      #as this function is for a singl paticular project we will pass tht project id too 
    project = Project.objects.get(id = pk) #so we r getting only tht paticular project wth id we got from our url & passing it here
    serializer = ProjectSerializer(project,many=False)  #now its false as its for only one project
    return Response(serializer.data)  


