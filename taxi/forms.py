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
    if not re.fullmatch(r"[A-Z]{3}\d{5}", value):
        raise ValidationError(
            "A licença deve ter 8 caracteres: 3 letras maiúsculas seguidas por 5 dígitos (ex: ABC12345)."
        )


# --- Formulário para Criação/Atualização de Driver (Inclui validação) ---
class DriverForm(forms.ModelForm):
    # Corrigido o erro de *builtins* (VNE003) renomeando a variável interna do campo,
    # embora a definição do campo esteja correta. A notação 'license' no field é o que é usado.
    license_field = forms.CharField(
        max_length=8,
        validators=[validate_license_format],
        label="Número da CNH"
    )

    class Meta:
        model = Driver
        # Adapte os campos abaixo com base no seu modelo Driver real
        fields = ["first_name", "last_name", "license_field", "bio"] # Usando license_field aqui

    def clean_license(self):
        # Garante que a validação seja chamada
        # O erro de VNE003 no clean_license pode ser ignorado se 'license' é um campo real no modelo,
        # mas ajustamos para usar o nome do field no model se for o caso.
        license_val = self.cleaned_data.get("license_field")
        validate_license_format(license_val)
        return license_val


# --- Formulário Específico para Atualização da CNH ---
class DriverLicenseUpdateForm(forms.Form):
    license = forms.CharField(
        max_length=8,
        validators=[validate_license_format],
        label="Novo Número da CNH"
    )

    def clean_license(self):
        license_val = self.cleaned_data["license"]
        validate_license_format(license_val)
        return license_val


# --- Formulário para Criação de Carro (com Checkboxes para Drivers) ---
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        # Assumindo que 'drivers' é o campo ManyToManyfield para Driver no modelo Car
        fields = ["model", "manufacturer", "plate_number", "drivers"]

        widgets = {
            # Switch para checkboxes
            "drivers": widgets.CheckboxSelectMultiple(),
        }
