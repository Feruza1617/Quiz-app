from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from account.models import Account


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=3, max_length=16, write_only=True)
    password2 = serializers.CharField(min_length=3, max_length=16, write_only=True)

    class Meta:
        model = Account
        fields = ('id', 'full_name', 'phone', 'password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError({
                "success": False,
                "message": "Password did not match, please try again!"
            })
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        return Account.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=16, required=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.CharField(max_length=100, read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)

    def get_token(self, obj):
        user = Account.objects.filter(phone=obj.get('phone')).first()
        return user.token

    def get_full_name(self, obj):
        user = Account.objects.filter(phone=obj.get('phone')).first()
        return user.full_name

    def get_image_url(self, obj):
        user = Account.objects.filter(phone=obj.get('phone')).first()
        return user.image_url

    class Meta:
        model = Account
        fields = ('token', 'id', 'phone', 'password', 'full_name', 'image_url')

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        user = authenticate(phone=phone, password=password)
        if not user:
            raise AuthenticationFailed({
                'message': 'Phone or password is not correct'
            })
        if not user.is_active:
            raise AuthenticationFailed({
                'message': 'Account disabled'
            })

        data = {
            'success': True,
            'token': user.token,
            'phone': user.phone,
            'full_name': user.full_name,
            'image_url': user.image_url,
            'id': user.id
        }
        return data


class AccountSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display')

    class Meta:
        model = Account
        fields = (
            'id',
            'phone',
            'full_name',
            'gender',
            'avatar',
            'date_login'
        )
        extra_kwargs = {
            'is_active': {'read_only': True}
        }


class ChangeNewPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(min_length=3, max_length=64, write_only=True)
    password = serializers.CharField(min_length=3, max_length=64, write_only=True)
    password2 = serializers.CharField(min_length=3, max_length=64, write_only=True)

    class Meta:
        model = Account
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                {'success': False, 'message': 'Old password did not match, please try again new'})

        if password != password2:
            raise serializers.ValidationError(
                {'success': False, 'message': 'Password did not match, please try again new'})

        user.set_password(password)
        user.save()
        return attrs


