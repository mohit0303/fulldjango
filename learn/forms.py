from dataclasses import field
from django import forms
from django.forms import ModelForm, modelformset_factory
from django import forms
from projects.models import Project



class ProjectForm(ModelForm):
    class Meta:
        model= Project
        #fields= '__all__'
        fields = ['title','featured_image','description','demo_link','source_link','tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
    def __init__(self,*args,**kwargs):
        super(ProjectForm,self).__init__(*args,**kwargs)
        #self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add Title'})
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


