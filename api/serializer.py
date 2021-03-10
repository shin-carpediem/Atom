from rest_framework import serializers
from users.models import User


# Create your models here.
# users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'is_active',
                  'is_staff', 'date_joined')
