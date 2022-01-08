from rest_framework import serializers

from .models import Backup


class BackUpSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Backup
        fields = ['app', 'total_size', 'total_files', 'server', 'status', 'log']
