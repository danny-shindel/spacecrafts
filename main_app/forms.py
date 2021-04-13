from django.forms import ModelForm
from .models import Craft

class CraftForm(ModelForm):
    class Meta:
        model = Craft
        fields = "__all__" 

        
