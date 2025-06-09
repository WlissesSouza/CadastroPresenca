from django.utils import timezone
from django.db import models
from django.conf import settings
from .constants import BatizadoOptions

class Pessoas(models.Model):
    imagem = models.ImageField(
        upload_to='fotos_cadastro/',
        blank=True,
        null=True,
        verbose_name='Foto de perfil'
    )
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome completo',
        help_text='Digite o nome completo'
    )
    telefone = models.CharField(
        max_length=15,
        unique=True,
        verbose_name='Telefone',
        help_text='Formato: (XX) XXXXX-XXXX'
    )
    endereco = models.TextField(
        max_length=200,
        blank=True,
        default='',
        verbose_name='Endereço Completo'
    )
    batizado = models.IntegerField(
        choices=BatizadoOptions.CHOICES,
        default=BatizadoOptions.OUTROS
    )
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de cadastro'
    )
    obs = models.TextField(
        max_length=200,
        blank=True,
        verbose_name='Observações'
    )

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class RegistroPresenca(models.Model):
    pessoa = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='registros_presenca',
        verbose_name='Pessoa'
    )

    dia = models.DateField(  # Data sem hora
        default=timezone.now,
        db_index=True,
        verbose_name='Data da presença'
    )

    # SE QUISER ADICIONAR A HORA

    # hora = models.TimeField(
    #     default=timezone.now,
    #     verbose_name='Hora do registro'
    # )

    obs = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='Observações'
    )

    class Meta:
        verbose_name = 'Registro de presença'
        verbose_name_plural = 'Registros de presença'
        unique_together = ['pessoa', 'dia']  # Não permite salvar a mesma pessoa no mesmo dia
        ordering = ['-dia', 'pessoa']  # Ordena por data decrescente

    def __str__(self):
        return f"{self.pessoa.nome} - {self.dia.strftime('%d/%m/%Y')}"
