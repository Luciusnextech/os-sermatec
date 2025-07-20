from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('os/', views.OrdemServicoListCreate.as_view()),
    path('os/<int:pk>/imagens/', views.ImagemOSCreate.as_view()),
    path('os/<int:pk>/pdf/', views.OrdemServicoPDFView.as_view()),
    path('area-tecnica/', views.ArquivoTecnicoList.as_view()),  # Rota da área técnica
]
