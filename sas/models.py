from django.db import models
from core.models import Empresa

class RegraTaxa(models.Model):
    TIPO_TAXA_CHOICES = [
        ('percentual', 'Percentual (%)'),
        ('fixa', 'Fixa (R$)'),
    ]
    
    # Se for nula, a regra é global para a categoria de negócio
    empresa = models.ForeignKey(
        Empresa, 
        on_delete=models.CASCADE, 
        null=True, blank=True, 
        related_name='regras_taxa',
        verbose_name='Parceiro / Empresa'
    )
    categoria = models.CharField(
        'Categoria Principal', 
        max_length=20, 
        choices=Empresa.CATEGORIA_CHOICES,
        default='hospedagem'
    )
    
    # Faixas de preço aplicáveis sobre o valor unitário da diária/ingresso
    valor_minimo = models.DecimalField('Valor Mínimo (R$)', max_digits=10, decimal_places=2, default=0.00)
    valor_maximo = models.DecimalField('Valor Máximo (R$)', max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Definição do valor cobrado
    tipo_taxa = models.CharField('Tipo de Taxa', max_length=15, choices=TIPO_TAXA_CHOICES, default='percentual')
    valor = models.DecimalField('Valor da Taxa', max_digits=10, decimal_places=2, default=10.00)
    
    cobranca_por_diaria = models.BooleanField(
        'Cobrança por Diária', 
        default=False,
        help_text='Apenas para Hospedagem: se ativado, multiplica o valor fixo pela quantidade de noites.'
    )
    ordem_prioridade = models.IntegerField(
        'Ordem de Prioridade', 
        default=0,
        help_text='Prioridades mais altas rodam primeiro (ex: parceiro = 10, tiers = 5, geral = 0).'
    )
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Regra de Taxa'
        verbose_name_plural = 'Regras de Taxas'
        ordering = ['-ordem_prioridade', 'valor_minimo']

    def __str__(self):
        target = self.empresa.nome_fantasia if self.empresa else f"Global {self.get_categoria_display()}"
        faixa = f" (R$ {self.valor_minimo} a R$ {self.valor_maximo or '∞'})"
        sufixo = " por diária" if self.cobranca_por_diaria and self.tipo_taxa == 'fixa' else ""
        return f"{target}{faixa}: {self.valor}{'%' if self.tipo_taxa == 'percentual' else ' R$'}{sufixo}"
