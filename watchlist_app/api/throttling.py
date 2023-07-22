from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class ReviewCreateThrottle(UserRateThrottle):
    scope = 'review-create'


class ReviewListThrottle(AnonRateThrottle):
    scope = 'review-list'