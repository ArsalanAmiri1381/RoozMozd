from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, OTP
# Register your models here.


# ----------------------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'role')
    list_filter = ('role', 'is_verified')
    search_fields = ('username', 'phone_number')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('role', 'is_verified')}),
        ('سطوح دسترسی', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('زمان‌ها', {'fields': ('last_login', 'created_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'is_verified', 'is_staff', 'is_superuser'),
        }),
    )

# ----------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','phone_number',)
    search_fields = ('user__username', 'phone_number')

# ----------------------------
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'code', 'created_at', 'is_used']
    list_filter = ['is_used']
    search_fields = ['phone_number']
