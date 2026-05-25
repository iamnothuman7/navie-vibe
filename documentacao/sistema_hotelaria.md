# Documentação Oficial: Sistema de Gestão Hoteleira (Naviê Hospedagens)

Este documento descreve a visão geral, objetivos, arquitetura, controle de acessos e o roadmap de recursos do **Sistema de Gestão Hoteleira (Naviê Hospedagens)**. Esta plataforma foi concebida para fornecer independência operacional absoluta a hotéis, pousadas, chalés e resorts parceiros da Serra da Ibiapaba, permitindo o gerenciamento de ponta a ponta do seu negócio.

---

## 1. Visão Geral & Objetivos

O objetivo do Naviê Hospedagens é ser uma ferramenta tão completa e vital que os estabelecimentos parceiros tornem-se dependentes de suas funcionalidades para funcionar no dia a dia. A plataforma resolve a vida do hotel em duas frentes:
1. **Fronteira com o Hóspede (B2C):** Reserva fácil, pedidos de serviço de quarto via celular, check-in digital simplificado e acesso a recibos.
2. **Operação e Back-Office (B2B):** Gestão financeira robusta, coordenação de atividades da equipe de limpeza e manutenção, controle tarifário dinâmico, promoções e cumprimento de regulamentações governamentais.

---

## 2. Níveis de Acesso & Controle de Equipe (Hierarquia)

Para refletir a hierarquia real das pousadas e hotéis, o sistema opera com 5 perfis de usuários com restrições lógicas e telas adaptadas:

### 2.1 Proprietário (`proprietario`)
* **Poder:** Total sobre o estabelecimento.
* **Funcionalidades Exclusivas:**
  * Visualização de faturamento global, relatórios financeiros consolidados e lucros.
  * Criação, edição e exclusão de contas de **Gerentes** e **Funcionários**.
  * Configuração de dados fiscais, bancários e regras de cancelamento da empresa.

### 2.2 Gerente (`gerente`)
* **Poder:** Operacional e financeiro completo.
* **Funcionalidades:**
  * Gerenciamento de quartos (bloqueios, tarifas, check-in, check-out).
  * Aprovação ou recusa manual de reservas solicitadas.
  * Lançamento manual de despesas (custos, compras) e receitas (consumo no bar, passeios).
  * Criação e atribuição de atividades/tarefas para a equipe de funcionários.
  * Criação de perfis de funcionários operacionais (Portaria, Camareiras, Manutenção).

### 2.3 Recepção / Portaria (`portaria`)
* **Poder:** Controle de tráfego de hóspedes.
* **Funcionalidades:**
  * Login rápido utilizando o **CPF** e senha (evita usernames complexos).
  * Tela dedicada de Check-in e Check-out em tempo real.
  * Leitor de QR Code para validação e busca instantânea de reservas no momento da chegada do hóspede.
  * Visualização do mapa de ocupação (quem está em qual quarto).
  * Painel de monitoramento de solicitações de hóspedes (pedidos de toalhas, serviço de quarto).

### 2.4 Camareira / Equipe de Limpeza (`camareira`)
* **Poder:** Controle de higienização de unidades.
* **Funcionalidades:**
  * Interface simplificada focada em dispositivos móveis (smartphone).
  * Visualização exclusiva da sua lista de tarefas diárias de limpeza (ex: "Limpar Chalé 03").
  * Botão de "Iniciar Limpeza" e "Marcar como Limpo/Pronto", que atualiza o mapa de ocupação da recepção instantaneamente.

### 2.5 Equipe de Manutenção (`manutencao`)
* **Poder:** Controle de reparos de infraestrutura.
* **Funcionalidades:**
  * Visualização de ordens de serviço pendentes nos quartos (ex: "Trocar lâmpada do quarto 102").
  * Opção de abrir relatos de problemas observados para aprovação do Gerente.
  * Botão de "Manutenção Concluída" para liberar o quarto de volta ao mapa operacional.

