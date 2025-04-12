from django import forms
import os

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        if self.allow_multiple_selected:
            return files.getlist(name)
        return super().value_from_datadict(data, files, name)

class MultiFileField(forms.FileField):
    widget = MultiFileInput

    def to_python(self, data):
        if not data:
            return []
        if isinstance(data, list):
            return data
        return [data]

    def validate(self, data):
        if self.required and not data:
            raise forms.ValidationError(self.error_messages['required'], code='required')
        if data:
            super().validate(data[0])

    def clean(self, data, initial=None):
        files = super().clean(data, initial)
        allowed_extensions = ['.txt', '.pdf', '.doc', '.docx']
        for f in files:
            ext = os.path.splitext(f.name)[1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError(
                    f"Unsupported file extension: {ext}. Allowed extensions are: {', '.join(allowed_extensions)}"
                )
        return files

class ResumeUploadForm(forms.Form):
    full_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )

    JOB_CATEGORIES = [
        ('Accountant', 'Accountant'),
        ('Advocate', 'Advocate'),
        ('Agriculture', 'Agriculture'),
        ('Apparel', 'Apparel'),
        ('Arts', 'Arts'),
        ('Automation', 'Automation'),
        ('Aviation', 'Aviation'),
        ('Banking', 'Banking'),
        ('BPO', 'BPO'),
        ('Business Development', 'Business Development'),
        ('Chef', 'Chef'),
        ('Construction', 'Construction'),
        ('Consultant', 'Consultant'),
        ('Designer', 'Designer'),
        ('Digital Media', 'Digital Media'),
        ('Engineering', 'Engineering'),
        ('Finance', 'Finance'),
        ('Fitness', 'Fitness'),
        ('Healthcare', 'Healthcare'),
        ('HR', 'HR'),
        ('Information Technology', 'Information Technology'),
        ('Public Relations', 'Public Relations'),
        ('Sales', 'Sales'),
        ('Teacher', 'Teacher'),
    ]

    job_category = forms.ChoiceField(
        choices=JOB_CATEGORIES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    files = MultiFileField(
        widget=MultiFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        required=True
    )
