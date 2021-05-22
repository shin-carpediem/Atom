from rest_framework import serializers
from users.models import House, User, Inquire, RequestChHouse, RequestHouseOwner
from app.models import HouseChore


# Create your models here.
# users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'house', 'house_common_fee', 'house_common_fee_date', 'housechore_title', 'housechore_desc', 'done_weekly', 'done_monthly', 'is_staff',
                  'is_active', 'date_joined')


class InquireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquire
        fields = ('id', 'email', 'session', 'content', 'created_at')


class RequestChHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestChHouse
        fields = ('id', 'email', 'current_house',
                  'request_house', 'created_at')


class RequestHouseOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestHouseOwner
        fields = ('id', 'email', 'house', 'created_at')


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('id', 'name', 'common_fee', 'common_fee_date', 'created_at')


class HouseChoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseChore
        fields = ('id', 'title', 'description', 'house')
