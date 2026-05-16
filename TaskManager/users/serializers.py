from rest_framework import serializers
from .models import NewUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('email', 'user_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    # def validate_email(self, value):

    #     if NewUser.objects.filter(email=value).exists():
    #         raise serializers.ValidationError(
    #             "User with this email already exists."
    #         )

    #     return value
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance