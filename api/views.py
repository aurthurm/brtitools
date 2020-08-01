
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, serializers
from rest_framework.fields import CurrentUserDefault
from .cross_serialisers import ExtraTokenObtainPairSerializer
from .cross_serialisers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view



class ExtraTokenObtainPairView(TokenObtainPairView):
    serializer_class = ExtraTokenObtainPairSerializer


class GetUserAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view()
def get_user_data(request):
    user = None
    user = CurrentUserDefault()
    # print(f"CurrentUserDefault : {user}")
    if user is None:
        user = request.user
        # print(f"request : {user}")
    user2 = serializers.CurrentUserDefault()
    # print(f"Ser : {request.user}")
    serializer = UserSerializer(user)
    return Response(serializer.data)