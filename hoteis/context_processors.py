from hoteis.models import Quarto
from datetime import datetime
from clientes.models import ClientePerfil
from decimal import Decimal

def carrinho(request):
    carrinho_data = request.session.get('carrinho', None)
    if not carrinho_data:
        return {'carrinho': None, 'carrinho_qtd': 0}
    
    try:
        quarto_id = carrinho_data.get('quarto_id')
        quarto = Quarto.objects.get(id=quarto_id)
        
        checkin_str = carrinho_data.get('checkin')
        checkout_str = carrinho_data.get('checkout')
        
        checkin = datetime.strptime(checkin_str, '%Y-%m-%d').date()
        checkout = datetime.strptime(checkout_str, '%Y-%m-%d').date()
        
        noites = (checkout - checkin).days
        if noites <= 0:
            noites = 1
            
        subtotal = quarto.preco * noites
        from sas.financeiro import calcular_taxas_reserva
        fin = calcular_taxas_reserva(quarto.hotel.empresa, 'hospedagem', quarto.preco, noites)
        subtotal = fin['subtotal']
        taxas = fin['taxa_servico']
        total = fin['total_cliente']
        
        # Forçar reativamente que a quantidade de hóspedes e fichas correspondam à capacidade máxima do quarto
        quantidade_hospedes = quarto.capacidade_pessoas
        hospedes = carrinho_data.get('hospedes', [{}])
        veiculo = carrinho_data.get('veiculo', {'placa': '', 'modelo': '', 'cor': ''})
        
        # Garantir que a lista de fichas de hóspedes tenha exatamente o tamanho da capacidade
        while len(hospedes) < quantidade_hospedes:
            hospedes.append({})
        while len(hospedes) > quantidade_hospedes:
            hospedes.pop()
            
        # Sincronizar reativamente na sessão caso haja divergência (sincroniza sessões antigas na hora!)
        if carrinho_data.get('quantidade_hospedes') != quantidade_hospedes or len(carrinho_data.get('hospedes', [])) != quantidade_hospedes:
            carrinho_data['quantidade_hospedes'] = quantidade_hospedes
            carrinho_data['hospedes'] = hospedes
            request.session['carrinho'] = carrinho_data
            request.session.modified = True
            
        # Se o hóspede principal (índice 0) está vazio e o usuário está logado, autofill
        if request.user.is_authenticated and not hospedes[0]:
            try:
                perfil = request.user.perfil
                hospedes[0] = {
                    'nome': request.user.get_full_name() or request.user.username,
                    'cpf': getattr(perfil, 'cpf', '') or '',
                    'email': request.user.email,
                    'telefone': getattr(perfil, 'telefone', '') or '',
                    'cep': getattr(perfil, 'cep', '') or '',
                    'endereco': f"{getattr(perfil, 'endereco', '') or ''}, {getattr(perfil, 'numero', '') or ''} - {getattr(perfil, 'bairro', '') or ''}, {getattr(perfil, 'cidade', '') or ''}/{getattr(perfil, 'estado', '') or ''}".strip(', -/'),
                    'rg': '',
                    'nacionalidade': 'Brasileira',
                    'profissao': ''
                }
                carrinho_data['hospedes'] = hospedes
                request.session['carrinho'] = carrinho_data
                request.session.modified = True
            except Exception:
                pass
                
        # Validação de cada hóspede
        hospedes_validados = []
        todos_hospedes_completos = True
        
        required_fields = ['nome', 'cpf', 'email', 'telefone', 'cep', 'endereco']
        
        for idx, h in enumerate(hospedes):
            # Verifica se o hóspede tem qualquer campo preenchido (está ativo)
            h_tem_dados = any(h.get(f) for f in required_fields + ['rg', 'nacionalidade', 'profissao'])
            
            # Se for o Titular (idx == 0), é sempre obrigatório ter dados e estar 100% completo
            if idx == 0:
                h_completo = all(h.get(f) for f in required_fields)
                if not h_completo:
                    todos_hospedes_completos = False
            else:
                # Para acompanhantes, se tiver qualquer dado preenchido, deve preencher tudo!
                if h_tem_dados:
                    h_completo = all(h.get(f) for f in required_fields)
                    if not h_completo:
                        todos_hospedes_completos = False
                else:
                    # Se estiver 100% vazio, é considerado válido/completo (opcional não preenchido)
                    h_completo = True
                
            h_info = h.copy()
            h_info['completo'] = h_completo
            h_info['index'] = idx
            h_info['ordem'] = idx + 1
            hospedes_validados.append(h_info)
            
        carrinho_info = {
            'quarto': quarto,
            'checkin': checkin,
            'checkout': checkout,
            'checkin_formatted': checkin.strftime('%d/%m/%Y'),
            'checkout_formatted': checkout.strftime('%d/%m/%Y'),
            'checkin_short': checkin.strftime('%d %b'),
            'checkout_short': checkout.strftime('%d %b'),
            'noites': noites,
            'subtotal': subtotal,
            'taxas': taxas,
            'total': total,
            'quantidade_hospedes': quantidade_hospedes,
            'capacidade_maxima': quarto.capacidade_pessoas,
            'hospedes': hospedes_validados,
            'todos_hospedes_completos': todos_hospedes_completos,
            'veiculo': veiculo,
            
            # Retrocompatibilidade
            'fnrh': hospedes_validados[0] if hospedes_validados else {},
            'fnrh_completo': todos_hospedes_completos,
        }
        return {'carrinho': carrinho_info, 'carrinho_qtd': 1}
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("EXCEPTION IN CARRINHO CONTEXT PROCESSOR:", e)
        # Se der erro (ex: quarto deletado), limpa o carrinho para evitar loop
        request.session['carrinho'] = None
        request.session.modified = True
        return {'carrinho': None, 'carrinho_qtd': 0}
