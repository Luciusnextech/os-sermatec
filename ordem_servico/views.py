from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from .models import OrdemServico, ImagemOS, ArquivoTecnico
from .serializers import OrdemServicoSerializer, ImagemOSSerializer, UserSerializer, ArquivoTecnicoSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from django.http import FileResponse
import os
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class UserRegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Usuário já existe.'}, status=400)
        user = User.objects.create_user(username=username, password=password, email=email)
        return Response(UserSerializer(user).data)

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data})
        return Response({'error': 'Login inválido.'}, status=400)

class OrdemServicoListCreate(generics.ListCreateAPIView):
    queryset = OrdemServico.objects.all()
    serializer_class = OrdemServicoSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)

class ImagemOSCreate(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        ordem_servico = OrdemServico.objects.get(pk=pk)
        for img in request.FILES.getlist('imagens'):
            ImagemOS.objects.create(ordem_servico=ordem_servico, imagem=img)
        return Response({'ok': True})

class OrdemServicoPDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        os_obj = OrdemServico.objects.get(pk=pk)
        response = FileResponse(self.generate_pdf(os_obj), as_attachment=True, filename=f'os_{pk}.pdf')
        return response

    def generate_pdf(self, os_obj):
        from io import BytesIO
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Adiciona logo se existir
        logo_path = os.path.join(settings.BASE_DIR, 'logo.png')
        if os.path.exists(logo_path):
            p.drawImage(logo_path, 50, height - 120, width=150, height=80, mask='auto')

        p.setFont("Helvetica-Bold", 18)
        p.drawString(220, height - 70, "Ordem de Serviço")

        p.setFont("Helvetica", 12)
        y = height - 140
        p.drawString(50, y, f"Cliente: {os_obj.cliente.username}")
        y -= 20
        p.drawString(50, y, f"Descrição: {os_obj.descricao}")
        y -= 20
        p.drawString(50, y, f"Status: {os_obj.status}")
        y -= 20
        p.drawString(50, y, f"Data Abertura: {os_obj.data_abertura.strftime('%d/%m/%Y %H:%M')}")
        if os_obj.data_fechamento:
            y -= 20
            p.drawString(50, y, f"Data Fechamento: {os_obj.data_fechamento.strftime('%d/%m/%Y %H:%M')}")

        # Adiciona assinaturas
        if os_obj.assinatura_cliente:
            p.drawString(50, y - 40, "Assinatura Cliente:")
            p.drawImage(os_obj.assinatura_cliente.path, 180, y - 70, width=150, height=50, mask='auto')
        if os_obj.assinatura_tecnico:
            p.drawString(350, y - 40, "Assinatura Técnico:")
            p.drawImage(os_obj.assinatura_tecnico.path, 480, y - 70, width=150, height=50, mask='auto')

        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer

class ArquivoTecnicoList(generics.ListAPIView):
    queryset = ArquivoTecnico.objects.all()
    serializer_class = ArquivoTecnicoSerializer
    permission_classes = [permissions.IsAuthenticated]  # Troque para AllowAny se quiser público
