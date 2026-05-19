from rest_framework import serializers

from users.models import NewUser
from .models import Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('email', 'user_name', 'first_name')
class TaskSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    class Meta:
        model = Task
        fields= '__all__'

class UserWithTasksSerializer(serializers.ModelSerializer):
 tasks= TaskSerializer(many=True, read_only=True)    
 class Meta:
    model = NewUser
    fields=('email','user_name','first_name','tasks') 

    #USERID related tasks show korar jonno serializer jelkhane post e userid pass korle get e oi userid related task show korbe. TaskSerializer e user field ta read_only=True kore deya hoyeche, jate user field ta automatically set hoye jai, and client ke explicitly provide korte na hoy.


class TaskList2Serializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    user_id= serializers.PrimaryKeyRelatedField(
    queryset=NewUser.objects.all(),
    source='user',
    write_only=True
    )  
    class Meta:
        model = Task
        fields= '__all__'

        # small serializer for list
class MiniTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields= ('id', 'title')        