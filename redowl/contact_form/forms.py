from django import forms
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=24, 
        min_length=2,    
        required=False,
        label="Давайте познакомимся",
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя','maxlength': '24', 'minlength': '2'}),
        error_messages={
            'required': 'Пожалуйста, введите ваше имя.',
            'max_length': 'Имя слишком длинное.',
            'min_length': 'Имя слишком короткое.'
        }
    )

    phone = forms.CharField(
        max_length=15,
        min_length=10,
        required=True,
        label="Ваш номер телефона",
        widget=forms.TextInput(attrs={ 'type': 'tel','placeholder': '+7 (900) 800-70-60', 'maxlength': '15', 'minlength': '10'}),
        error_messages={
            'required': 'Пожалуйста, введите ваш номер телефона.',
            'max_length': 'Номер телефона слишком длинный.',
            'min_length': 'Номер телефона слишком короткий. Возможно, вы набирали его неправильно.'
        }
    )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise ValidationError('Номер телефона должен содержать только цифры.')
        return phone

    class Meta:
        fields = ['name', 'phone']