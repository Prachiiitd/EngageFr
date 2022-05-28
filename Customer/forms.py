from django.forms import ModelForm
from .models import Application


class ApplicationForm(ModelForm):
    """
    This class is used to create a form for the Application model.
    """
    class Meta:
        """
        This class is used to specify the model and fields to be used in the form.
        """
        model = Application  # The model to use
        fields = '__all__'  # Assign all fields in the model to the form
        exclude = ['customer', 'appId', 'found', 'lastTrackDate', 'lastTrackLoc']  # Fields to be excluded from the form

    def __init__(self, *args, **kwargs):
        """
        This function is used to initialize the form.
        """
        super(ApplicationForm, self).__init__(*args, **kwargs)  # Call the parent's __init__ function

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'  # Set the class of the form fields to form-control

        self.fields['images'].required = True  # Set the images' field to be required
