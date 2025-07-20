from rest_framework import serializers
from django.contrib.auth.models import User
from .models import OrdemServico, ImagemOS, ArquivoTecnico

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ImagemOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagemOS
        fields = ['id', 'imagem']

class OrdemServicoSerializer(serializers.ModelSerializer):
    cliente = UserSerializer(read_only=True)
    imagens = ImagemOSSerializer(many=True, read_only=True)
    class Meta:
        model = OrdemServico
        fields = [
            'id', 'cliente', 'tecnico', 'descricao',
            'data_abertura', 'data_fechamento', 'status',
            'imagens', 'assinatura_cliente', 'assinatura_tecnico'
        ]

class ArquivoTecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArquivoTecnico
        fields = ['id', 'titulo', 'arquivo', 'criado_em']
