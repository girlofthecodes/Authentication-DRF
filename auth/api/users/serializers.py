from users.models import User

#Imports for the validators
from rest_framework.serializers import ValidationError 
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed
#from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import password_validation


class UserSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, 
        validators = [UniqueValidator(queryset=User.objects.all(), message={'msg': 'El usuario ya existe. Introduzca un nombre de usuario distinto.'})]
    )
    email = serializers.EmailField(
        required=True, 
        validators = [UniqueValidator(queryset=User.objects.all(), message={'msg':'Este email ya existe. Introduzca un email distinto.'})]
    )
    class Meta:
        model = User
        fields = [
            'id', #Muestra el id del usuario
            'username',
            'email',
            'password',
            'is_active',
            'is_verified',
            'created_at',
            'updated_at',
        ]

        extra_kwargs = {
            'password':{
                'write_only':True
            }
        }

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]-./=¿?<>]"


        if len(username) < 6: 
            raise ValidationError({"msg":"El nombre de usuario debe tener un mínimo de 6 caracteres"})

        if len(username) > 20: 
            raise ValidationError({'msg':'El nombre de usuario debe tener un máximo de 20 caracteres'})

        if any(i.isspace() for i in username):
            raise ValidationError({'msg':'El nombre de usuario no admite espacios'})

        if any(i in special_characters for i in username): 
           raise ValidationError({'msg':'El nombre de usuario no admite caracteres especiales'})

        if any(i.isspace() for i in username):
            raise ValidationError('El nombre de usuario no admite espacios')

        if not any(i.isalpha() for i in password):
            raise ValidationError({'msg':'La contraseña debe incluir al menos una letra'})
        
        if not any(i.isupper() for i in password):
            raise ValidationError({'msg':'La contraseña debe incluir al menos una letra mayúscula'})
        
        if not any(i.isdigit() for i in password):
            raise ValidationError({'msg':'La contraseña debe incluir al menos un dígito'})
        
        if not any(i in special_characters for i in password): 
            raise ValidationError({'msg':'La contraseña debe incluir al menos un caracter especial'})

        if any(i.isspace() for i in password): 
            raise ValidationError({'msg':'La contraseña no debe incluir espacios'})

        if len(password) > 20:
            raise ValidationError({'msg':'La contraseña debe tener un máximo 20 caracteres'})
        
        if len(password) < 6:
            raise ValidationError({'msg':'La contraseña debe tener un mínimo de 6 caracteres'})
        
        return super(UserSignUpSerializer, self).validate(data)

        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSignUpSerializer, self).create(validated_data)

#Inicio de sesión
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, max_length=20)
    

    class Meta: 
        model = User
        fields = [
            'email', 
            'password',
            'is_active',
            'is_verified',
        ]
        

#Solicitud de restablecimiento de contraseña por email
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

#Datos que se ingresaran para poder realizar el restablecimiento de contraseña alusuario bloqueado 
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=20, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True) #Token para comprobar que la contraseña es correcta
    uidb64 = serializers.CharField(min_length=1, write_only=True) #El id del usuario codificado en base 64

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('El enlace de reinicio no es válido.')

            user.set_password(password)
            user.is_active = True
            user.save()
            return (user)
        except Exception:
            raise AuthenticationFailed('El enlace de reinicio no es válido.')

class ChangeNewPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(min_length=6, max_length=20, write_only=True) #Contraseña actual
    new_password = serializers.CharField(min_length=6, max_length=20, write_only=True)  
    confirm_password = serializers.CharField(min_length=6, max_length=20, write_only=True)
    
    class Meta:
        fields = [
            'current_password',
            'new_password',
            'confirm_password'
            ]

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise AuthenticationFailed({'msg':'La contraseña actual no coincide.'})
        return value

    def validate(self, data):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]-./=¿?<>]"

        if not any(i.isalpha() for i in data['new_password']): 
                raise ValidationError({'msg':'La contraseña debe contener al menos una letra.'})
        
        if not any(i.isupper() for i in data['new_password']):
            raise ValidationError({'msg':'La contraseña debe incluir al menos una letra mayúscula'})
        
        if not any(i.isdigit() for i in data['new_password']):
            raise ValidationError({'msg':'La contraseña debe incluir al menos un dígito'})
        
        if not any(i in special_characters for i in data['new_password']): 
            raise ValidationError({'msg':'La contraseña debe incluir al menos un caracter especial'})

        if any(i.isspace() for i in data['new_password']): 
            raise ValidationError({'msg':'La contraseña no debe incluir espacios'})

        if len(data['new_password']) > 20:
            raise ValidationError({'msg':'La contraseña debe tener un máximo 20 caracteres'})
        
        if len(data['new_password']) < 6:
            raise ValidationError({'msg':'La contraseña debe tener un mínimo de 6 caracteres'})

        if data['new_password'] != data['confirm_password']:
            raise AuthenticationFailed({'msg':"Las contraseñas no coinciden."})

        if data['new_password'] == data['current_password']: 
            raise ValidationError({'msg':'Esta contraseña ya ha sido usada. Prueba una diferente.'})
        password_validation.validate_password(data['new_password'], self.context['request'].user)
        return data
          

        
        