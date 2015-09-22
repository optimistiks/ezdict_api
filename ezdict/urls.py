from django.conf.urls import url, include
from ezdict.translation.views import TranslationView, LanguageView, SuggestedMeaningView
from ezdict.translation_history.views import TranslationHistoryViewSet
from ezdict.card.views import CardViewSet, CardMeaningViewSet, CardToStudyViewSet
from ezdict.user_profile.views import UserProfileView
from ezdict.quiz.views import QuizViewSet
from rest_framework_bulk.routes import BulkRouter


router = BulkRouter()
router.register(r'translation_history', TranslationHistoryViewSet)
router.register(r'cards', CardViewSet)
router.register(r'card_meanings', CardMeaningViewSet)
router.register(r'cards_to_study', CardToStudyViewSet)
router.register(r'quizzes', QuizViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^user/', include('djoser.urls')),
    url(r'^profile/$', UserProfileView.as_view(), name='user_profile'),
    url(r'^translation/$', TranslationView.as_view(), name='translation'),
    url(r'^suggested_meanings/$', SuggestedMeaningView.as_view(), name='suggested_meanings'),
    url(r'^languages/$', LanguageView.as_view(), name='languages'),
]
