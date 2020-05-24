from rest_framework import serializers
from .models import User, UserBill, Group, GroupBill, GroupMember, Bill


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBill
        fields = '__all__'

class GroupBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupBill
        fields = '__all__'


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = '__all__'


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'
