# taxi/forms.py
import re
from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from .models import Driver, Car, User # Assumindo que seus modelos estão aqui

# --- Validação Customizada da CNH ---
def validate_license_format(value):
    """
    Valida se a licença:
    1. Tem exatamente 8 caracteres.
    2. Os 3 primeiros são letras maiúsculas.
    3. Os 5 últimos são dígitos.
    """
    if not re.fullmatch(r'[A-Z]{3}\d{5}', value):
        raise ValidationError(
            'A licença deve ter 8 caracteres: 3 letras maiúsculas seguidas por 5 dígitos (ex: ABC12345).'
        )

# --- Formulário para Criação/Atualização de Driver (Inclui validação) ---
class DriverForm(forms.ModelForm):
    license = forms.CharField(
        max_length=8,
        validators=[validate_license_format],
        label="Número da CNH"
    )

    class Meta:
        model = Driver
        # Adapte os campos abaixo com base no seu modelo Driver real
        fields = ['first_name', 'last_name', 'license', 'bio']

    def clean_license(self):
        # Garante que a validação seja chamada
        license = self.cleaned_data.get('license')
        validate_license_format(license)
        return license

# --- Formulário Específico para Atualização da CNH ---
class DriverLicenseUpdateForm(forms.Form):
    license = forms.CharField(
        max_length=8,
        validators=[validate_license_format],
        label="Novo Número da CNH"
    )

    def clean_license(self):
        license = self.cleaned_data['license']
        validate_license_format(license)
        return license

# --- Formulário para Criação de Carro (com Checkboxes para Drivers) ---
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        # Assumindo que 'drivers' é o campo ManyToManyfield para Driver no modelo Car
        fields = ['model', 'manufacturer', 'plate_number', 'drivers']

        widgets = {
            # Switch para checkboxes
            'drivers': widgets.CheckboxSelectMultiple(),
        }
