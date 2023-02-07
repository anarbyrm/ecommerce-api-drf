from rest_framework import views, permissions, status, generics
from rest_framework.response import Response
from accounts.api.serializers import UserSerializer
from accounts.models import User


class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
        