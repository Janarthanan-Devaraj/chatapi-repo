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
    email = serializers.EmailField()
    
    class Meta:
        model = User
        fields = "__all__"
    
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
        message = Message.objects.filter(sender_id=obj.user.id, receiver_id = user_id, is_read=False).distinct()
        
        return message.count()
    

class FavoriteSerializer(serializers.Serializer):
    favorite_id = serializers.IntegerField()