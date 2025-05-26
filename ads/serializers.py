from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class AdSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Ad
        fields = ['id', 'user', 'title', 'description', 'image_url',
                 'category', 'condition', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ExchangeProposalSerializer(serializers.ModelSerializer):
    ad_sender = AdSerializer(read_only=True)
    ad_receiver = AdSerializer(read_only=True)
    ad_sender_id = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(), write_only=True, source='ad_sender'
    )
    ad_receiver_id = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(), write_only=True, source='ad_receiver'
    )

    class Meta:
        model = ExchangeProposal
        fields = ['id', 'ad_sender', 'ad_receiver', 'ad_sender_id',
                 'ad_receiver_id', 'comment', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

    def validate(self, data):
        if data['ad_sender'].user != self.context['request'].user:
            raise serializers.ValidationError(
                "Вы можете создавать предложения обмена только для своих объявлений"
            )
        if data['ad_sender'] == data['ad_receiver']:
            raise serializers.ValidationError(
                "Нельзя создать предложение обмена на то же самое объявление"
            )
        return data 