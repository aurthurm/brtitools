from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'get_full_name',
            'email',
        ]
        read_only_fields = ['id', 'username', 'get_full_name']


class ExtraTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['user'] = {
            'username': self.user.username,
            'user_id': self.user.pk,
            # 'user_groups' : self.user.groups.values_list('name', flat=True)
        }
        return data