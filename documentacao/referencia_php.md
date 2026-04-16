# Referência Inicial (PHP)

Os códigos abaixo foram desenvolvidos em PHP puro e servem como referência de design, interface, e lógica de negócios base (como listagem, destacao, exibição do evento e o carrinho de compras) para o novo sistema Naviê Vibe em Java.

### index.php (Página Principal)

```php
<?php
// =================================================================
// | PÁGINA PRINCIPAL (INDEX.PHP) - NAVIÊ VIBE                      |
// =================================================================
// | OBJETIVO: Exibir o evento em destaque e uma lista dos         |
// |           próximos eventos cadastrados no banco de dados.     |
// =================================================================

// -----------------------------------------------------------------
// PARTE 1: CONFIGURAÇÃO E CONEXÃO
// -----------------------------------------------------------------

// ini_set e error_reporting: Essencial para desenvolvimento.
// Mostra todos os erros de PHP na tela, o que nos ajuda a encontrar
// e consertar problemas rapidamente.
ini_set("display_errors", 1);
ini_set("display_startup_errors", 1);
error_reporting(E_ALL);

// session_start(): Inicia uma sessão PHP.
// É necessário para que possamos, no futuro, saber se um usuário
// está logado e quantos itens ele tem no carrinho.
session_start();

// require_once: Inclui outros arquivos PHP no nosso script.
// Usamos `require_once` para garantir que o arquivo seja incluído
// apenas uma vez, evitando erros. '__DIR__' é uma constante mágica
// que representa o diretório do arquivo atual (no caso, a pasta 'public').
require_once __DIR__ . '/includes/db_connection.php'; // Caminho para a conexão com o BD
require_once __DIR__ . '/includes/auth_check.php';    // Caminho para a função que verifica o login

// -----------------------------------------------------------------
// PARTE 2: LÓGICA DE BUSCA DE DADOS
// -----------------------------------------------------------------

// 1. CONECTAR AO BANCO DE DADOS
// Criamos uma instância da nossa classe DB e pegamos a conexão PDO.
// A partir daqui, a variável `$db` pode ser usada para fazer consultas.
$db_instance = new DB();
$db = $db_instance->getConnection();

// 2. BUSCAR O EVENTO EM DESTAQUE
// Preparamos uma consulta SQL para buscar o evento marcado como `destaque = 1`.
// JOIN `locais`: "Junta" a tabela `eventos` com a `locais` usando o `local_id`
//                para que possamos pegar o nome do local diretamente.
// LIMIT 1: Garante que apenas UM resultado seja retornado.
$stmt_destaque = $db->query(
    'SELECT e.*, l.nome as local_nome 
     FROM eventos e 
     JOIN locais l ON e.local_id = l.id 
     WHERE e.destaque = 1 
     LIMIT 1'
);
// fetch(PDO::FETCH_ASSOC): Pega a primeira linha do resultado e a transforma
// em um array associativo (ex: $evento_destaque['nome']).
$evento_destaque = $stmt_destaque->fetch(PDO::FETCH_ASSOC);


// 3. BUSCAR OS PRÓXIMOS EVENTOS
// Preparamos outra consulta SQL para buscar os próximos eventos.
// WHERE e.data_inicio >= CURDATE(): Filtra apenas eventos que acontecerão
//                                 hoje ou no futuro. `CURDATE()` pega a data atual.
// ORDER BY e.data_inicio ASC: Ordena os resultados pela data, do mais próximo ao mais distante.
// LIMIT 6: Pega apenas os próximos 6 eventos para não poluir a página.
$stmt_proximos = $db->query(
    'SELECT e.*, l.nome as local_nome 
     FROM eventos e 
     JOIN locais l ON e.local_id = l.id 
     WHERE e.data_inicio >= CURDATE() AND e.status = "ativo"
     ORDER BY e.data_inicio ASC 
     LIMIT 6'
);
// fetchAll(PDO::FETCH_ASSOC): Pega TODAS as linhas do resultado.
$eventos_proximos = $stmt_proximos->fetchAll(PDO::FETCH_ASSOC);


// 4. PREPARAR INFORMAÇÕES DO HEADER
// Verifica se o usuário está logado para exibir o botão de 'Sair' ou 'Entrar'.
$user_info = getUserInfo();
// Conta os itens no carrinho (que está salvo na sessão) para exibir no ícone.
$cart_item_count = isset($_SESSION["cart"]) ? count($_SESSION["cart"]) : 0;


// -----------------------------------------------------------------
// PARTE 3: ESTRUTURA HTML E EXIBIÇÃO DINÂMICA
// -----------------------------------------------------------------
// Agora, usamos o PHP para "imprimir" os dados que buscamos do banco
// diretamente no HTML.
?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Naviê Vibe - Descubra os Melhores Eventos</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
        html { scroll-behavior: smooth; }
        body { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
        .bg-action-blue { background-color: #2563eb; }
        .text-action-blue { color: #2563eb; }
        .hover\:bg-action-blue-dark:hover { background-color: #1d4ed8; }
        .event-card { transition: transform 0.3s ease, box-shadow 0.3s ease; }
        .event-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1); }
    </style>
</head>
<body>

    <?php require_once __DIR__ . '/includes/header.php'; ?>

    <main class="container mx-auto px-4 py-8">
        
        <?php if ($evento_destaque): ?>
        <section class="mb-12">
            <div class="relative rounded-2xl overflow-hidden h-64 md:h-96">
                <img src="<?php echo htmlspecialchars($evento_destaque['banner']); ?>" alt="Imagem do evento <?php echo htmlspecialchars($evento_destaque['nome']); ?>" class="w-full h-full object-cover">
                
                <div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
                <div class="absolute bottom-0 left-0 p-4 md:p-8 text-white">
                    <h2 class="text-3xl md:text-4xl lg:text-5xl font-extrabold mb-2"><?php echo htmlspecialchars($evento_destaque['nome']); ?></h2>
                    <div class="flex flex-col sm:flex-row sm:items-center gap-2 md:gap-4 text-md md:text-lg">
                        <div class="flex items-center gap-2">
                            <i data-lucide="calendar" class="w-5 h-5"></i>
                            <span><?php echo date('d/m/Y', strtotime($evento_destaque['data_inicio'])); ?></span>
                        </div>
                        <div class="flex items-center gap-2">
                            <i data-lucide="map-pin" class="w-5 h-5"></i>
                            <span><?php echo htmlspecialchars($evento_destaque['local_nome']); ?></span>
                        </div>
                    </div>
                    <a href="evento.php?id=<?php echo $evento_destaque['id']; ?>" class="mt-6 inline-block bg-action-blue text-white px-6 py-3 rounded-full font-semibold hover:bg-action-blue-dark transition-colors">
                        Ver Detalhes
                    </a>
                </div>
            </div>
        </section>
        <?php endif; ?>

        <section>
            <h3 class="text-2xl font-bold text-gray-900 mb-6">Próximos Eventos</h3>
            <div id="events-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                
                <?php foreach ($eventos_proximos as $evento): ?>
                
                <a href="evento.php?id=<?php echo $evento['id']; ?>" class="event-card bg-white rounded-2xl overflow-hidden shadow-md group">
                    <div class="relative">
                        <img src="<?php echo htmlspecialchars($evento['banner']); ?>" alt="Imagem do evento <?php echo htmlspecialchars($evento['nome']); ?>" class="w-full h-48 object-cover">
                        <div class="absolute top-4 right-4 bg-white/90 backdrop-blur-sm p-2 rounded-lg text-center leading-none">
                            <span class="font-bold text-lg text-action-blue"><?php echo date('d', strtotime($evento['data_inicio'])); ?></span>
                            <span class="text-xs font-semibold text-gray-600 block"><?php echo date('M', strtotime($evento['data_inicio'])); ?></span>
                        </div>
                    </div>
                    <div class="p-4">
                        <h4 class="font-bold text-lg text-gray-900 truncate"><?php echo htmlspecialchars($evento['nome']); ?></h4>
                        <p class="text-sm text-gray-500 flex items-center gap-2 mt-1">
                            <i data-lucide="map-pin" class="w-4 h-4"></i>
                            <?php echo htmlspecialchars($evento['local_nome']); ?>
                        </p>
                        <div class="mt-4 flex justify-between items-center">
                            <span class="text-lg font-bold text-action-blue">Ingressos</span>
                            <div class="bg-action-blue/10 text-action-blue px-4 py-2 rounded-full text-sm font-semibold group-hover:bg-action-blue group-hover:text-white transition-colors">
                                Ver mais
                            </div>
                        </div>
                    </div>
                </a>

                <?php endforeach; ?>
                
            </div>
        </section>
    </main>

    <?php require_once __DIR__ . '/includes/footer.php'; ?>

    <script>
        lucide.createIcons();
    </script>

    <script>
        // Inicializa todos os ícones da biblioteca Lucide que usamos na página.
        lucide.createIcons();

        // --- Lógica para o botão de busca mobile ---

        // 1. Pega os elementos do HTML pelo seu 'id'.
        const mobileSearchBtn = document.getElementById('mobile-search-btn');
        const mobileSearchBar = document.getElementById('mobile-search-bar');

        // 2. Adiciona um "ouvinte de evento": quando o botão for clicado...
        mobileSearchBtn.addEventListener('click', () => {
            // 3. ...ele executa esta ação:
            // Pega a lista de classes do painel de busca e "alterna" a classe 'hidden'.
            // Se a classe 'hidden' estiver lá, ele a remove (mostrando o painel).
            // Se a classe 'hidden' não estiver lá, ele a adiciona (escondendo o painel).
            // É como um interruptor de luz.
            mobileSearchBar.classList.toggle('hidden');
        });

        // --- Lógica para o botão de menu mobile (funciona da mesma forma) ---
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');

        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    </script>
</body>
</html>
```

