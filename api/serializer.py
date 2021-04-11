from rest_framework import serializers
from users.models import User, House
from app.models import HouseChore


# Create your models here.
# users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'house', 'house_common_fee', 'house_common_fee_date', 'housechore_title', 'housechore_desc', 'done_weekly', 'done_monthly', 'is_staff',
                  'is_active', 'date_joined')


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('id', 'name', 'common_fee', 'common_fee_date', 'created_at')


class HouseChoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseChore
        fields = ('title', 'description', 'house')
