from rest_framework import routers
from .views import TweetViewSet

router = routers.DefaultRouter()
router.register(r'tweets', TweetViewSet, basename='tweet')

urlpatterns = router.urls
