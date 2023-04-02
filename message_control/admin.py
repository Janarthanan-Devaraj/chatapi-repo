from django.contrib import admin
from .models import (GenericFileUpload, Message, MessageAttachment)

admin.site.register((GenericFileUpload, Message, MessageAttachment))
