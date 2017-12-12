import uuid
from io import BytesIO
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, FormView, View
from PIL import Image
from .forms import WatermarkForm
from .models import add_watermark


class Watermark(FormView):
    template_name = 'waterMark_templates/watermark.html'
    form_class = WatermarkForm
    def form_valid(self, form):
        image           = Image.open(form.cleaned_data['image'])
        wm_image        = Image.open(form.cleaned_data['watermark_image'])
        result_image    = add_watermark(image, wm_image)
        result_id       = _createid()
        _save_source_image(image, result_id)
        _save_result_image(result_image, result_id)
        return HttpResponseRedirect(reverse_lazy('watermark-result', kwargs={'result_id': result_id}))

class WatermarkAdded(TemplateView):
    template_name = 'waterMark_templates/watermark_added.html'
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        result_id = kwargs.get('result_id', 'unknown')
        context_data['source_image_src'] = reverse_lazy('cached-image',
                                                        kwargs={'key': '{%s}-image-{%s}' %('Source',result_id)})
        context_data['result_image_src'] = reverse_lazy('cached-image',
                                                        kwargs={'key': '{%s}-image-{%s}' %('Result',result_id)})
        return context_data


class CachedImage(View):
    def get(self, request, key=None, **kwargs):
        image_fp = _get_image_fp(key)
        image_fp.seek(0)
        return HttpResponse(image_fp)

def _createid():
    return uuid.uuid4().hex

def _save_image(key, image, format_='png'):
    bytes_io = BytesIO()
    image.save(bytes_io, format=format_)
    cache.set(key, bytes_io.getvalue())

def _save_source_image(image, result_id, format_=None):
    _save_image('{%s}-image-{%s}' %('Source',result_id), image, format_=format_ if format_ is not None else image.format)

def _save_result_image(image, result_id, format_='png'):
    _save_image('{%s}-image-{%s}' %('Result',result_id), image, format_=format_)

def _get_image_fp(key):
    return BytesIO(cache.get(key))





watermark           = Watermark.as_view()
watermark_added    = WatermarkAdded.as_view()
cached_image        = CachedImage.as_view()

