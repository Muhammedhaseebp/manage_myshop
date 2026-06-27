from rest_framework import serializers
from .models import Recharge

class RechargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recharge
        fields = "__all__"
