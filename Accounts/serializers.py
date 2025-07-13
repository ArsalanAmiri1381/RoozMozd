# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser, UserProfile, OTP


#---------------------------------  Models Serializer  -------------------------------------------


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'is_active']
        read_only_fields = ['is_active']

class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['user', 'address', 'phone_number', 'profile_image', 'national_id', 'birth_date']


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['id', 'user', 'code', 'created_at', 'is_verified']
        read_only_fields = ['created_at', 'is_verified']


#---------------------------------  OTP Verify Serializer  -------------------------------------------


class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        phone = attrs.get('phone_number')
        code = attrs.get('code')
        try:
            otp = OTP.objects.filter(phone_number=phone, code=code, is_used=False).latest('created_at')
        except OTP.DoesNotExist:
            raise serializers.ValidationError("Wrong code entered")

        attrs['otp'] = otp
        return attrs

    def save(self):
        otp = self.validated_data['otp']
        otp.is_used = True
        otp.save()
        return otp.phone_number


#---------------------------------  SignUp Serializer  -------------------------------------------

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'password','phone_number' ,'email' , 'national_id']

    def validate_phone_number(self, value):
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user



#---------------------------------  Complete SignUp Serializer  -------------------------------------------


class CompleteRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'phone_number', 'national_id', 'first_name', 'last_name']

    def validate_phone_number(self, value):

        if not OTP.objects.filter(phone_number=value, is_used=True).exists():
            raise serializers.ValidationError("Phone Number is not Verified or Invalid")
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists")
        return value



    def create(self, validated_data):
        password = validated_data.pop('password')
        phone_number = validated_data.pop('phone_number')

        user = CustomUser.objects.create_user(
            phone_number=phone_number,
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user
