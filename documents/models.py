from django.db import models
from accounts.models import User
from products.models import Product

class Info_Adicionais(models.Model):
    distancia = models.PositiveBigIntegerField()
    horas = models.PositiveBigIntegerField()
    valor_km = models.DecimalField(max_digits=10, decimal_places=2)
    valor_hora = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.total)

class Cabecalho(models.Model):
    nome = models.CharField(max_length=80)
    cnpj = models.CharField(max_length=20)
    cpf = models.CharField(max_length=15)
    endereco = models.CharField(max_length=40)
    cep = models.CharField(max_length=10)
    cidade = models.CharField(max_length=40)
    telefone = models.CharField(max_length=14)
    info_adicionais = models.ForeignKey(Info_Adicionais, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    comissao = models.DecimalField(max_digits=10, decimal_places=2)
    usuario_criador = models.ForeignKey(User, on_delete=models.CASCADE)
    aprovado = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
    
class Documento(models.Model):
    maquina = models.CharField(max_length=50)
    numero_maquina = models.CharField(max_length=40)
    quantidade_linhas = models.PositiveBigIntegerField()
    maquina_nova = models.BooleanField(default=False)
    faturado_revenda = models.CharField(max_length=100)
    produto = models.ForeignKey(Product, on_delete=models.CASCADE)
    valor_produto = models.DecimalField(max_digits=10, decimal_places=2)
    servicos_executados = models.CharField(max_length=100)
    testes_realizados = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    cabecalho = models.ForeignKey(Cabecalho, on_delete=models.CASCADE)


class Documento_Instalacao(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dono_documento_set')
    nota_fiscal = models.CharField(max_length=20)
    parceiros = models.ManyToManyField(User, related_name='parceiros_documento_set')


class Documento_Pos_Venda(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
