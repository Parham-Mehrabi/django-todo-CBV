from rest_framework import serializers
from ..models import Task
from account.models import CostumUser


class CostumeUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CostumUser
        fields = ('id', 'email', 'is_staff')


class TaskSerializer(serializers.ModelSerializer):
    # author = CostumeUserSerializer()
    # note:2
    # note:3
    task_absolute_url = serializers.SerializerMethodField(method_name='get_task_absolute_url', read_only=True)
    task_relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    # note:1

    class Meta:
        read_only_fields = ['author']
        model = Task
        fields = ('author', 'task_absolute_url', 'task_relative_url', 'title', 'context', 'is_complete', 'created')

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        return super().create(validated_data)

    def get_task_absolute_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('task_absolute_url', None)
            rep.pop('task_relative_url', None)
        else:
            rep.pop('context', None)

        rep['author'] = CostumeUserSerializer(instance.author, context={'request': request}).data
        # note:4
        return rep


"""
NOTES:
1:
    #1: task_absolute_url use's the method declared in serializer however rask_relative_url use's the model's method
    (URLField vs SerializerMethodField)

    #2: if we don't specify the name of method for SerializerMethodField, by default it expect us to have a method in
    serializer with as follows : 'get_field-name' like get_task_absolute_url


2:
    when we call a serializer on another serializer we dont have the access to the request object in called serializer,
    we should send a context that is like this: context = {'request': self.context.get('request')}
    
    
3:
    except of overriding this field here directly, we do it on to_representation,
     in this case we still use the author object's id for post requests but to represent it we send the object
     to its serializer
     
4:
    #1:
        if we hypothetically need request object in the called serializer(CostumeUserSerializer in this case),
         we should send the request object in the context just as we did here however we didnt use request in the
         CostumeUserSerializer yet
    #2:
        since the serializer itself returns a serializer object we should specify that we need its data here in the field
        so we add .data in the end
     
"""