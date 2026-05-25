import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from .models import SolicitacaoEmpresa, Documento


@require_POST
def solicitar_parceria(request):
    """Recebe o formulário de solicitação de empresa e salva no banco."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'erro': 'Dados inválidos.'}, status=400)

    # Validação de campos obrigatórios
    obrigatorios = [
        'cep', 'endereco', 'numero', 'cidade', 'estado',
        'responsavel_nome',
        'responsavel_email', 'responsavel_telefone',
        'descricao_negocio',
    ]
    for campo in obrigatorios:
        if not data.get(campo, '').strip():
            return JsonResponse({'ok': False, 'erro': f'Campo obrigatório: {campo}'}, status=400)

    if not data.get('aceite_termos') or not data.get('aceite_privacidade') or not data.get('autoriza_contato'):
        return JsonResponse({'ok': False, 'erro': 'Aceite de todos os termos é obrigatório.'}, status=400)

    # Cria o registro isolado
    SolicitacaoEmpresa.objects.create(
        razao_social=data['razao_social'].strip(),
        nome_fantasia=data['nome_fantasia'].strip(),
        cnpj=data['cnpj'].strip(),
        tipo_empresa=data['tipo_empresa'],
        site=data.get('site', '').strip(),
        instagram=data.get('instagram', '').strip(),
        cep=data['cep'].strip(),
        endereco=data['endereco'].strip(),
        numero=data.get('numero', '').strip(),
        bairro=data.get('bairro', '').strip(),
        cidade=data['cidade'].strip(),
        estado=data['estado'].strip().upper(),
        responsavel_nome=data['responsavel_nome'].strip(),
        responsavel_cargo=data.get('responsavel_cargo', 'Proprietário/Gestor').strip(),
        responsavel_email=data['responsavel_email'].strip(),
        responsavel_telefone=data['responsavel_telefone'].strip(),
        descricao_negocio=data['descricao_negocio'].strip(),
        capacidade=data.get('capacidade', '').strip(),
        como_soube=data.get('como_soube', '').strip(),
        aceite_termos=bool(data.get('aceite_termos')),
        aceite_privacidade=bool(data.get('aceite_privacidade')),
        autoriza_contato=bool(data.get('autoriza_contato')),
        status='pendente',
    )

    return JsonResponse({'ok': True, 'mensagem': 'Solicitação recebida com sucesso! Em breve nossa equipe entrará em contato.'})


def ver_documento(request, slug):
    """Renderiza a página do documento legal (termos / política)."""
    doc = get_object_or_404(Documento, slug=slug)
    return render(request, 'parceiros/documento.html', {'doc': doc})
