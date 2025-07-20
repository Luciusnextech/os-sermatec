from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('andamento', 'Em andamento'),
        ('concluida', 'Concluída'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='os_cliente')
    tecnico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='os_tecnico')
    descricao = models.TextField()
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_fechamento = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta')
    assinatura_cliente = models.ImageField(upload_to='assinaturas/', null=True, blank=True)
    assinatura_tecnico = models.ImageField(upload_to='assinaturas/', null=True, blank=True)

    def __str__(self):
        return f"OS #{self.id} - {self.cliente.username} - {self.status}"

class ImagemOS(models.Model):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='imagens_os/')

    def __str__(self):
        return f"Imagem OS {self.ordem_servico.id}"

class ArquivoTecnico(models.Model):
    titulo = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to='area_tecnica/')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
