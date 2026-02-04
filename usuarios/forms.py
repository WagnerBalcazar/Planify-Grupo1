from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Importamos el validador oficial de seguridad
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


class RegistroUsuarioForm(forms.ModelForm):
    # ... (Tus campos de nombre, apellido, correo igual que antes) ...
    correo = forms.EmailField(
        required=True, label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com', 'class': 'input-pequeno'})
    )
    nombre = forms.CharField(required=True, label="Nombre", widget=forms.TextInput(attrs={'class': 'input-pequeno'}))
    apellido = forms.CharField(required=True, label="Apellido",
                               widget=forms.TextInput(attrs={'class': 'input-pequeno'}))

    password_1 = forms.CharField(
        label="Contraseña", required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Mínimo 8 caracteres', 'class': 'input-pequeno'}),
        help_text=None  # El texto lo pondremos visualmente si quieres, o dejamos que valide al enviar
    )
    password_2 = forms.CharField(
        label="Confirmar", required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Repite la contraseña', 'class': 'input-pequeno'})
    )

    class Meta:
        model = User
        fields = ('correo', 'nombre', 'apellido')

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if User.objects.filter(username=correo).exists():
            raise ValidationError("Este correo ya está registrado.")
        return correo

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password_1")
        p2 = cleaned_data.get("password_2")

        # 1. Verificar que coincidan
        if p1 and p2 and p1 != p2:
            self.add_error('password_2', "Las contraseñas no coinciden.")

        # 2. VALIDACIÓN FUERTE DE DJANGO (Aquí está la magia)
        if p1:
            try:
                # Esto revisa si es muy corta, muy común, o numérica
                validate_password(p1)
            except ValidationError as e:
                # Si falla, agregamos el error al campo
                self.add_error('password_1', e)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nombre']
        user.last_name = self.cleaned_data['apellido']
        user.email = self.cleaned_data['correo']
        user.username = self.cleaned_data['correo']  # Usuario = Correo
        user.set_password(self.cleaned_data['password_1'])
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(forms.Form):
    correo = forms.EmailField(
        label="Usuario", # Visualmente dirá "Usuario" como en tu foto
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu correo ', 'class': 'input-pequeno'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'class': 'input-pequeno'})
    )

    def clean(self):
        correo = self.cleaned_data.get('correo')
        password = self.cleaned_data.get('password')

        if correo and password:
            # Buscamos si existe un usuario con ese username (que es el correo)
            user = authenticate(username=correo, password=password)
            if not user:
                raise forms.ValidationError("Usuario o contraseña incorrectos.")
            self.user_cache = user
        return self.cleaned_data

    def get_user(self):
        return self.user_cache