from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from watchlist_app import models
from watchlist_app.api import permissions as custom_permissions
from watchlist_app.api import serializers, throttling


class UserReview(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer
    
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return models.Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewCreateThrottle]

    def get_queryset(self):
        return models.Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = models.WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = models.Review.objects.filter(watchlist=movie, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError('You have already reviewed this movie!', code=status.HTTP_400_BAD_REQUEST)

        if movie.number_of_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2

        movie.number_of_rating += 1
        movie.save()

        serializer.save(watchlist=movie, review_user=review_user)


class ReviewList(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer
    throttle_classes = [throttling.ReviewListThrottle, throttling.AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [custom_permissions.IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
    queryset = models.StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformSerializer
    permission_classes = [custom_permissions.IsReviewUserOrReadOnly]
    throttle_classes = [throttling.AnonRateThrottle]


class WatchListAV(APIView):
    permission_classes = [custom_permissions.IsAdminOrReadOnly]

    def get(self, request: Request):
        movies = models.WatchList.objects.all()
        serializer = serializers.WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request: Request):
        serializer = serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchDetailAV(APIView):
    permission_classes = [custom_permissions.IsAdminOrReadOnly]

    def get(self, request: Request, pk: int):
        try:
            movie = models.WatchList.objects.get(pk=pk)
        except models.WatchList.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request: Request, pk: int):
        movie = models.WatchList.objects.get(pk=pk)
        serializer = serializers.WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request: Request, pk: int):
        movie = models.WatchList.objects.get(pk=pk)
        movie.delete()
        return Response({'msg': 'Movie Deleted'}, status=status.HTTP_204_NO_CONTENT)
