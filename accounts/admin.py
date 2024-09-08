from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
  list_display = (
    "username",
    "is_staff",
    "is_superuser",
  )

  fieldsets = (
    ("基本情報", {"fields": ("username", "password")}),
    (
      "権限情報",
      {
        "fields": (
          "is_staff",
          "is_superuser",
          "groups",
          "user_permissions",
        ),
      },
    ),
    ("日時情報" , {"fields": ["last_login"]}),
  )

admin.site.register(CustomUser, CustomUserAdmin)