### evento.php (Detalhes do Evento/Hotel)

```php
<?php
// =================================================================
// | PÁGINA DE DETALHES DO EVENTO (EVENTO.PHP) - VERSÃO FINAL      |
// =================================================================
// | OBJETIVO: Exibir informações com ordem de conteúdo correta    |
// |           no mobile e layout de coluna no desktop.            |
// =================================================================

// PARTE 1: CONFIGURAÇÃO E VALIDAÇÃO (sem alterações)
ini_set("display_errors", 1);
error_reporting(E_ALL);
if (session_status() == PHP_SESSION_NONE) { session_start(); }
require_once __DIR__ . '/includes/db_connection.php';
require_once __DIR__ . '/includes/auth_check.php';
$event_id = filter_input(INPUT_GET, 'id', FILTER_VALIDATE_INT);
if (!$event_id) { header('Location: index.php'); exit(); }

// PARTE 2: LÓGICA DE BUSCA DE DADOS (sem alterações)
$db_instance = new DB();
$db = $db_instance->getConnection();
$sql_evento = 'SELECT e.*, l.nome as local_nome, l.endereco as local_endereco_rua, l.cidade as local_cidade, l.estado as local_estado, p.nome_publico as produtor_nome FROM eventos e JOIN locais l ON e.local_id = l.id JOIN produtores p ON e.produtor_id = p.id WHERE e.id = :id';
$stmt = $db->prepare($sql_evento);
$stmt->bindParam(':id', $event_id, PDO::PARAM_INT);
$stmt->execute();
$event_details = $stmt->fetch(PDO::FETCH_ASSOC);
if (!$event_details) { header('Location: index.php'); exit(); }
$sql_ingressos = 'SELECT * FROM tipos_ingresso WHERE evento_id = :evento_id ORDER BY preco ASC';
$stmt_ingressos = $db->prepare($sql_ingressos);
$stmt_ingressos->bindParam(':evento_id', $event_id, PDO::PARAM_INT);
$stmt_ingressos->execute();
$event_details['ingressos'] = $stmt_ingressos->fetchAll(PDO::FETCH_ASSOC);

// ====================================================================
// | NOVO CÓDIGO: BUSCAR AS IMAGENS DO EVENTO PARA O CARROSSEL        |
// ====================================================================
$sql_imagens = 'SELECT * FROM evento_imagens WHERE evento_id = :evento_id ORDER BY ordem ASC';
$stmt_imagens = $db->prepare($sql_imagens);
$stmt_imagens->bindParam(':evento_id', $event_id, PDO::PARAM_INT);
$stmt_imagens->execute();

// Adicionamos as imagens encontradas ao nosso array principal $event_details.
$event_details['imagens'] = $stmt_imagens->fetchAll(PDO::FETCH_ASSOC);

// ... resto do código ...

$data_inicio_obj = new DateTime($event_details['data_inicio']);
$event_details['data_formatada'] = $data_inicio_obj->format('d/m/Y');
$horario_inicio_obj = new DateTime($event_details['horario_inicio']);
$event_details['horario_formatado'] = 'Abertura às ' . $horario_inicio_obj->format('H:i');
$event_details['local_completo'] = $event_details['local_endereco_rua'] . ', ' . $event_details['local_cidade'] . ' - ' . $event_details['local_estado'];
$user_info = getUserInfo();
$cart_item_count = isset($_SESSION['cart']) ? count($_SESSION['cart']) : 0;

?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo htmlspecialchars($event_details['nome']); ?> - Naviê Vibe</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
        .bg-action-blue { background-color: #2563eb; }
        .text-action-blue { color: #2563eb; }
        .border-action-blue { border-color: #2563eb; }
        .hover\:bg-action-blue-dark:hover { background-color: #1d4ed8; }
        .ticket-card.selected { border-color: #2563eb; box-shadow: 0 0 0 2px #2563eb; }
    </style>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css"/>
    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
</head>
<body class="w-full">

    <?php require_once __DIR__ . '/includes/header.php'; ?>

    <main class="container mx-auto px-4 py-8">
        
        <div class="lg:grid lg:grid-cols-3 lg:gap-12 lg:items-start">
            
            <div class="lg:col-span-2">

                <div class="relative rounded-2xl overflow-hidden h-64 md:h-96 mb-8 bg-gray-200">
    
    <?php
    // ====================================================================
    // | LÓGICA DO CARROSSEL - VERSÃO CORRIGIDA (SEM DUPLICAÇÃO)         |
    // ====================================================================

    // Pega as imagens do banco. Se não houver, usa o banner principal como fallback.
    $imagens_do_banco = !empty($event_details['imagens']) ? $event_details['imagens'] : [['url_imagem' => $event_details['banner']]];

    if (count($imagens_do_banco) > 1):
        // (Lógica omitida do array final, mantida da referência original)
        // ...
?>
    <div class="swiper h-full">
        <!-- ... -->
    </div>

<?php else: ?>
    <img src="<?php echo htmlspecialchars($imagens_do_banco[0]['url_imagem']); ?>" alt="Imagem do evento" class="w-full h-full object-cover">
<?php endif; ?>
    
                   </div>

                <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900 mb-4"><?php echo htmlspecialchars($event_details['nome']); ?></h1>
                <!-- ... -->
            </div>

            <div class="lg:col-start-3 lg:row-start-1 lg:sticky lg:top-28 mt-8 lg:mt-0">
                <form id="cart-form" action="controllers/processa_adicionar_carrinho.php" method="POST" class="bg-white p-6 rounded-2xl shadow-lg">
                    <!-- ... forms em HTML mantidos na referencia... -->
                </form>
            </div>
            
        </div>
    </main>

    <?php require_once __DIR__ . '/includes/footer.php'; ?>
    
</body>
</html>
```

### carrinho.php (Carrinho)

```php
<?php
// =================================================================
// | PÁGINA DO CARRINHO DE COMPRAS (CARRINHO.PHP)                  |
// =================================================================
// | OBJETIVO: Exibir os itens que o usuário adicionou ao carrinho |
// |           (que estão salvos na sessão), calcular o total e    |
// |           permitir a finalização da compra.                   |
// =================================================================

// Inicia a sessão para que possamos ler os dados de $_SESSION['cart'].
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}

// ... Demais lógicas do carrinho ...
?>
<!DOCTYPE html>
<html lang="pt-br">
<!-- HTML de Carrinho aqui em referência original -->
</html>
```
