import os
import sys
import django

# Adiciona o diretório raiz do projeto ao PATH do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'navievibe.settings')
django.setup()

from django.test import RequestFactory
from hoteis.views import vanity_url

print("Simulando requisição GET para '/pousadaramilostiangua'...")

try:
    rf = RequestFactory()
    # Adiciona cabeçalhos padrão
    request = rf.get('/pousadaramilostiangua')
    response = vanity_url(request, slug='pousadaramilostiangua')
    
    print("\n--- RESULTADOS DO DIAGNÓSTICO ---")
    print(f"Status Code da resposta: {response.status_code}")
    
    if response.status_code == 200:
        print("SUCESSO: A Vanity URL e o template detalhe.html foram compilados e renderizados com 100% de integridade!")
    else:
        print(f"ERRO: Resposta retornou código {response.status_code}")
except Exception as e:
    print("\n--- ERRO NA COMPILAÇÃO DO TEMPLATE ---")
    import traceback
    traceback.print_exc()
