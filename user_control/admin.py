from django.contrib import admin
from .models import (CustomUser, UserProfile,Favorite )

admin.site.register((CustomUser, UserProfile, Favorite))
