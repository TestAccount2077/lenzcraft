from django.conf.urls import url

from .views import *

app_name = 'accounts'


validate_signup = LoginViewSet.as_view({
    'post': 'validate_signup'
})

validate_login = LoginViewSet.as_view({
    'post': 'validate_login'
})

validate_google_login = LoginViewSet.as_view({
    'post': 'validate_google_login'
})

logout = LoginViewSet.as_view({
    'post': 'logout'
})

urlpatterns = [

    url(r'^ajax/validate-signup/$', validate_signup),
    url(r'^ajax/validate-login/$', validate_login),
    url(r'^ajax/validate-google-login/$', validate_google_login),
    url(r'^ajax/logout/$', logout),
]
