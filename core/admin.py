from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Partido, Cargo, Politico, Mandato, Nota, AvaliacaoUsuario


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ("sigla", "nome")
    search_fields = ("sigla", "nome")


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ("nome", "poder", "nivel")
    list_filter = ("poder", "nivel")
    search_fields = ("nome",)


@admin.register(Politico)
class PoliticoAdmin(admin.ModelAdmin):
    list_display = ("nome", "partido", "cargo", "uf", "municipio", "ativo")
    list_filter = ("ativo", "uf", "esfera", "cargo__poder", "cargo__nivel")
    search_fields = ("nome", "slug", "municipio")
    autocomplete_fields = ("partido", "cargo")
    prepopulated_fields = {"slug": ("nome",)}


@admin.register(Mandato)
class MandatoAdmin(admin.ModelAdmin):
    list_display = ("politico", "cargo", "inicio", "fim")
    list_filter = ("cargo__poder", "cargo__nivel")
    search_fields = ("politico__nome", "cargo__nome")
    autocomplete_fields = ("politico", "cargo")


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ("politico", "periodo_ref", "nota_final", "nota_ia", "nota_usuario")
    list_filter = ("periodo_ref",)
    search_fields = ("politico__nome",)
    autocomplete_fields = ("politico",)


@admin.register(AvaliacaoUsuario)
class AvaliacaoUsuarioAdmin(admin.ModelAdmin):
    list_display = ("politico", "usuario", "nota", "criado_em")
    list_filter = ("nota", "criado_em")
    search_fields = ("politico__nome", "usuario__username")
    autocomplete_fields = ("politico", "usuario")


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'cpf', 'nome_completo', 'email', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'cpf', 'nome_completo', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('cpf', 'nome_completo', 'telefone', 'data_nascimento')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('cpf', 'nome_completo', 'telefone', 'data_nascimento')
        }),
    )
