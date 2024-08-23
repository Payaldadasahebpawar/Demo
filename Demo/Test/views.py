from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Name
from .serializers import UserAccountSerializer,UserLoginSerializer,TokenSerializer,UserNameSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserAccountSerializer

class RegisterView(APIView):


    def post(self, request):
        serializer = UserAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            # Handle the deletion of the name if validation fails
            if 'name' in request.data:
                name_data = request.data['name']
                Name.objects.filter(first_name=name_data.get('first_name'), last_name=name_data.get('last_name')).delete()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = []
       
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        
        token_serializer = TokenSerializer(data={
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
        token_serializer.is_valid()
        return Response(token_serializer.data, status=status.HTTP_200_OK,data={'message':'user login successfully','Status':'Success','code':'200','data':serializer.data})        
        # return Response(data={'message': 'User created Successfully.','status':'Success',"code": 201,"content_type":"null","error": {},'data': serializer.data,}, status=status.HTTP_201_CREATED)


class UserListView(generics.ListAPIView):
    queryset = Name.objects.all()
    serializer_class = UserNameSerializer
    # filterset_fields = ['first_name','last_name']   
    authentication_classes = []  # No authentication required
    permission_classes = []    
    
    
    
    