from django.conf.urls import url, include
from rest_framework import routers
from ezdict.translation.views import TranslationView
from ezdict.translation_history.views import TranslationHistoryViewSet
from ezdict.word.views import WordToLearnViewSet, WordIsLearnedViewSet

router = routers.DefaultRouter()
router.register(r'translation_history', TranslationHistoryViewSet)
router.register(r'word/learning', WordToLearnViewSet)
router.register(r'word/learned', WordIsLearnedViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^user/', include('djoser.urls')),
    url(r'^translation/', TranslationView.as_view(), name='translation'),
]
