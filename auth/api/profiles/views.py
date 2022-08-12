from profiles.serializers import ProfileSerializer, ProfileListSerializer

from profiles.models import Profile

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status


class UserProfileView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request): 
        try: 
            request.data["user"] = request.user.id
            serializer = ProfileSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = {
                'data': serializer.data,
                'msg': 'Perfil creado exitosamente.'
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except: 
            return Response({'msg':'Contáctese con el usuario administrador.'}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request): 
        profile = Profile.objects.filter(user = request.user.id, status_delete=False)
        serializer = ProfileListSerializer(profile, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    def patch(self, request, id): 
        try: 
            profile = Profile.objects.get(user = request.user.id, id=id)
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if profile.status_delete: 
                    profile.status_delete = True
                    return Response({'msg':'No se ha encontrado el perfil solicitado.'}, status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            data = {
                'data': serializer.data, 
                'msg': 'Perfil actualizado exitosamente.'
            }
            return Response(data, status=status.HTTP_200_OK)
        except: 
            return Response({'msg':'Perfil no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    
    def delete(self, request, id): 
        try: 
            profile = Profile.objects.get(user = request.user.id, id=id)
            if profile.status_delete: 
                profile.status_delete = True
                return Response({'msg':'El perfil ya ha sido eliminado.'}, status=status.HTTP_404_NOT_FOUND)
            profile.status_delete = True
            profile.save()
            return Response({'msg':'Se ha eliminado el perfil exitosamente.'}, status=status.HTTP_200_OK)
        except: 
            return Response({'msg':'Perfil no encontrado.'}, status=status.HTTP_404_NOT_FOUND)