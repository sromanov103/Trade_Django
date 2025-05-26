from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее только владельцам объекта редактировать его.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class AdViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с объявлениями.
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'category']
    ordering_fields = ['created_at', 'title']

    def get_queryset(self):
        queryset = Ad.objects.all()
        category = self.request.query_params.get('category', None)
        condition = self.request.query_params.get('condition', None)

        if category:
            queryset = queryset.filter(category=category)
        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с предложениями обмена.
    """
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ExchangeProposal.objects.filter(
            Q(ad_sender__user=user) | Q(ad_receiver__user=user)
        )

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Принять предложение обмена"""
        proposal = self.get_object()
        if proposal.ad_receiver.user != request.user:
            return Response(
                {"error": "Только получатель предложения может его принять"},
                status=403
            )
        proposal.status = 'accepted'
        proposal.save()
        return Response({"status": "Предложение принято"})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Отклонить предложение обмена"""
        proposal = self.get_object()
        if proposal.ad_receiver.user != request.user:
            return Response(
                {"error": "Только получатель предложения может его отклонить"},
                status=403
            )
        proposal.status = 'rejected'
        proposal.save()
        return Response({"status": "Предложение отклонено"})
