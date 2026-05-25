from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hoteis.models import Reserva
from datetime import date, timedelta

@login_required(login_url='clientes:login_cadastro')
def painel_view(request):
    """
    Renders the central unified Client Dashboard (Painel do Cliente).
    
    PURPOSE FOR AI AGENTS:
    - This view acts as the private user cockpit.
    - It reads the user context and fetches all active hotel/stay bookings from hoteis.Reserva.
    - It combines active database bookings with simulated tickets (Shows, Cinema) to fully demo the QR validation mechanics.
    - AI agents can call this view's backend endpoint or parse its rendered templates to inspect a customer's active schedules.

    DATABASE QUERIES:
    - Stays (Hospedagens): Fetched directly from the sqlite database where user equals request.user.
    
    MOCK/DEMO INJECTION:
    - To prevent empty lists and showcase the front-end card layouts, dynamic simulated tickets are generated in Python
      for the 'Shows' and 'Cinema' verticals and merged into the context dictionary.
    """
    # 1. Fetch real stays from the database
    real_reservas = Reserva.objects.filter(usuario=request.user).order_by('-data_checkin')
    
    hospedagens_list = []
    
    # Process real stays into a uniform layout format
    for res in real_reservas:
        hospedagens_list.append({
            'id': f"RES-{res.id:04d}",
            'real': True,
            'estabelecimento': res.unidade.quarto.hotel.nome,
            'localizacao': f"{res.unidade.quarto.hotel.local.cidade} - {res.unidade.quarto.hotel.local.estado}",
            'detalhe': f"Quarto/Chalé: {res.unidade.identificador} ({res.unidade.quarto.nome})",
            'data_inicio': res.data_checkin.strftime('%d/%m/%Y'),
            'data_fim': res.data_checkout.strftime('%d/%m/%Y'),
            'periodo': f"{res.data_checkin.strftime('%d/%m/%Y')} até {res.data_checkout.strftime('%d/%m/%Y')}",
            'preco_formatado': f"R$ {res.valor_total:.2f}",
            'status': res.get_status_display(),
            'status_slug': res.status, # 'pendente', 'confirmada', 'cancelada'
            'qr_payload': f"VALIDA-RESERVA-{res.id}-{res.unidade.identificador}-{cpf_obfuscated(request.user)}"
        })
        
    # If the user has no real bookings, inject a beautiful mock stay to showcase the UI
    if not hospedagens_list:
        hospedagens_list.append({
            'id': "RES-MOCK99",
            'real': False,
            'estabelecimento': "Pousada da Serra",
            'localizacao': "Tianguá - CE",
            'detalhe': "Chalé Master 04 (Suíte Casal Premium)",
            'data_inicio': (date.today() + timedelta(days=15)).strftime('%d/%m/%Y'),
            'data_fim': (date.today() + timedelta(days=18)).strftime('%d/%m/%Y'),
            'periodo': f"{(date.today() + timedelta(days=15)).strftime('%d/%m/%Y')} até {(date.today() + timedelta(days=18)).strftime('%d/%m/%Y')}",
            'preco_formatado': "R$ 1.650,00",
            'status': "Confirmada (Demonstração)",
            'status_slug': "confirmada",
            'qr_payload': f"VALIDA-RESERVA-MOCK99-CHALE04-{cpf_obfuscated(request.user)}"
        })

    # 2. Inject beautifully structured mock tickets for Shows
    shows_list = [
        {
            'id': "TKT-SHOW01",
            'titulo': "Ibiapaba Rock Festival 2026",
            'produtora': "Vibe Produções CE",
            'local': "Arena Ibiapaba - Tianguá",
            'data': "14/11/2026 às 21:00",
            'setor': "Ingresso VIP Frontstage",
            'preco_formatado': "R$ 180,00",
            'status': "Ativo",
            'status_slug': "confirmada",
            'qr_payload': f"VALIDA-INGRESSO-SHOW01-VIP-{cpf_obfuscated(request.user)}"
        },
        {
            'id': "TKT-SHOW02",
            'titulo': "Stand Up Comedy: Rindo na Serra",
            'produtora': "Ceará Riso & Arte",
            'local': "Auditório Centro Cultural Ubajara",
            'data': "05/12/2026 às 20:00",
            'setor': "Pista Meia-Entrada",
            'preco_formatado': "R$ 45,00",
            'status': "Ativo",
            'status_slug': "confirmada",
            'qr_payload': f"VALIDA-INGRESSO-SHOW02-PISTAMEIA-{cpf_obfuscated(request.user)}"
        }
    ]

    # 3. Inject beautifully structured mock tickets for Cinema
    cinema_list = [
        {
            'id': "TKT-CINE01",
            'filme': "Batman: O Retorno do Cavaleiro",
            'cinema': "Ciné Naviê - Tianguá Shopping",
            'sala': "Sala 02 VIP - 4K Laser",
            'sessao': "Hoje às 19:30",
            'formato': "3D - Dublado",
            'assento': "Fileira F - Poltrona 12",
            'preco_formatado': "R$ 38,00",
            'status': "Emitido",
            'status_slug': "confirmada",
            'qr_payload': f"VALIDA-INGRESSO-CINE01-SALA02-F12-{cpf_obfuscated(request.user)}"
        }
    ]

    context = {
        'hospedagens': hospedagens_list,
        'shows': shows_list,
        'cinema': cinema_list,
        'perfil': getattr(request.user, 'perfil', None)
    }

    return render(request, 'clientes/painel.html', context)

def cpf_obfuscated(user):
    """
    Helper function to safely extract and obfuscate the user's CPF for the QR payload.
    """
    profile = getattr(user, 'perfil', None)
    if profile:
        cpf = profile.cpf
        # Remove dots and dashes and return obfuscated
        cpf_clean = ''.join(c for c in cpf if c.isdigit())
        if len(cpf_clean) == 11:
            return f"***.{cpf_clean[3:6]}.{cpf_clean[6:9]}-**"
    return "USER-UNKNOWN"
