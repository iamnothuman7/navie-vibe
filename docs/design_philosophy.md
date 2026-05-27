# Naviê Vibe: Filosofia de Design e UX

## 1. Nossa Missão Visual
O Naviê Vibe não é apenas uma plataforma de reservas, é uma experiência de conversão. 
A plataforma deve ser **Amigável, Prática e Simples**. O usuário nunca deve se sentir sobrecarregado por informações ou escolhas complexas.

## 2. A Regra de Ouro: Mínimo Esforço Cognitivo
Toda tela, formulário ou botão deve passar pelo teste do "Mínimo Esforço Cognitivo".
- **Minimalismo Útil:** Se um elemento na tela não ajuda o usuário a tomar uma decisão ou avançar no fluxo, ele não deve existir.
- **Leitura Assertiva:** Textos diretos e sem jargões desnecessários.
- **Tipografia Acolhedora:** Utilizamos `Poppins` para todo o corpo de texto devido à sua legibilidade geométrica e amigável, e `Quicksand` para títulos de destaque, proporcionando um ar moderno, arredondado e acolhedor.

## 3. A Regra dos 3 Passos (Funil de Vendas)
O Naviê foi construído para que o cliente feche uma venda/reserva no menor tempo possível, sem frustrações. O fluxo de compra B2C deve ser estritamente dividido em no máximo 3 passos:

1. **A Escolha:** O usuário visualiza o catálogo (quartos, atividades) de forma limpa, com fotos grandes, preços claros e informações resumidas. (Ex: Página Cinemática do Quarto).
2. **O Pagamento:** Formulário reduzido. Exigimos apenas os dados essenciais para faturamento e processamento do pagamento. Sem páginas longas de cadastro.
3. **A Confirmação:** O cliente recebe seu comprovante/ingresso imediatamente em tela e também via email/WhatsApp de forma instantânea.

## 4. Padrões de Interface (UI)
- **Cores Dinâmicas:** Botões primários sempre refletem a marca da empresa hospedeira (`var(--brand-color)`). O texto interno deve contrastar automaticamente (`var(--brand-text-color)`).
- **Cartões (Cards):** Elementos listáveis (quartos, empresas, eventos) devem usar Cards com cantos arredondados (`rounded-3xl` ou `rounded-2xl`), sombras suaves (`shadow-lg`) e animações de elevação no hover (`hover:-translate-y-1`), transmitindo fisicalidade e interatividade.
- **Ocultação do Desnecessário:** Menus complexos, links de sistema e painéis laterais pesados pertencem ao painel B2B. A visão B2C (cliente) deve focar 100% no produto.
