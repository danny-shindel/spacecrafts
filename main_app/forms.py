from django.forms import ModelForm
from .models import Craft

class CraftForm(ModelForm):
    class Meta:
        model = Craft
        # fields = ['cargo_capacity', 'consumables', 'cost_in_credits', 'crew', 'length', 'manufacturer', 'max_atmosphering_speed', 'model', 'name', 'passengers', 'hyperdrive_rating', 'vehicle_class', 'starship_class', 'MGLT', 'sell_price', 'condition', 'description', 'mileage'] 
        exclude = ['url', 'user']

