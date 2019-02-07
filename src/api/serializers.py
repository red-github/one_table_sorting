from rest_framework import serializers
from .models import Module


class SubModuleField(serializers.Field):

    def to_representation(self, value):

        list_sub_module = Module.objects.filter(
            parent_id=value.id
        ).values('id', 'name').order_by('sort_id')

        return list_sub_module


class ModuleSerializer(serializers.ModelSerializer):

    sub_module = SubModuleField(source='*', read_only=True)

    class Meta:
        model = Module
        fields = ('id', 'name', 'parent_id', 'sort_id', 'sub_module',)

    def create(self, validated_data):

        current_list = Module.objects.filter(
            parent_id=validated_data['parent_id']
        ).values(
            'id', 'name', 'parent_id', 'sort_id'
        ).order_by('parent_id', 'sort_id')

        new_list = []

        if current_list.count() == 0:
            instance = Module.objects.create(
                name=validated_data['name'],
                parent_id=validated_data['parent_id'],
                sort_id=1
            )

        else:

            for data in current_list:
                new_list.append(data)

            module_reindex = validated_data

            if module_reindex['sort_id'] > len(current_list):
                index = len(current_list)
                # counter = 0
            else:
                index = module_reindex['sort_id'] - 1

            new_list.insert(index, module_reindex)

            counter = 1

            for data in new_list:
                try:
                    Module.objects.filter(id=data['id']).update(
                        sort_id=counter, parent_id=data['parent_id']
                    )
                except KeyError:
                    instance = Module.objects.create(
                        name=validated_data['name'],
                        parent_id=validated_data['parent_id'],
                        sort_id=counter
                    )

                counter = counter + 1

        return instance

    def update(self, instance, validated_data):

        current_list = Module.objects.filter(
            parent_id=validated_data['parent_id']
        ).values(
            'id', 'name', 'parent_id', 'sort_id'
        ).order_by('parent_id', 'sort_id')

        counter = 1
        new_list = []
        module_index = 0

        for data in current_list:

            if data['id'] == instance.id:
                module_index = counter
            new_list.append(data)
            counter = counter + 1

        if module_index != 0:

            module_index = module_index
            module_reindex = new_list.pop(module_index - 1)

        else:

            validated_data['id'] = instance.id
            module_reindex = validated_data

        new_list.insert(validated_data['sort_id'] - 1, module_reindex)

        counter = 1

        for data in new_list:

            Module.objects.filter(id=data['id']).update(
                sort_id=counter, parent_id=validated_data['parent_id']
            )
            counter = counter + 1

        instance = Module.objects.get(id=instance.id)

        return instance
