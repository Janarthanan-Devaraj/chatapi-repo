from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile, CustomUser
from message_control.serializers import GenericFileUploadSerializer
from django.db.models import Q

User = get_user_model()
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}
    
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def validate(self, attrs):
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = ("password", )

class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    profile_picture = GenericFileUploadSerializer(read_only=True)
    profile_picture_id = serializers.IntegerField(
        write_only=True, required=False)
    message_count = serializers.SerializerMethodField("get_message_count")
    
    class Meta:
        model = UserProfile
        fields = "__all__"
        
    def get_message_count(self, obj):
        try:
            user_id = self.context("request").user.id
        except Exception as e:
            user_id = None
        
        from message_control.models import Message
        message = Message.objects.filter(Q(sender_id=user_id, receiver_id = obj.user.id) | Q(
            sender_id=obj.user.id, receiver_id=user_id)).distinct()
        
        return message.count()