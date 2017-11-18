from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static
from bobross import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^episode/(?P<pk>[0-9]+)/$', views.EpisodeDetail.as_view(), name='episode-detail'),
    url(r'^episodes/$', views.EpisodeList.as_view(), name='episode-list'),
    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^user-art$', views.UserArtList.as_view(), name='user-art-list'),
    url(r'^user-art/(?P<pk>[0-9]+)/$', views.UserArtDetail.as_view(), name='user-art-detail'),
    url(r'^gallery/$', views.UserArtGallery.as_view(), name='gallery'),
    url(r'^about/$', views.About.as_view(), name='about'),
    url(r'^$', views.api_root),
]


urlpatterns = format_suffix_patterns(urlpatterns)