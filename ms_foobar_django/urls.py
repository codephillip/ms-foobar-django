from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from ms_foobar_app.views import LoginCodeVerifierView, LoginInputView, ResendCodeInputView

urlpatterns = [
    path('', include('ms_foobar_app.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/token/login/', LoginInputView.as_view(), name='login'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/token/verify_login/', LoginCodeVerifierView.as_view(), name='login_code_verifier'),
    path('auth/token/resend_code/', ResendCodeInputView.as_view(), name='resend_code'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()