from django.contrib import admin
from django.urls import path

from vinted_backend.views import UserGenderView, SmartlyView, UserAgeView, UserDeviceView
from vinted_backend.views import UserRegistrationView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user-gender/', UserGenderView.as_view()),
    path('user-age/', UserAgeView.as_view()),
    path('user-device/', UserDeviceView.as_view()),
    path('user-registration/', UserRegistrationView.as_view()),
    path('smartly/', SmartlyView.as_view())
]