---

## 3. Módulos & Recursos Planejados

O sistema é composto por módulos específicos interligados que garantem a gestão holística da hospedagem:

### 3.1 Gestão de Unidades e Quartos (Inventário)
* **Cadastro Flexível:** Suporte a múltiplos tipos de hospedagem: hotéis convencionais, pousadas ecológicas, chalés rústicos e áreas de camping.
* **Tipos de Acomodação:** Cadastro de categorias de quartos (ex: Suíte Master, Chalé Master) com descrição, fotos, capacidade máxima e comodidades.
* **Unidades Físicas:** Cadastro de salas reais associadas a cada categoria (ex: Quarto 101, Chalé 05).
* **Bloqueio de Unidades:** Opção de bloquear quartos específicos temporariamente por motivos de manutenção, reserva direta externa ou indisponibilidade sazonal.

### 3.2 Motor Tarifário Dinâmico & Promoções
* **Tarifas por Temporada:** Configuração de valores diferenciados para dias de semana, finais de semana, feriados e alta temporada.
* **Cupons de Desconto:** Criação de códigos promocionais customizados (ex: `SERRA10`), com validade temporal e limite de usos.
* **Promoções Especiais:** Lançamento de ofertas do tipo "Pague 2, Leve 3" ou descontos progressivos para estadias de longa duração.

### 3.3 Gerenciador Financeiro Integrado
* **Fluxo de Caixa:** Lançamento de entradas (pagamento de reservas, consumo, passeios) e saídas (salários, contas de luz, compras de mantimentos).
* **Taxas & Comissões:** Cálculo automático da taxa de intermediação da plataforma Naviê Vibe (ex: comissão padrão de 10% sobre reservas geradas via app).
* **Faturamento Dinâmico:** Relatórios de lucratividade, tíquete médio por hóspede e taxa de ocupação mensal.

### 3.4 Gestão de Atividades Operacionais (Workflow)
* **Distribuição de Tarefas:** Geração automática de tarefas de limpeza na saída do hóspede (Check-out) ou tarefas de higienização recorrente para estadias longas.
* **Alertas Visuais:** Painel de controle no dashboard do gerente mostrando o tempo médio de limpeza e tarefas em atraso.

### 3.5 Integração com Governo & Regulamentações
* **FNRH (Ficha Nacional de Registro de Hóspedes):** Adequação às exigências da Embratur e do Ministério do Turismo brasileiro (SNHRs).
* **Fluxo Gov.br:** Integração ou preenchimento de campos oficiais exigidos por lei para coleta e envio automático de dados de hóspedes estrangeiros e nacionais no momento do check-in.

### 3.6 Portal de Pedidos Digitais (Guest Portal)
* **Serviço de Quarto Digital:** O hóspede escaneia um QR Code colado no quarto e acessa um menu digital no celular para pedir café da manhã, toalhas extras, bebidas ou serviços de SPA.
* **Comanda Digital:** O pedido é enviado diretamente para a recepção ou cozinha, e o valor é lançado automaticamente na comanda do quarto para pagamento no check-out.

---

## 4. Segurança & Arquitetura de Banco de Dados

* **Isolamento Físico de Banco de Dados:** Conforme o design de sharding de dados, todas as tabelas deste aplicativo residem na conexão dedicada `hospedagem` (`db_hospedagem.sqlite3`), impedindo fisicamente que falhas em outras verticais comprometam os dados hoteleiros.
* **UUIDs e Prevenção IDOR:** Todas as IDs expostas em URLs e transações financeiras utilizam hashes UUID4 não sequenciais de 128 bits para barrar tentativas de varredura ou acessos não autorizados a recursos de terceiros.
* **Senhas Operacionais:** Gerentes têm o poder de redefinir as credenciais das equipes operacionais sob demanda, eliminando a dependência de fluxos complexos de recuperação por e-mail para funcionários de campo.
