from django import forms
from django.core.checks.messages import Error
from django.db.models import fields
from django.forms.widgets import HiddenInput
from .models import AuctionList, Bid, Category, Comments, User

class AuctionForm(forms.ModelForm):
    #*****************************************************************************************
    #************************* OVER RIDING THE DEFAULT FORM "STYLE" IN ***********************
    #************************************MODEL FORMS******************************************
    #*****************************************************************************************
    
    name         = forms.CharField(label='',widget=forms.TextInput(attrs={"placeholder":"Your titile for the product"}))
    description  = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Description",
                "class" : "justify-content-center col-4 form-control",
                "id": "AuctionFormid",
                "rows":8,
                "cols": 1
            }
        )
    )
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    initial_bid       = forms.DecimalField()
    image_link1 = forms.CharField(max_length=100,required=False)
    image_link2 = forms.CharField(max_length=100,required=False)
    image_link3 = forms.CharField(max_length=100,required=False)
    image_link4 = forms.CharField(max_length=100,required=False)
    image_link5 = forms.CharField(max_length=100,required=False)

    #*******************************************************************************
    #*******************************************************************************
    #*******************************************************************************
    
    """ The fields in class meta are the ones that are send to the backend so if you
        want to add any new field in the forms in actuall project not for testing then
        you will have to migrate the database model again and then add it to class meta 
        else you will get error
        BUT
        for just testing an field not associating a backend with it then just add the 
        field above but dont add it to class meta """
    class Meta:
        model = AuctionList
        fields =[
            'name',
            'description',
            'category',
            'initial_bid',
            'image_link1',
            'image_link2',
            'image_link3',
            'image_link4',
            'image_link5'
        ]
    
class Bidform(forms.ModelForm):
    amount = forms.DecimalField(decimal_places = 2, max_digits=1000 ,widget=forms.NumberInput(
            attrs={
                "placeholder": "Your bid must be higher than the current bid",
                "class" : "form-control",
            }
        ))

    class Meta:
        model = Bid
        fields = [
            'amount'
        ]

class AuctionWatchers(forms.ModelForm):
    watchers = forms.ModelMultipleChoiceField(
        queryset = User.objects.all(),
        widget = forms.CheckboxSelectMultiple
    )

    class Meta:
        model = AuctionList
        fields = [
            'watchers'
        ]

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Write your comment here",
                "class" : "form-control",
                "id": "commentFormid",
                "rows":2,
                "cols": 50
            }
        )
    )

    class Meta :
        model = Comments
        fields = [
            'comment'
        ]

    def clean_comment(self,*args,**kwargs):
        comment = self.cleaned_data.get("comment")
        if len(comment)==0 and (not comment.isspace()):
            raise forms.ValidationError("Hey you cant submit an empty comment")
        else:
            return comment









    """ THIS IS THE FUNCTION THAT CAN DO ACTUAL BACKEND VERIFICATION LIKE LENGHT OF PHONE NUMBER WHETHER @ IS IN EMAIL """
    # def clean_<NAME OF FIELD TO VALIDATE>(self,*args,**kwargs):
    # def clean_title(self,*args,**kwargs):
    #     title = self.cleaned_data.get("title")
    #     if not "samsung" in title:
    #         raise forms.ValidationError("Only samsung products allowed")
    #     else:
    #         return title