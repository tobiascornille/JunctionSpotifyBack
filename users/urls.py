from django.conf.urls import url
from . import views
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    url(r'^update', views.update_user),
    url(r'^callback', views.authentication_spotify),
    url(r'^([\w.@+-]+)', views.user_data, name='user_data'),
    url(r'^$', views.create_user),
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
