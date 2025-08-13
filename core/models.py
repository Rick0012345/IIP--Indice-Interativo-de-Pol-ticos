from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import re


def validate_cpf(value):
    """Valida se o CPF está no formato correto (apenas números)"""
    cpf = re.sub(r'\D', '', value)  # Remove caracteres não numéricos
    if len(cpf) != 11:
        raise ValidationError('CPF deve ter 11 dígitos')
    
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido')
    
    return cpf


class CustomUser(AbstractUser):
    """Modelo de usuário personalizado com CPF único"""
    cpf = models.CharField(
        max_length=11, 
        unique=True, 
        validators=[validate_cpf],
        help_text='CPF do usuário (apenas números)'
    )
    nome_completo = models.CharField(max_length=255, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Remove caracteres não numéricos do CPF antes de salvar
        if self.cpf:
            self.cpf = re.sub(r'\D', '', self.cpf)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.username} - {self.cpf}"
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class Partido(models.Model):
    sigla = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Partido"
        verbose_name_plural = "Partidos"

    def __str__(self):
        return self.sigla


class Cargo(models.Model):
    PODER_CHOICES = [
        ("EXECUTIVO", "Executivo"),
        ("LEGISLATIVO", "Legislativo"),
        ("JUDICIARIO", "Judiciário"),
    ]
    NIVEL_CHOICES = [
        ("MUNICIPAL", "Municipal"),
        ("ESTADUAL", "Estadual"),
        ("FEDERAL", "Federal"),
    ]

    nome = models.CharField(max_length=100)
    poder = models.CharField(max_length=20, choices=PODER_CHOICES)
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        unique_together = ("nome", "poder", "nivel")

    def __str__(self):
        return f"{self.nome} ({self.get_poder_display()} • {self.get_nivel_display()})"


class Politico(models.Model):
    ESFERA_CHOICES = [
        ("MUNICIPAL", "Municipal"),
        ("ESTADUAL", "Estadual"),
        ("FEDERAL", "Federal"),
    ]

    nome = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True)
    foto_url = models.URLField(blank=True, null=True, help_text="URL da foto (opcional)")
    foto = models.ImageField(upload_to='politicos/', blank=True, null=True, help_text="Upload da foto (opcional)")

    partido = models.ForeignKey(Partido, on_delete=models.SET_NULL, null=True, blank=True, related_name="politicos")
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True, related_name="politicos_atual")  # cargo atual (opcional)

    esfera = models.CharField(max_length=20, choices=ESFERA_CHOICES, blank=True)
    uf = models.CharField(max_length=2, blank=True)
    municipio = models.CharField(max_length=120, blank=True)

    ativo = models.BooleanField(default=True)
    data_nascimento = models.DateField(null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Político"
        verbose_name_plural = "Políticos"
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["nome"]),
        ]

    def __str__(self):
        return self.nome


class Mandato(models.Model):
    politico = models.ForeignKey(Politico, on_delete=models.CASCADE, related_name="mandatos")
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, related_name="mandatos")
    inicio = models.DateField()
    fim = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Mandato"
        verbose_name_plural = "Mandatos"
        ordering = ["-inicio"]

    def __str__(self):
        return f"{self.politico} - {self.cargo} ({self.inicio} a {self.fim or 'atual'})"


class Nota(models.Model):
    politico = models.ForeignKey(Politico, on_delete=models.CASCADE, related_name="notas")
    periodo_ref = models.DateField(help_text="Data de referência (ex.: primeiro dia do mês)")

    nota_dados_oficiais = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sentimento_noticias = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    nota_usuario = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    nota_ia = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    nota_final = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"
        unique_together = ("politico", "periodo_ref")
        ordering = ["-periodo_ref"]

    def __str__(self):
        return f"Nota {self.politico} {self.periodo_ref}: {self.nota_final}"


class AvaliacaoUsuario(models.Model):
    politico = models.ForeignKey(Politico, on_delete=models.CASCADE, related_name="avaliacoes")
    usuario = models.ForeignKey(getattr(settings, "AUTH_USER_MODEL", "auth.User"), on_delete=models.SET_NULL, null=True, blank=True)
    nota = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    comentario = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Avaliação de Usuário"
        verbose_name_plural = "Avaliações de Usuários"
        ordering = ["-criado_em"]

    def __str__(self):
        user = "anônimo" if not self.usuario else str(self.usuario)
        return f"{self.politico} - {self.nota} por {user}"
