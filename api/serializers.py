#we create a url/api named as project,profile and all so tht we get data of these things on frontend
#when we hit the url like projects we get list of project but we need to searilz tht list so we create a class ProjectSearilize and pass the DB/Table project in the class
#the plist of project we got has all the data but the owner names,tags names are object id not d name, so we create class for thm and serialize it as well


from rest_framework import serializers
from projects.models import Project, Tag,Review #calling the model/Table here which we want to serialize are inside the project folder and in the model.py
from users.models import Profile                 #bcz all the users Profiles are in the user folder


#3.to get the Reviews from table and get it serialize/jsonified we created ths class,now we will use a serilz method field to use ot in the Projectserialz class
#4. so now the in ProjectSerilaz class we will use a SerializeMethodField() where we can get reviews by creating a function only for reviews
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


#1.as project model hav owner,tags linked in it, we will pass these 2 in it as well to make a relation
#2.IMP as we r calling ProfileSerializr and tagserializer and reviewselizaer in the below class, thy need to be declared/created bfr ths class
class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False) #many is false as only one owner will be there
    tags = TagSerializer(many=True)       #many is true bcz multuiple tags(react,python) can be there in a project
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project      #passing teh value.name of the model we need to serialize
        fields = '__all__'   #passing the fields of tht model/table we want to pass/return
                             #so here the model/table named Project will be serialized i.e all its field will be converted into json oject as we need to pass it to front end

    #by default to use SerializerMethodField all the fun created will start by "get_" and thn the name of tag whatevr we are fetching
    def get_reviews(self,obj):   #here ths self is not pointing to the model, it is pointing to the ProjectSerializer class & obj will be the object we r serialzing i.e the Projct 
        reviews = obj.review_set.all() #getting all the reviews
        serializer = ReviewSerializer(reviews,many=True) #serializng all the reviews by calling ReviewSerializer class created above, it has to be created up els it wont know what is Reveiwserilzr class is
        return serializer.data





