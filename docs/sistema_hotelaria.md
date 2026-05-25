# Documentação Oficial: Sistema de Gestão Hoteleira (Naviê Hospedagens)

Este documento registra os objetivos, a hierarquia de usuários, os módulos funcionais e a arquitetura de segurança do **Sistema de Gestão Hoteleira (Naviê Hospedagens)**. Esta vertical do portal Naviê Vibe foi projetada para atender de ponta a ponta o mercado de turismo e acomodações na Serra da Ibiapaba, abrangendo **Hotéis, Pousadas, Chalés, Cabanas e Resorts**.

---

## 1. Visão Geral & Filosofia do Produto

O Naviê Hospedagens atua em duas frentes integradas:
1. **Fronteira com o Cliente (B2C):** Catálogo online de acomodações na Ibiapaba, permitindo que turistas busquem, filtrem e reservem de forma transparente e segura.
2. **Back-Office e Operação (B2B):** Um sistema de planejamento e gestão empresarial (ERP) completo para o estabelecimento hoteleiro, garantindo autonomia nas esferas financeira, de equipes, tarifária e governamental.

---

## 2. Níveis de Acesso & Controle de Equipe (Hierarquia)

Para espelhar fielmente a realidade da gestão de hotéis e pousadas, o sistema implementa cinco perfis de colaboradores, cada um com fluxos de trabalho e permissões adaptadas:

### 2.1 Proprietário (`proprietario`)
* **Descrição:** Representa o dono da pousada ou do hotel. É o administrador geral da conta empresarial.
* **Funcionalidades Principais:**
  * Visualização do faturamento bruto consolidado, custos operacionais e margem de lucro líquido.
  * Criação, gerenciamento e inativação de contas de **Gerentes** e outros membros da equipe.
  * Configuração de chaves PIX de recebimento, dados fiscais da empresa e regras gerais de cancelamento.

### 2.2 Gerente (`gerente`)
* **Descrição:** Gestor operacional encarregado da rotina diária e controle financeiro regular do estabelecimento.
* **Funcionalidades Principais:**
  * Cadastro e alteração de diárias, bloqueio de unidades para manutenção ou reservas de balcão (diretas).
  * Lançamento manual de receitas (consumo de frigobar, SPA, passeios locais) e custos (compra de mantimentos, reparos rápidos, produtos de limpeza).
  * Criação de tarefas e distribuição de cronogramas diários para a equipe operacional.
  * Criação de perfis de funcionários operacionais (Portaria, Camareira, Manutenção).

### 2.3 Portaria / Recepção (`portaria`)
* **Descrição:** Funcionários da linha de frente do atendimento ao hóspede.
* **Funcionalidades Principais:**
  * Login rápido e seguro utilizando o **CPF** e senha operacional.
  * Painel de Check-in e Check-out dinâmicos em tempo real.
  * Validador de QR Code das reservas geradas no app para localização imediata da reserva.
  * Controle do mapa de ocupação diária.
  * Atendimento de solicitações internas (pedidos de serviço de quarto, toalhas extras).

### 2.4 Camareira / Equipe de Limpeza (`camareira`)
* **Descrição:** Colaboradores dedicados à conservação e higienização física das acomodações.
* **Funcionalidades Principais:**
  * Interface enxuta projetada prioritariamente para visualização em smartphones e tablets.
  * Lista diária de tarefas a cumprir (higienizações pós-checkout ou preventivas).
  * Botões de controle: "Iniciar Faxina" e "Marcar como Limpo e Disponível" (que atualiza o status do quarto instantaneamente no mapa da portaria).

### 2.5 Equipe de Manutenção (`manutencao`)
* **Descrição:** Profissionais responsáveis pela infraestrutura e reparos gerais (elétrica, hidráulica, pintura).
* **Funcionalidades Principais:**
  * Lista de ordens de serviço pendentes geradas pelo Gerente ou informadas pelas camareiras.
  * Abertura direta de avisos de defeito com controle de nível de urgência (Ex: Ar-condicionado quebrado).
  * Botão de liberação rápida ("Reparo Concluído") para reintegração automática do quarto ao inventário ativo.

---

## 3. Módulos Estruturais

