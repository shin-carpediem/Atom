from rest_framework import serializers
from users.models import User, House, UserAndHouse


# Create your models here.
# users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'is_staff',
                  'is_active', 'date_joined')


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('id', 'name', 'created_at')


class UserAndHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAndHouse
        fields = ('id', 'user', 'house', 'created_at')
