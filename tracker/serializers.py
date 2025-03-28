from .models import TrackerModel
from rest_framework import serializers
from datetime import datetime, timedelta

class TrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackerModel
        fields = "__all__"
    
    def update(self, instance, validated_data):
        if 'end_time' in validated_data:
            instance.end_time = validated_data["end_time"]
            instance.duration = instance.end_time - instance.start_time
            instance.save()
        return instance
        
