# Monitor de Promoções no Telegram

Monitore produtos em canais e grupos do Telegram e receba alertas com comparação de preço e filtros personalizados!

Projeto pessoal desenvolvido em Python para automatizar o acompanhamento de ofertas. A aplicação usa regras de texto e reconhecimento de preços; não utiliza modelos de inteligência artificial.

## Demonstração

A demonstração apresenta o cadastro de filtros, a identificação de ofertas, a comparação com metas de preço e a remoção de produtos com confirmação.

<p align="center">
  <img width="720" height="790" alt="demo" src="https://github.com/user-attachments/assets/9362679f-1eed-4302-bd21-fae397dd2ba0" />

  ###### Os produtos e preços utilizados na demonstração são fictícios e não representam anúncios ou recomendações de compra.
</p>

## O que o projeto oferece

- Filtros com ou sem meta de preço e cadastro de várias regras em um comando.
- Alertas classificados como dentro da meta, próximos da meta ou acima da meta.
- Margens de tolerância configuráveis por faixa de preço.
- Seleção de canais e grupos, pausa e retomada do monitoramento.
- Exportação de filtros como comandos prontos para copiar e colar.
- Comandos restritos à conta autorizada.

## Como funciona

1. **Leitura:** uma conta Telegram autenticada pelo Telethon acompanha novas mensagens nos canais e grupos aos quais tem acesso.
2. **Filtro:** o conteúdo é comparado com os termos cadastrados.
3. **Preço:** quando a regra tem uma meta, a aplicação tenta identificar o valor e classificá-lo.
4. **Alerta:** um bot criado no BotFather envia o resultado para o chat configurado.

**A conta leitora e o bot têm funções diferentes.** A conta precisa participar das origens monitoradas; o bot é responsável pelo envio dos alertas. A implementação é destinada a um único usuário autorizado, não a um serviço com contas independentes para vários usuários.

## Exemplo rápido

Na conversa privada com o bot, usando a conta autorizada, envie:

```text
/add notebook exemplo < 5000
```

Uma nova mensagem contendo os termos “notebook” e “exemplo”, com o preço `R$ 4.499,00`, poderá gerar:

```text
🟢 DENTRO DA META

Filtro: notebook exemplo
Preço identificado: R$ 4.499,00
Meta: R$ 5.000,00
```

O alerta também inclui o texto original e o nome da origem. Os termos são comparados sem diferenciar maiúsculas de minúsculas; todas as palavras do filtro precisam aparecer na mensagem, mas não necessariamente juntas.

## Instalação local

### 1. Prepare os requisitos

Você precisará de:

