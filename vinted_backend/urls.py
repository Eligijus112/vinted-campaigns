from django.contrib import admin
from django.urls import path

from vinted_backend.views import UserGenderView, SmartlyAggView, UserAgeView, UserDeviceView
from vinted_backend.views import UserRegistrationView, SmartlyGranularView, AdWordsAggView, AdWordsGranularView
from vinted_backend.views import InstallationTotal, InstallationCampaign, UserBehaviour

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user-gender/', UserGenderView.as_view()),
    path('user-age/', UserAgeView.as_view()),
    path('user-device/', UserDeviceView.as_view()),
    path('user-registration/', UserRegistrationView.as_view()),
    
    path('smartly-aggregations/', SmartlyAggView.as_view()),
    path('smartly-granular/', SmartlyGranularView.as_view()),

    path('adwords-aggregations/', AdWordsAggView.as_view()),
    path('adwords-granular/', AdWordsGranularView.as_view()),

    path('installations-total/', InstallationTotal.as_view()),
    path('installations-campaign/', InstallationCampaign.as_view()),

    path('user-behaviour/', UserBehaviour.as_view()),
]
