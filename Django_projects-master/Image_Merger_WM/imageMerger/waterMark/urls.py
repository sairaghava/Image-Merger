from django.conf import settings
from django.conf.urls.static import static
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView
from django.conf.urls import url
from django.contrib import admin
from .views import (watermark,watermark_added,cached_image)

app_name = 'waterMark'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('/waterMark_templates/watermark')), name='home'),
    url(r'^watermark/$', watermark, name='watermark'),
    url(r'^watermark-result/(?P<result_id>[0-9a-f]{32})/$', watermark_added, name='watermark-result'),
    url(r'^cached-image/(?P<key>.+)/$', cached_image, name='cached-image')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
