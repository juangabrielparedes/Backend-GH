from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from apps.users.models import User
from apps.users.api.serializers import UserSerializer, TestUserSerializer

@api_view(['GET', 'POST'])
def user_api_view(request):
    
    #Listar usuarios
    if request.method == 'GET':
        #Consulta a la base de datos
        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)
        
        test_data = {
            'name': 'Eduardo',
            'email': 'Eduardo@gmail.com'
        }
        
        test_user = TestUserSerializer(data = test_data)
        if test_user.is_valid():
            print('Paso la validacion')
        
        return Response(users_serializer.data, status= status.HTTP_200_OK)
    #Crear usuario
    elif request.method == 'POST':
        users_serializer = UserSerializer(data = request.data)
        #Validar si los datos son validos
        if users_serializer.is_valid():
            users_serializer.save()
            return Response({'message':'Usuario creado correctamente!'}, status = status.HTTP_201_CREATED)
        return Response(users_serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api_view(request, pk=None):
    #Consultar si existe el usuario
    user = User.objects.filter(id=pk).first()
    #Validar si existe el usuario
    if user:
        #Validar si el metodo es GET
        if request.method == 'GET':
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status= status.HTTP_200_OK)
        #si se actualiza el usuario
        elif request.method == 'PUT':
            user_serializer = UserSerializer(user,data = request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status= status.HTTP_200_OK)
            return Response(user_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        # si elimina el ususario
        elif request.method == 'DELETE':
            user.delete()
            return Response({'menssage':'Usuario eliminado correctamente!'}, status= status.HTTP_200_OK)
        
    return Response({'menssage':'No se ha encontrado un usuario con estos datos!'}, status= status.HTTP_400_BAD_REQUEST)