- Python com suporte às dependências de `requirements.txt` e Git instalados.
- Uma conta Telegram que participe dos canais ou grupos desejados.
- Uma aplicação Telegram, criada em [my.telegram.org](https://my.telegram.org), para obter `API_ID` e `API_HASH`.
- Um bot criado pelo [@BotFather](https://t.me/BotFather), para obter `BOT_TOKEN`.
- Uma instância MongoDB acessível pela aplicação.
- O ID numérico da sua conta e o ID do chat que receberá os alertas.

### 2. Baixe o projeto e instale as dependências

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/victor-rk/telegram-monitor-promocoes.git
cd telegram-monitor-promocoes
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no **Windows — PowerShell**:

```powershell
.venv\Scripts\Activate.ps1
```

Ou no **Linux/macOS**:

```bash
source .venv/bin/activate
```

Depois instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Nos sistemas em que o executável se chama `python3`, substitua `python` por `python3`.

### 3. Onde obter cada credencial

#### Criar o bot e obter o BOT_TOKEN

1. Abra o Telegram e acesse o [BotFather oficial](https://t.me/BotFather).
2. Envie `/newbot`.
3. Escolha o nome exibido, por exemplo, **Meu Monitor de Ofertas**.
4. Escolha um username disponível terminado em `bot`, por exemplo, `meu_monitor_ofertas_bot`.
5. O BotFather retornará um token. Guarde-o como `BOT_TOKEN`.
6. Abra o link do bot (por exemplo, `t.me/meu_monitor_ofertas_bot`) criado e pressione **Iniciar / Start**.

Você não precisa adicionar esse bot aos canais de ofertas: quem lê as mensagens é a conta autenticada no Telethon.

<!-- PRINT: conversa com o BotFather mostrando /newbot e a escolha do nome. Oculte integralmente o token antes de enviar a imagem ao GitHub. -->

#### Obter API_ID e API_HASH

1. Acesse [my.telegram.org](https://my.telegram.org).
2. Entre com o número da conta que participará dos canais e confirme o código recebido pelo Telegram.
3. Abra **API development tools**.
4. Se ainda não houver uma aplicação, preencha os dados solicitados e crie uma aplicação para uso próprio.
5. Copie **App api_id** para `API_ID` e **App api_hash** para `API_HASH`.

Essas credenciais pertencem à aplicação Telegram; são diferentes do token entregue pelo BotFather.

#### Descobrir OWNER_ID e CHAT_ID

Para receber alertas na sua conversa privada com o bot:

1. Usando a mesma conta que será autenticada no Telethon, abra o bot criado e envie uma mensagem, como `Olá`.
2. Antes de iniciar o projeto, consulte o método oficial `getUpdates` no navegador, substituindo o marcador pelo seu token:

```text
https://api.telegram.org/botSEU_BOT_TOKEN/getUpdates
```

3. Na resposta, localize a mensagem que você acabou de enviar.
4. Copie `"message":{.."from":{"id":...}}` para `OWNER_ID`.
5. Copie `"message":{.."chat":{"id":...}}` para `CHAT_ID`. Em uma conversa privada comum com sua própria conta, esses dois valores coincidem.

Use somente o número, sem aspas, parênteses ou `Long`. Se `result` estiver vazio, envie uma nova mensagem ao bot e atualize a consulta. Um webhook previamente configurado nesse mesmo bot pode impedir a consulta; prefira um bot novo para este projeto.

**O token aparece no endereço da consulta. Não compartilhe esse endereço nem tire prints da barra do navegador.** Feche a página após copiar os IDs.

#### Criar o banco no MongoDB Atlas

1. Acesse [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register), crie sua conta e um projeto.
2. Crie um cluster/deployment escolhendo região e modalidade adequadas ao seu uso. Confira os custos antes de confirmar.
3. Em **Database Access / Database Users**, crie um usuário de banco com senha própria e permissão de leitura e escrita no banco `telegram_bot`. Esse usuário não é o login da sua conta Atlas.
4. Em **Network Access / IP Access List**, permita o IP do computador que executará o teste local.
5. Abra o cluster e clique em **Connect → Drivers**. Escolha **Python** e copie a connection string.
6. Na URL copiada, substitua `<username>` pelo usuário criado em Database Access e `<password>` pela senha definida para ele. Depois, salve a URL completa na variável `MONGO_URI` do arquivo `.env`. Se a senha tiver caracteres especiais, codifique-os para URL.
7. Salve a URI completa em `MONGO_URI`.

A aplicação cria a configuração na coleção `telegram_bot.config` ao iniciar; não é necessário inserir um documento manualmente.

Para hospedar no Render, a lista de acesso do Atlas também precisa permitir os endereços de saída do serviço. Consulte os dados de rede do serviço no Render e adicione os intervalos correspondentes. Não libere acesso de qualquer IP apenas para contornar uma falha de conexão.

<!-- PRINT: tela Connect → Drivers com o campo da URI totalmente oculto. Não exiba usuário, senha ou connection string real. -->

Os nomes dos menus podem variar. Consulte o [guia oficial de conexão do Atlas](https://www.mongodb.com/docs/atlas/connect-to-database-deployment/) se a interface for diferente.

### 4. Gere a sessão da conta leitora

Execute localmente:

```bash
python gerar_sessao.py
```

Informe o API ID, o API Hash e os dados solicitados pelo Telegram para autenticar sua própria conta. Copie a sessão gerada para `SESSION_STRING`.

**A sessão permite acesso à conta autenticada.** Não a envie a terceiros, não a mostre em gravações e não a publique no repositório.

### 5. Configure o ambiente

Crie uma cópia de `.env.example` chamada `.env` na raiz do projeto e preencha:

| Variável | Conteúdo |
|---|---|
| `API_ID` | ID numérico da aplicação Telegram. |
| `API_HASH` | Hash da mesma aplicação. |
| `BOT_TOKEN` | Token fornecido pelo BotFather. |
| `CHAT_ID` | ID do chat que receberá as respostas e os alertas. |
| `SESSION_STRING` | Sessão gerada por `gerar_sessao.py`. |
| `MONGO_URI` | URI de conexão com o MongoDB, incluindo as credenciais necessárias. |
| `OWNER_ID` | ID numérico da conta autorizada a enviar comandos. |
| `PORT` | Porta HTTP; o padrão é `10000`. |

Para uso individual, use sua própria conta em `OWNER_ID` e seu chat privado com o bot como destino em `CHAT_ID`. Inicie a conversa com o bot antes de executar a aplicação.

O banco utilizado pelo código é `telegram_bot`, com a coleção `config`. Alterar apenas o nome do banco no caminho da URI não muda essa seleção definida no código.

### 6. Inicie a aplicação

```bash
python bot.py
```

Com o processo em execução, envie `/status` na conversa privada com o bot, a partir da conta definida em `OWNER_ID`.

As respostas são enviadas ao `CHAT_ID` configurado. A aplicação precisa permanecer em execução para processar mensagens e comandos.

## Utilização

### Cadastrar e consultar filtros

Sem meta:

```text
/add mouse sem fio
```

Com meta:

```text
/add notebook exemplo < 5000
```

Vários filtros em uma mensagem:

```text
/add teclado aurora demo < 300, fone orbita demo < 250
```

Use valores como `5000`, `5.000` ou `3.000,50`. Separe as regras por vírgula e não utilize vírgulas no nome do produto.

| Comando | Ação |
|---|---|
| `/list` | Lista os filtros e seus números. |
| `/rem 2` | Remove o segundo filtro da lista atual. |
| `/rem notebook exemplo < 5000` | Remove a regra informada exatamente como cadastrada. |
| `/export` | Retorna um ou mais comandos de cadastro para copiar e guardar. |
| `/remall` | Solicita confirmação para excluir todos os filtros. |
| `/remall confirmar` | Confirma a exclusão dentro de dois minutos da solicitação. |
| `/cancelar` | Cancela a confirmação pendente. |

**A exclusão confirmada remove todos os filtros dessa configuração.** Guarde uma cópia de `/export` antes de testar esse fluxo com dados pessoais.

### Entender as classificações

| Resultado | Significado |
|---|---|
| 🟢 Dentro da meta | Preço identificado menor ou igual à meta. |
| 🟡 Próximo da meta | Preço acima da meta, mas dentro da margem configurada. |
| 🔴 Acima da meta | Preço superior à meta acrescida da margem. |
| ⚪ Preço não identificado ou ambíguo | Não foi possível determinar um único preço elegível. |
| 🔔 Filtro encontrado | Regra cadastrada sem meta de preço. |

As margens são escolhidas pela **meta do filtro**, não pelo preço encontrado:

| Faixa da meta | Margem inicial |
|---|---|
| Até R$ 300 | 20% |
| Acima de R$ 300 e até R$ 5.000 | 15% |
| Acima de R$ 5.000 | 10% |

Consulte com `/margem` ou altere as três faixas:

```text
/margem 20 15 10
```

Cada percentual deve ser um inteiro de 0 a 100. Uma meta de R$ 250 com margem de 20% considera preços até R$ 300 como próximos da meta.

### Escolher quais alertas receber

| Comando | Comportamento para regras com meta |
|---|---|
| `/modo todos` | Inclui dentro, próximos e acima da meta. |
| `/modo proximos` | Inclui dentro e próximos da meta. |
| `/modo meta` | Inclui apenas preços dentro da meta. |
| `/sem_preco ligado` | Permite alertas quando o preço não é identificado. |
| `/sem_preco desligado` | Suprime esses alertas. |

A opção de alertas sem preço é independente do modo. Regras sem meta continuam gerando alertas por correspondência de texto.

### Selecionar origens

| Comando | Ação |
|---|---|
| `/canais` | Lista canais e grupos acessíveis à conta, com números e IDs. |
| `/addcanal 3` | Inclui a origem de número 3 na seleção existente. |
| `/remcanal 3` | Retira essa origem do monitoramento. |
| `/addall` | Monitora todos os canais e grupos acessíveis, inclusive os futuros. |

Execute `/canais` antes de usar seus números; também é possível informar diretamente o ID.

**Uma seleção vazia significa monitorar todos**, não monitorar nenhum. Nesse estado, `/addcanal` informa que todas as origens já estão incluídas. Use `/remcanal` para excluir origens ou `/pausar` para interromper o monitoramento.

### Controlar o processo pelo Telegram

| Comando | Ação |
|---|---|
| `/pausar` | Pausa a análise de novas mensagens. |
| `/retomar` | Retoma a análise. |
| `/status` | Consulta conexões e configurações do monitor. |
| `/help` ou `/start` | Exibe a ajuda. |

## Hospedagem no Render

Faça primeiro o teste local. Depois, utilize uma cópia do repositório na sua conta GitHub e gere a sessão localmente antes da implantação.

### 1. Criar um Web Service

1. Acesse [dashboard.render.com](https://dashboard.render.com/) e entre na sua conta.
2. Clique em **New + → Web Service**. Se já estiver na tela **Create a new Service**, escolha diretamente o cartão **Web Services**.
3. Conecte sua conta GitHub quando solicitado e autorize o acesso ao repositório desejado.
4. Selecione a sua cópia de `telegram-monitor-promocoes`.

A imagem de referência desta etapa deve mostrar o cartão **Web Services**. O botão **New +** abre a seleção de serviços; ele não é a opção final a escolher.

### 2. Preencher a configuração

| Campo | Valor |
|---|---|
| Name | Um nome disponível, como `meu-monitor-promocoes`. |
| Language / Runtime | Python 3. |
| Branch | A branch que contém o código, normalmente `main`. |
| Region | Uma região adequada ao seu uso. |
| Root Directory | Deixe vazio se `bot.py` estiver na raiz. |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python bot.py` |
| Instance Type | Escolha após conferir preço e limitações do plano. |
| Health Check Path | `/health`, nas opções avançadas ou nas configurações do serviço. |

### 3. Adicionar as variáveis de ambiente

No formulário de criação, procure **Environment Variables**. Se o serviço já existir, abra **Environment → Edit → Add Environment Variable**.

Cadastre separadamente as seguintes chaves e os seus valores:

```text
API_ID
API_HASH
BOT_TOKEN
CHAT_ID
SESSION_STRING
MONGO_URI
OWNER_ID
```

Os valores são os mesmos do seu teste local. Não cole o nome da variável junto com o valor. Não envie seu arquivo `.env` para o GitHub.

O código utiliza a variável `PORT` fornecida pelo ambiente e usa `10000` como alternativa. Não é necessário duplicar uma variável que a plataforma já fornece.

### 4. Implantar e conferir

1. Pare a instância local com **Ctrl + C**, para não manter duas cópias em execução.
2. Conclua a criação em **Deploy Web Service / Create Web Service**. Ao alterar um serviço existente, escolha a opção de salvar com implantação.
3. Acompanhe **Logs**: a instalação precisa terminar e a aplicação deve registrar `Monitor conectado`.
4. Abra a URL pública do serviço acrescentando `/health`. A resposta esperada é `Servidor ativo`.
5. No Telegram, envie `/status` pela conta autorizada e confira as conexões e o estado do monitor.
6. Cadastre um filtro de demonstração e publique uma oferta fictícia em um grupo ao qual a conta leitora tenha acesso.

Uma resposta HTTP não comprova a saúde do Telegram ou do MongoDB; confira também `/status`.

### Configurar o UptimeRobot para monitorar o Render

Este tutorial considera o **UptimeRobot** ([uptimerobot.com](https://uptimerobot.com/)). O monitor HTTP verifica a URL pública do Render e pode manter um Web Service gratuito ativo ao enviar solicitações periódicas.

#### 1. Copiar e testar a URL de saúde no Render

1. Acesse [dashboard.render.com](https://dashboard.render.com/) e entre na sua conta.
2. Na página **Projects**, abra o projeto que contém o bot.
3. Em **Production**, clique no serviço Web Service do bot.
4. Na página do serviço, copie a URL pública exibida no cabeçalho, por exemplo, `https://meu-monitor.onrender.com`.
5. Acrescente `/health` ao final. A URL completa deve ficar parecida com `https://meu-monitor.onrender.com/health`.
6. Cole essa URL em uma nova aba do navegador. A resposta esperada é `Servidor ativo`.

Se o serviço gratuito estava dormindo, a primeira solicitação pode demorar enquanto o Render o inicia. Aguarde e atualize a página uma vez.

#### 2. Criar um monitor HTTP no UptimeRobot

1. Acesse [uptimerobot.com](https://uptimerobot.com/) e entre ou crie uma conta.
2. No painel principal (**Dashboard**), clique em **+ Add New Monitor**.
3. Em **Monitor Type**, selecione **HTTP(s)**.
4. No campo **URL**, cole o endereço completo terminado em `/health`.
5. Em **Friendly Name**, informe um nome fácil de reconhecer, por exemplo, `Telegram Promo Bot — Render`.
6. Em **Alert Contacts**, selecione seu e-mail ou outro contato de notificação. Confira se o contato recebe alertas de indisponibilidade (**Down**) e de recuperação (**Up**).
7. Revise o intervalo de verificação e as demais opções. No plano gratuito atual, as verificações são feitas a cada 5 minutos; a disponibilidade de opções pode variar conforme o plano.
8. Clique em **Create monitor**.

#### 3. Confirmar que o monitor está funcionando

1. Volte ao **Dashboard** do UptimeRobot.
2. Localize o monitor pelo nome que você escolheu.
3. Confirme que o status aparece como **Up**.
4. Se aparecer **Down**, abra o monitor para ver o incidente e teste novamente a URL `/health` no navegador. Confira também **Render → seu serviço → Logs**.

O endpoint `/health` verifica se o processo HTTP do bot está respondendo. Para confirmar as conexões com Telegram e MongoDB, consulte também o comando `/status` no Telegram.

#### O que isso faz no plano gratuito do Render

O Render suspende um Web Service gratuito após 15 minutos sem tráfego de entrada. O UptimeRobot, no plano gratuito, verifica o endereço a cada 5 minutos; essas requisições HTTP ao endpoint `/health` podem impedir que o serviço fique inativo. Isso pode ajudar o bot a permanecer acordado, mas não garante disponibilidade: falhas, pausas, limites de uso e mudanças nos planos dos provedores ainda podem interromper o serviço.

Um Web Service mantido ativo consome horas gratuitas do workspace. O Render oferece atualmente 750 horas de instância gratuita por workspace em cada mês; um serviço mantido ativo continuamente pode usar quase todas essas horas, deixando menos para outros serviços gratuitos do mesmo workspace. Confira os limites atuais antes de depender dessa configuração.

Para disponibilidade contínua com garantias mais adequadas, avalie um plano pago do Render. O UptimeRobot é uma ferramenta de monitoramento HTTP; ele não corrige falhas da aplicação, não verifica diretamente se Telegram/MongoDB estão conectados e não substitui o comando `/status`.

Consulte também os guias oficiais: [criar um monitor no UptimeRobot](https://help.uptimerobot.com/en/articles/11358364-how-to-create-your-first-monitor-on-uptimerobot-quick-setup-guide), [intervalo de verificação do UptimeRobot](https://help.uptimerobot.com/en/articles/11360876-what-is-a-monitoring-interval-in-uptimerobot) e [limites dos serviços gratuitos do Render](https://render.com/docs/free).

## Segurança e limitações

- A conta leitora precisa participar dos canais e grupos monitorados.
- O projeto acompanha novas mensagens; não oferece importação de histórico.
- O reconhecimento de preço usa regras de texto. Valores de parcelas, cupons e formatos diferentes podem exigir conferência manual.
- Mais de um preço elegível pode produzir um resultado ambíguo.
- O filtro compara palavras, não entende semanticamente o produto. Confira sempre a oferta original.
- O processamento envia no máximo um alerta por mensagem recebida, conforme a primeira regra aplicável.

## Solução de problemas

| Situação | O que conferir |
|---|---|
| Variável obrigatória ausente | Preenchimento do `.env` ou das variáveis da hospedagem. |
| Falha de conexão com o MongoDB | URI, credenciais, acesso de rede e disponibilidade do banco. |
| Comando sem resposta | Processo ativo, conversa privada e conta correspondente ao `OWNER_ID`. As respostas vão ao `CHAT_ID`. |
| Oferta não gera alerta | Participação na origem, seleção de canais, pausa, termos do filtro e modo de alertas. |
| Preço não identificado | Formato do preço; teste uma mensagem fictícia com um único valor, como `POR: R$ 249,90`. |
| Alertas duplicados | Outra instância do projeto executando com a mesma configuração. |

## Estrutura do repositório

```text
bot.py             Aplicação, comandos e processamento das mensagens
gerar_sessao.py     Autenticação local e geração da sessão Telegram
requirements.txt   Dependências Python
.env.example       Modelo de configuração sem credenciais
LICENSE            Licença do projeto
```

## Tecnologias Usadas

- Python
- Telethon
- Telegram Bot API
- MongoDB
- Google Antigravity
- GPT-6.1 Sol

## Autor

Victor Riki (https://github.com/victor-rk/)
