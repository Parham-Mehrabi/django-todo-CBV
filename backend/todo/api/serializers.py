from rest_framework import serializers
from ..models import Task
from account.models import CostumUser


class CostumUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostumUser
        fields = ('id', 'email', 'is_staff')


class TaskSerializer(serializers.ModelSerializer):
    author = CostumUserSerializer()
    task_absolute_url = serializers.SerializerMethodField(method_name='get_task_absolute_url', read_only=True)
    task_relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    # #1: task_absolute_url use's the method declared in serializer however rask_relative_url use's the model's method
    # (URLField vs SerializerMethodField)
    #
    # #2: if we don't specify the name of method for SerializerMethodField, by default it expect us to have a method in
    # serializer with as follows : 'get_field-name' like get_task_absolute_url

    class Meta:
        model = Task
        fields = ('author', 'task_absolute_url', 'task_relative_url', 'title', 'context', 'is_complete', 'created')

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        return super().create(validated_data)

    def get_task_absolute_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