### 3.1 Gestão e Cadastro de Quartos (Acomodações)
O sistema permite cadastrar e organizar acomodações de forma estruturada:
* **Categorias de Quarto (`Quarto`):** Definição lógica com descrição, fotos, comodidades (ar-condicionado, banheira, vista para a serra), capacidade máxima de adultos/crianças e preço base.
* **Unidades Físicas (`UnidadeQuarto`):** Cadastro individual das unidades reais existentes (Ex: "Suíte 101", "Chalé 04", "Chalé Master 02"), permitindo total controle individual de cada cômodo.
* **Bloqueio Temporário:** Ferramenta para desabilitar unidades do inventário B2C temporariamente por motivos de avarias estruturais ou reserva corporativa exclusiva offline.

### 3.2 Motor Tarifário Dinâmico & Campanhas Promocionais
Permite a flexibilização inteligente de preços para maximizar a taxa de ocupação:
* **Tarifação Sazonal:** Definição de taxas diferenciadas para feriados locais, finais de semana ou alta temporada serrana (como no inverno da Ibiapaba).
* **Cupons de Desconto:** Geração de códigos promocionais configuráveis (ex: `INVERNO20`), com regras de validade temporal, valor fixo ou percentual e limite de utilizações.
* **Descontos Progressivos:** Reduções automáticas na diária média para estadias de longa duração (Ex: Pacotes semanais).

### 3.3 Gerenciador Financeiro Integrado
Centraliza e organiza todas as finanças do negócio, reduzindo custos com softwares terceiros:
* **Controle de Caixa:** Painel contábil separando receitas geradas (diárias de reservas, consumo no local) e despesas (folha salarial, insumos, lavanderia).
* **Comissionamento da Plataforma:** Cálculo automático da taxa operacional cobrada pelo Naviê Vibe (padrão de 10% sobre reservas originadas online).
* **Demonstrativo de Lucros:** Relatórios automáticos de faturamento, margem de lucratividade mensal e tíquete médio de gasto por reserva.

### 3.4 Gestão de Atividades Operacionais (Workflow)
Automação inteligente do fluxo operacional físico do estabelecimento:
* **Geração Automática de Faxina:** Sempre que um hóspede realiza o checkout através da recepção, o sistema gera de forma automática uma tarefa de limpeza pesada para a equipe de camareiras na unidade.
* **Distribuição Inteligente:** O sistema equilibra as tarefas de forma uniforme entre a equipe de camareiras ativa.

### 3.5 Integração com Governo & Regulamentações
* **FNRH (Ficha Nacional de Registro de Hóspedes):** Campos obrigatórios de coleta exigidos pela Embratur e Ministério do Turismo do Brasil (SNHRs).
* **Emissão Rápida:** Simplificação do envio eletrônico de fichas cadastrais no momento de validação do check-in.

### 3.6 Portal de Pedidos Digitais (Guest Portal)
* **SPA & Room Service Digital:** Cada acomodação física recebe um adesivo com QR Code exclusivo. Ao escanear, o hóspede é direcionado para uma interface local no celular onde pode pedir lanches, bebidas, solicitar reposição de amenities ou agendar serviços de bem-estar.
* **Lançamento Automático:** Os valores de consumação aprovados pela recepção entram de forma transparente na fatura consolidada do cliente para quitação no check-out.

---

## 4. Segurança e Isolamento Arquitetural

* **Sharding Físico de Banco de Dados:** Todos os dados da vertical de hotelaria são direcionados para o arquivo de banco de dados exclusivo `db_hospedagem.sqlite3`. Isso garante total proteção e conformidade (a falha em outra vertical, como cinema ou eventos, jamais expõe ou indisponibiliza os dados de gestão da pousada).
* **Prevenção IDOR (UUIDs):** Reservas e transações financeiras geram IDs no padrão UUIDv4 de 128 bits, impossibilitando tentativas de adivinhação sequencial de faturas ou dados sensíveis.
* **Administração de Credenciais Operacionais:** Gerentes e Proprietários administram a criação e o reset de senhas diretamente para a equipe operacional de campo, diminuindo gargalos e otimizando a rotina corporativa.
