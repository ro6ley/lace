from rest_framework import serializers

from .models import Template


class TemplateSerializer(serializers.ModelSerializer):
    """ Serializer to map the Template model instance into JSON format.
    """
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Template
        fields = ('id', 'title', 'content', 'owner', 'is_private', 
                  'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
