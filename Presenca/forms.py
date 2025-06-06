from django import forms
from django.core.validators import RegexValidator
from .models import Pessoas, RegistroPresenca
import os
from django.utils import timezone


class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoas
        fields = '__all__'
        widgets = {
            'telefone': forms.TextInput(attrs={
                'data-mask': '(00) 00000-0000',
                'placeholder': '(XX) XXXXX-XXXX'
            })
        }

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        numeros = ''.join(filter(str.isdigit, telefone))
        if len(numeros) not in [10, 11]:
            raise forms.ValidationError("Telefone deve ter 10 (fixo) ou 11 (celular) dígitos")
        return telefone

    def save(self, commit=True):
        instance = super().save(commit=False)

        if not instance.id and 'imagem' in self.files:  # Novo registro com imagem
            instance.save()  # Salva primeiro para gerar ID
            imagem = self.files['imagem']
            nome_limpo = ''.join(e for e in instance.nome if e.isalnum()).lower()
            extensao = os.path.splitext(imagem.name)[1].lower()
            novo_nome = f"fotos_cadastro/{nome_limpo}_{instance.id}{extensao}"
            instance.imagem.save(novo_nome, imagem, save=False)

        if commit:
            instance.save()
        return instance


class RegistroPresencaForm(forms.ModelForm):
    class Meta:
        model = RegistroPresenca
        fields = '__all__'
        widgets = {
            'dia': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        dia = cleaned_data.get('dia')

        if dia and dia > timezone.now().date():
            raise forms.ValidationError("Data futura não permitida")

        return cleaned_data