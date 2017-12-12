from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class WatermarkForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'watermark-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.layout = Layout(
            'image',
            'watermark_image',
            Submit('submit', 'Submit')
        )

    image               = forms.ImageField(label='Original Image', required=True)
    watermark_image     = forms.ImageField(label='Watermark Image', required=True)