from rest_framework import serializers
from .models import *

class Itemserializer(serializers.ModelSerializer):
    class Meta:
        model= Items
        fields= '__all__'

        #kjfkdjglkbjfllkldsfkoktdgokook
        print('samuel')