from .models import CustomUser
from django.conf import settings
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegisterSerializer, UserProfileSerializer, UserProfile
from django.contrib.auth import authenticate
from rest_framework.response import Response
from chatapi.custom_methods import IsAuthenticatedCustom
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.db import IntegrityError
from rest_framework.viewsets import ModelViewSet
import re
from django.db.models import Q, Count, Subquery, OuterRef
import jwt


# def decodeJWT(bearer):
#     if not bearer:
#         return None

#     token = bearer[7:]
#     decoded = jwt.decode(token, key=settings.SECRET_KEY)
#     if decoded:
#         try:
#             return CustomUser.objects.get(id=decoded["user_id"])
#         except Exception:
#             return None
        
class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, 
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'])

        if not user:
            return Response({"error": "Invalid email or password"}, status="400")

        refresh = RefreshToken.for_user(user)
        
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id" : user.id
        })



class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.pop("username")

        CustomUser.objects.create_user(username=username, **serializer.validated_data)

        return Response({"success": "User created."}, status=201)
    


class UserProfileView(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedCustom]
    
    def get_queryset(self):
        data = self.request.query_params.dict()
        keyword = data.get("keyword", None)
        
        if keyword:
            search_fields = {
                "user__username" , "first_name", "last_name"
            }
            
            query = self.get_query(keyword, search_fields)
            return self.queryset.filter(query).distinct()
        
        return self.queryset
    
    @staticmethod
    def get_query(query_string, search_fields):
        query = None  # Query to search for every search term
        terms = UserProfileView.normalize_query(query_string)
        for term in terms:
            or_query = None  # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
        return query
    
    @staticmethod
    def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]
    

class MeView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserProfileSerializer

    def get(self, request):
        user_id = request.user.id
        return Response({"id": user_id}, status=200)