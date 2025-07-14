from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from users.models import Employee, Position
from teams.models import Team

User = get_user_model()


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'name')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name')


class EmployeeSerializer(serializers.ModelSerializer):
  
    full_name = serializers.CharField(source='employe.get_full_name', read_only=True)
    username = serializers.CharField(source='employe.username', read_only=True)
    position_name = serializers.CharField(source='position.name', read_only=True)
    team = TeamSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), source='team', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'username', 'position', 'position_name', 'team', 'team_id']
        read_only_fields = ['id', 'full_name', 'username', 'position_name', 'team']


# ... (imports)

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não conferem."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        user = User.objects.create_user(**validated_data)
        
        return user


class UserProfileSerializer(serializers.ModelSerializer):

    employee_profile = EmployeeSerializer(read_only=True) 

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'employee_profile')
        read_only_fields = ('username', 'email', 'is_staff', 'is_superuser')
