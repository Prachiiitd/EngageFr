from django.forms import ModelForm
from .models import Application


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = '__all__'
        exclude = ['customer', 'appId', 'found', 'lastTrackDate', 'lastTrackLoc']

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['images'].required = True


