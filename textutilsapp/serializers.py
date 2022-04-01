from rest_framework import serializers


class FileSerializer(serializers.Serializer):
    chatfile = serializers.FileField(max_length=100)
