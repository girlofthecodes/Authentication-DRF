from rest_framework import serializers
from rest_framework.serializers import ValidationError

from datetime import date

from profiles.models import Profile

from users.models import User



class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username', 
            'email',
        ]

class ProfileSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Profile
        fields = [
            'id', 
            'user', 
            'first_name', 
            'middle_name', 
            'first_surname',
            'second_surname',
            'birth_date',
            'age',
            'place_of_birth',
            'residence_place',
            'residence_country',
        ]

        extra_kwargs = {
            'middle_name': {'required': False},
            'second_surname': {'required': False},
            'age': {'required': False}, 
        }
        
    def to_representation(self, instance):
        data = super().to_representation(instance=instance)
        data['first_name'] = data['first_name'].title() if data['first_name'] else data['first_name']
        data['middle_name'] = data['middle_name'].title() if data['middle_name'] else data['middle_name']
        data['first_surname'] = data['first_surname'].title() if data['first_surname'] else data['first_surname']
        data['second_surname'] = data['second_surname'].title() if data['second_surname'] else data['second_surname']
        data['place_of_birth'] = data['place_of_birth'].upper() if data['place_of_birth'] else data['place_of_birth']
        data['residence_place'] = data['residence_place'].upper() if data['residence_place'] else data['residence_place']
        data['residence_country'] = data['residence_country'].upper() if data['residence_country'] else data['residence_country']
        return data

    def validate(self, data): 
        age = data.get('age')
        today = date.today()
        if today < data['birth_date']: 
            raise ValidationError({'msg':'Fecha de nacimiento no válida.'})
        age = today.year - data['birth_date'].year - ((today.month, today.day) < (data['birth_date'].month, data['birth_date'].day)) 
        data['age'] = age

        return data        

class ProfileListSerializer(serializers.ModelSerializer): 
    user = UserSignUpSerializer(read_only=True) 
    class Meta: 
        model = Profile
        fields = [
            'id', 
            'user', 
            'first_name', 
            'middle_name', 
            'first_surname',
            'second_surname',
            'birth_date',
            'age',
            'place_of_birth',
            'residence_place',
            'residence_country',
        ]

    def to_representation(self, instance):
        data = super(ProfileListSerializer, self).to_representation(instance=instance)
        data['first_name'] = data['first_name'].title() if data['first_name'] else data['first_name']
        data['middle_name'] = data['middle_name'].title() if data['middle_name'] else data['middle_name']
        data['first_surname'] = data['first_surname'].title() if data['first_surname'] else data['first_surname']
        data['second_surname'] = data['second_surname'].title() if data['second_surname'] else data['second_surname']
        data['place_of_birth'] = data['place_of_birth'].upper() if data['place_of_birth'] else data['place_of_birth']
        data['residence_place'] = data['residence_place'].upper() if data['residence_place'] else data['residence_place']
        data['residence_country'] = data['residence_country'].upper() if data['residence_country'] else data['residence_country']
        return data
