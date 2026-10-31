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

---

# Instalação e configuração

## 1. Prepare os requisitos

Você precisará de:

- Python com suporte às dependências de `requirements.txt`.
- Git instalado.
- Uma conta no GitHub.
- Uma conta Telegram que participe dos canais ou grupos desejados.
- Uma aplicação Telegram, criada em [my.telegram.org](https://my.telegram.org), para obter `API_ID` e `API_HASH`.
- Um bot criado pelo [@BotFather](https://t.me/BotFather), para obter `BOT_TOKEN`.
- Uma instância MongoDB acessível pela aplicação.
- O ID numérico da sua conta e o ID do chat que receberá os alertas.
- Contas no [Render](https://render.com/) e no [UptimeRobot](https://uptimerobot.com/).

## 2. Baixe o projeto e instale as dependências

Primeiro, clone o repositório original e entre na pasta do projeto:

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

## 3. Crie seu próprio repositório no GitHub

Antes de conectar o projeto ao Render, você precisa ter uma cópia do código na sua própria conta do GitHub.

### 3.1. Criar um novo repositório

1. Acesse [github.com](https://github.com/) e entre na sua conta.
2. Clique no botão **+**, no canto superior direito.
3. Selecione **New repository**.
4. Em **Repository name**, escolha um nome para o seu projeto, por exemplo, `telegram-monitor-promocoes`.
5. Escolha a visibilidade **Private** ou **Public**, conforme sua preferência.
6. Clique em **Create repository**.

O GitHub exibirá uma página com instruções para conectar um repositório local. Mantenha essa página aberta.

### 3.2. Conectar seu projeto ao novo repositório

Volte ao terminal, dentro da pasta `telegram-monitor-promocoes`.

Primeiro, confira o endereço remoto atual:

```bash
git remote -v
```

O resultado deverá mostrar o repositório original:

```text
origin  https://github.com/victor-rk/telegram-monitor-promocoes.git
```

Agora, altere o endereço remoto para o seu próprio repositório:

```bash
git remote set-url origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
```

Substitua `SEU_USUARIO` e `SEU_REPOSITORIO` pelos dados da sua conta e do repositório criado.

Confira se a alteração foi realizada:

```bash
git remote -v
```

O endereço exibido agora deverá ser o do seu repositório.

### 3.3. Enviar o projeto para o GitHub

Antes de enviar, confira se o Git está reconhecendo os arquivos:

```bash
git status
```

Caso existam alterações pendentes que você deseja incluir, adicione-as:

```bash
git add .
```

Crie um commit:

```bash
git commit -m "Configura projeto para hospedagem"
```

Por fim, envie o código para o GitHub:

```bash
git branch -M main
git push -u origin main
```

O comando `git push` envia os commits locais para o repositório remoto. A opção `-u` configura o acompanhamento da branch `main`, facilitando os próximos envios.

**Importante:** se o comando `git commit` informar que não há alterações para registrar, você pode prosseguir diretamente para o `git push`.

### 3.4. Conferir o repositório

1. Atualize a página do seu novo repositório no GitHub.
2. Confira se os arquivos e pastas do projeto aparecem.
3. Abra o `README.md` e verifique se a documentação foi enviada corretamente.
4. Confira se o arquivo `.env` não foi publicado.
5. Verifique se nenhum arquivo contendo credenciais ou sessões foi enviado.

O arquivo `.env` contém credenciais e não deve ser enviado ao GitHub. Utilize o `.env.example` como modelo e mantenha as informações reais apenas no ambiente local ou nas variáveis de ambiente da hospedagem.

A partir daqui, o Render deverá utilizar esse repositório próprio.

### 3.5. Atualizar o repositório futuramente

Sempre que fizer alterações no projeto, utilize:

```bash
git add .
git commit -m "Descrição das alterações"
git push
```

Substitua `Descrição das alterações` por uma mensagem curta que explique o que foi modificado.

O Render poderá ser configurado para realizar uma nova implantação automaticamente sempre que houver um novo envio para a branch conectada.

---

## 4. Obtenha as credenciais

### Criar o bot e obter o BOT_TOKEN

1. Abra o Telegram e acesse o [BotFather oficial](https://t.me/BotFather).
2. Envie `/newbot`.
3. Escolha o nome exibido, por exemplo, **Meu Monitor de Ofertas**.
4. Escolha um username disponível terminado em `bot`, por exemplo, `meu_monitor_ofertas_bot`.
5. O BotFather retornará um token. Guarde-o como `BOT_TOKEN`.
6. Abra o link do bot criado e pressione **Iniciar / Start**.

Você não precisa adicionar esse bot aos canais de ofertas: quem lê as mensagens é a conta autenticada no Telethon.

### Obter API_ID e API_HASH

1. Acesse [my.telegram.org](https://my.telegram.org).
2. Entre com o número da conta que participará dos canais e confirme o código recebido pelo Telegram.
3. Abra **API development tools**.
4. Se ainda não houver uma aplicação, preencha os dados solicitados e crie uma aplicação para uso próprio.
5. Copie **App api_id** para `API_ID` e **App api_hash** para `API_HASH`.

Essas credenciais pertencem à aplicação Telegram; são diferentes do token entregue pelo BotFather.

### Descobrir OWNER_ID e CHAT_ID

Para receber alertas na sua conversa privada com o bot:

1. Usando a mesma conta que será autenticada no Telethon, abra o bot criado e envie uma mensagem, como `Olá`.
2. Consulte o método oficial `getUpdates` no navegador, substituindo o marcador pelo seu token:

```text
https://api.telegram.org/botSEU_BOT_TOKEN/getUpdates
```

3. Na resposta, localize a mensagem que você acabou de enviar.
4. Copie o valor de `"message":{"from":{"id":...}}` para `OWNER_ID`.
5. Copie o valor de `"message":{"chat":{"id":...}}` para `CHAT_ID`. Em uma conversa privada comum com sua própria conta, esses dois valores coincidem.

Use somente o número, sem aspas, parênteses ou `Long`. Se `result` estiver vazio, envie uma nova mensagem ao bot e atualize a consulta. Um webhook previamente configurado nesse mesmo bot pode impedir a consulta; prefira um bot novo para este projeto.

**O token aparece no endereço da consulta. Não compartilhe esse endereço nem tire prints da barra do navegador.** Feche a página após copiar os IDs.

### Criar o banco no MongoDB Atlas

1. Acesse [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register), crie sua conta e um projeto.
2. Crie um cluster/deployment escolhendo região e modalidade adequadas ao seu uso. Confira os custos antes de confirmar.
3. Em **Database Access / Database Users**, crie um usuário de banco com senha própria e permissão de leitura e escrita no banco `telegram_bot`. Esse usuário não é o login da sua conta Atlas.
4. Em **Network Access / IP Access List**, configure o acesso de rede para permitir que o serviço no Render alcance o banco.
5. Consulte os endereços de saída do seu serviço no Render e adicione os intervalos correspondentes à lista de acesso do Atlas. Se também for executar a aplicação localmente, autorize o IP público da sua conexão local.
6. Abra o cluster e clique em **Connect → Drivers**. Escolha **Python** e copie a connection string.
7. Na URL copiada, substitua `<username>` pelo usuário criado em Database Access e `<password>` pela senha definida para ele. Guarde a URL completa para utilizar como `MONGO_URI`. Se a senha tiver caracteres especiais, codifique-os para URL.

A aplicação cria a configuração na coleção `telegram_bot.config` ao iniciar; não é necessário inserir um documento manualmente.

**Importante:** não libere acesso de qualquer IP apenas para contornar uma falha de conexão. Autorize somente os endereços necessários.

Os nomes dos menus podem variar. Consulte o [guia oficial de conexão do Atlas](https://www.mongodb.com/docs/atlas/connect-to-database-deployment/) se a interface for diferente.

## 5. Gere a sessão da conta leitora

A sessão da conta Telegram deve ser gerada localmente, antes da implantação no Render.

No terminal, dentro da pasta do projeto e com o ambiente virtual ativado, execute:

```bash
python gerar_sessao.py
```

Informe o API ID, o API Hash e os dados solicitados pelo Telegram para autenticar sua própria conta. Copie a sessão gerada para `SESSION_STRING`.

**Atenção: a sessão é uma credencial de acesso à sua conta Telegram.** Não a envie a terceiros, não a mostre em gravações e não a publique no repositório.

### Cuidados com a sessão

A mesma `SESSION_STRING` não deve ser utilizada simultaneamente por diferentes processos ou instâncias do Telethon.

Para esta implantação:

- Gere a sessão localmente.
- Utilize essa sessão exclusivamente no serviço do Render.
- Não mantenha `python bot.py` em execução no computador enquanto o Render estiver utilizando a mesma sessão.
- Não configure a mesma sessão em outro serviço ou instância do bot.
- Mantenha apenas uma execução ativa do monitor.

Se precisar substituir a sessão, interrompa primeiro a execução no Render e todas as execuções locais. Gere uma nova sessão e atualize a variável no Render. Depois salve a alteração e aplique a implantação antes de retomar o serviço.

O uso simultâneo da mesma sessão a partir de diferentes endereços IP pode invalidar a chave de autenticação e provocar o erro `AuthKeyDuplicatedError`.

## 6. Configure as variáveis de ambiente

Crie uma cópia de `.env.example` chamada `.env` na raiz do projeto e preencha as variáveis:

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

Para uso individual, use sua própria conta em `OWNER_ID` e seu chat privado com o bot como destino em `CHAT_ID`. Inicie a conversa com o bot antes de implantar a aplicação.

O banco utilizado pelo código é `telegram_bot`, com a coleção `config`. Alterar apenas o nome do banco no caminho da URI não muda essa seleção definida no código.

**Importante:** o arquivo `.env` é utilizado para organizar suas credenciais localmente. Na hospedagem, os valores também deverão ser cadastrados diretamente nas variáveis de ambiente do Render. Nunca envie o arquivo `.env` para o GitHub.

---

# Hospedagem no Render

Com o repositório próprio publicado no GitHub, as credenciais preparadas e a sessão gerada, você já pode implantar o projeto.

O `bot.py` será iniciado pelo próprio Render; não é necessário executá-lo localmente.

## 1. Criar um Web Service

1. Acesse [dashboard.render.com](https://dashboard.render.com/) e entre na sua conta.
2. Clique em **New + → Web Service**.
3. Conecte sua conta GitHub quando solicitado e autorize o acesso ao repositório desejado.
4. Selecione o repositório que você criou anteriormente.

**Atenção:** selecione seu repositório, não o repositório original `victor-rk/telegram-monitor-promocoes`.

## 2. Preencher a configuração

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
| Health Check Path | `/health` |

## 3. Adicionar as variáveis de ambiente

No formulário de criação, procure **Environment Variables**. Se o serviço já existir, abra **Environment → Edit → Add Environment Variable**.

Cadastre separadamente as seguintes chaves e seus respectivos valores:

```text
API_ID
API_HASH
BOT_TOKEN
CHAT_ID
SESSION_STRING
MONGO_URI
OWNER_ID
```

Os valores são os mesmos que você preparou na configuração local. Não cole o nome da variável junto com o valor. Não envie seu arquivo `.env` para o GitHub.

O código utiliza a variável `PORT` fornecida pelo ambiente e usa `10000` como alternativa. Não é necessário duplicar uma variável que a plataforma já fornece.

## 4. Implantar e conferir

1. Confira se todas as variáveis de ambiente foram cadastradas corretamente.
2. Conclua a criação em **Deploy Web Service / Create Web Service**.
3. Ao alterar variáveis de um serviço existente, salve a alteração e aplique a implantação para que o novo processo utilize os valores atualizados.
4. Acompanhe **Logs**: a instalação precisa terminar e a aplicação deve registrar `Monitor conectado`.
5. Abra a URL pública do serviço acrescentando `/health`. A resposta esperada é `Servidor ativo`.
6. No Telegram, envie `/status` pela conta autorizada e confira as conexões e o estado do monitor.

Uma resposta HTTP não comprova a saúde do Telegram ou do MongoDB; confira também `/status`.

**Não é necessário manter o terminal local executando `bot.py`.** Depois da implantação, o Render será responsável por iniciar e manter o processo de acordo com as condições do serviço contratado.

### Atenção à quantidade de instâncias

Este projeto utiliza uma sessão Telethon destinada a uma única execução. Não configure várias instâncias simultâneas do bot utilizando a mesma `SESSION_STRING`.

Também não execute o mesmo bot localmente enquanto ele estiver ativo no Render.

---

# Configurar o UptimeRobot para monitorar o Render

Este tutorial considera o **UptimeRobot** ([uptimerobot.com](https://uptimerobot.com/)). O monitor HTTP verifica a URL pública do Render e permite acompanhar a disponibilidade do endpoint de saúde.

## 1. Copiar e testar a URL de saúde no Render

1. Acesse [dashboard.render.com](https://dashboard.render.com/) e entre na sua conta.
2. Abra o projeto que contém o bot.
3. Abra o serviço Web Service do bot.
4. Copie a URL pública exibida no cabeçalho, por exemplo, `https://meu-monitor.onrender.com`.
5. Acrescente `/health` ao final. A URL completa deverá ficar parecida com `https://meu-monitor.onrender.com/health`.
6. Cole essa URL em uma nova aba do navegador.

A resposta esperada é:

```text
Servidor ativo
```

Se o serviço gratuito estava suspenso por inatividade, a primeira solicitação pode demorar enquanto o Render o inicia. Aguarde e atualize a página uma vez.

## 2. Conferir o endpoint HTTP

O endpoint `/health` precisa responder corretamente tanto a requisições `GET` quanto `HEAD`.

- `GET` retorna o texto `Servidor ativo`.
- `HEAD` retorna os mesmos cabeçalhos HTTP, sem o corpo da resposta.

Essa compatibilidade é importante porque ferramentas de monitoramento podem utilizar `HEAD` para verificar a disponibilidade do endereço.

Durante a configuração deste projeto, o UptimeRobot identificou um erro **HTTP 501 Not Implemented** na região da América do Norte. O problema foi resolvido após a implementação do suporte a `HEAD` no servidor HTTP.

Se estiver implementando essa funcionalidade em outro ambiente, o handler deverá tratar os dois métodos:

```python
class HealthHandler(BaseHTTPRequestHandler):

    def _send_health(self, send_body=True):
        if self.path not in ("/", "/health"):
            self.send_error(404)
            return

        body = b"Servidor ativo\n"

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        if send_body:
            self.wfile.write(body)

    def do_GET(self):
        self._send_health(send_body=True)

    def do_HEAD(self):
        self._send_health(send_body=False)

    def log_message(self, format, *args):
        pass
```

Esse trecho representa a implementação utilizada no projeto. Não é necessário adicioná-lo novamente se o `bot.py` já contiver essa versão.

## 3. Criar um monitor HTTP no UptimeRobot

1. Acesse [uptimerobot.com](https://uptimerobot.com/) e entre ou crie uma conta.
2. No painel principal (**Dashboard**), clique em **+ Add New Monitor**.
3. Em **Monitor Type**, selecione **HTTP(s)**.
4. No campo **URL**, cole o endereço completo terminado em `/health`.
5. Em **Friendly Name**, informe um nome fácil de reconhecer, por exemplo, `Telegram Promo Bot — Render`.
6. Em **Alert Contacts**, selecione seu e-mail ou outro contato de notificação.
7. Revise o intervalo de verificação e as demais opções disponíveis no seu plano.
8. Clique em **Create monitor**.

## 4. Confirmar que o monitor está funcionando

1. Volte ao **Dashboard** do UptimeRobot.
2. Localize o monitor pelo nome escolhido.
3. Confirme que o status aparece como **Up**.
4. Se aparecer **Down**, abra o monitor e confira o código HTTP do incidente.
5. Teste novamente a URL `/health` no navegador.
6. Confira também **Render → seu serviço → Logs**.

Os principais estados são:

| Estado | Significado |
|---|---|
| Up | O monitor conseguiu verificar o endereço. |
| Down | O monitor identificou uma falha de disponibilidade. |
| Resolved | Um incidente anterior foi encerrado após a recuperação. |

O endpoint `/health` verifica se o servidor HTTP do processo está respondendo. Ele não comprova, sozinho, que Telegram e MongoDB continuam conectados. Para isso, consulte também `/status` no Telegram e os logs do Render.

## 5. Entender o funcionamento no plano gratuito do Render

O Render suspende Web Services gratuitos após períodos de inatividade. Requisições periódicas ao endpoint `/health` podem ajudar a manter o serviço ativo, mas isso não representa uma garantia de disponibilidade nem substitui um plano adequado à execução contínua.

Um serviço mantido ativo consome horas gratuitas do workspace. O Render oferece uma quantidade limitada de horas gratuitas por mês; um serviço ativo continuamente pode consumir quase todo esse limite, deixando menos horas disponíveis para outros serviços gratuitos.

Confira os limites e condições atuais antes de depender dessa configuração:

- [Documentação oficial do Render — Free](https://render.com/docs/free)
- [Guia oficial do UptimeRobot](https://help.uptimerobot.com/)

O UptimeRobot é uma ferramenta de monitoramento HTTP. Ele não corrige falhas da aplicação, não verifica diretamente as conexões do Telegram ou MongoDB e não substitui o comando `/status`.

---

# Utilização

## Cadastrar e consultar filtros

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

## Entender as classificações

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

## Escolher quais alertas receber

| Comando | Comportamento para regras com meta |
|---|---|
| `/modo todos` | Inclui dentro, próximos e acima da meta. |
| `/modo proximos` | Inclui dentro e próximos da meta. |
| `/modo meta` | Inclui apenas preços dentro da meta. |
| `/sem_preco ligado` | Permite alertas quando o preço não é identificado. |
| `/sem_preco desligado` | Suprime esses alertas. |

A opção de alertas sem preço é independente do modo. Regras sem meta continuam gerando alertas por correspondência de texto.

## Selecionar origens

| Comando | Ação |
|---|---|
| `/canais` | Lista canais e grupos acessíveis à conta, com números e IDs. |
| `/addcanal 3` | Inclui a origem de número 3 na seleção existente. |
| `/remcanal 3` | Retira essa origem do monitoramento. |
| `/addall` | Monitora todos os canais e grupos acessíveis, inclusive os futuros. |

Execute `/canais` antes de usar seus números; também é possível informar diretamente o ID.

**Uma seleção vazia significa monitorar todos**, não monitorar nenhum. Nesse estado, `/addcanal` informa que todas as origens já estão incluídas. Use `/remcanal` para excluir origens ou `/pausar` para interromper o monitoramento.

## Controlar o processo pelo Telegram

| Comando | Ação |
|---|---|
| `/pausar` | Pausa a análise de novas mensagens. |
| `/retomar` | Retoma a análise. |
| `/status` | Consulta conexões e configurações do monitor. |
| `/help` ou `/start` | Exibe a ajuda. |

---

# Segurança e limitações

- A conta leitora precisa participar dos canais e grupos monitorados.
- O projeto acompanha novas mensagens; não oferece importação de histórico.
- O reconhecimento de preço usa regras de texto. Valores de parcelas, cupons e formatos diferentes podem exigir conferência manual.
- Mais de um preço elegível pode produzir um resultado ambíguo.
- O filtro compara palavras, não entende semanticamente o produto. Confira sempre a oferta original.
- O processamento envia no máximo um alerta por mensagem recebida, conforme a primeira regra aplicável.
- A `SESSION_STRING` permite acesso à conta Telegram autenticada e deve ser tratada como uma credencial privada.
- Não execute simultaneamente várias instâncias utilizando a mesma sessão Telethon.

# Solução de problemas

| Situação | O que conferir |
|---|---|
| Variável obrigatória ausente | Preenchimento do `.env` ou das variáveis da hospedagem. |
| Falha de conexão com o MongoDB | URI, credenciais, acesso de rede no Atlas e disponibilidade do banco. |
| Erro TLS ao conectar ao MongoDB | Verifique a lista de IPs autorizados no Atlas e os endereços de saída do Render. |
| Comando sem resposta | Processo ativo, conversa privada e conta correspondente ao `OWNER_ID`. As respostas vão ao `CHAT_ID`. |
| Oferta não gera alerta | Participação na origem, seleção de canais, pausa, termos do filtro e modo de alertas. |
| Preço não identificado | Formato do preço; teste uma mensagem fictícia com um único valor, como `POR: R$ 249,90`. |
| Alertas duplicados | Verifique se existe outra instância do projeto executando com a mesma configuração. |
| `AuthKeyDuplicatedError` | A mesma sessão Telethon pode estar sendo usada simultaneamente por processos ou endereços IP diferentes. Interrompa todas as execuções, gere uma nova sessão localmente e configure-a exclusivamente em uma única instância do Render. |
| UptimeRobot retorna HTTP 501 | Confira se o servidor HTTP implementa os métodos `GET` e `HEAD` no endpoint `/health`. |
| UptimeRobot retorna HTTP 502 | Confira se o processo do bot continua ativo nos logs do Render. Um erro que encerra `bot.py` também derruba o servidor HTTP. |
| UptimeRobot marca o serviço como Down | Teste `/health` no navegador e confira o código HTTP e os logs do Render. |
| Erro ao executar `git push` | Confira o endereço remoto com `git remote -v`, a autenticação do GitHub e as permissões da conta. |
| GitHub rejeita o envio por privacidade do e-mail | Configure o e-mail `noreply` disponibilizado pelo GitHub nas configurações do Git e atualize o e-mail do autor do commit, se necessário. |

## Recuperação da sessão Telethon

Se aparecer:

```text
AuthKeyDuplicatedError
```

Siga esta sequência:

1. Suspenda temporariamente o serviço do Render.
2. Encerre todas as execuções locais de `bot.py`.
3. Confira se não existe outro serviço ou instância utilizando a mesma sessão.
4. Execute localmente apenas:

```bash
python gerar_sessao.py
```

5. Atualize o valor de `SESSION_STRING` no Render, sem compartilhar ou publicar o conteúdo.
6. Salve a variável e aplique a implantação.
7. Retome o serviço somente depois de confirmar que não existe outra execução utilizando a nova sessão.
8. Confira os logs até aparecer `Monitor conectado` sem novos erros.

Não é necessário alterar o código ou gerar sessões repetidamente sem antes verificar se existe outra execução utilizando a mesma credencial.

---

# Estrutura do repositório

```text
bot.py             Aplicação, comandos e processamento das mensagens
gerar_sessao.py     Autenticação local e geração da sessão Telegram
requirements.txt   Dependências Python
.env.example       Modelo de configuração sem credenciais
LICENSE            Licença do projeto
README.md          Documentação do projeto
```

# Tecnologias Utilizadas

- Python
- Telethon
- Telegram Bot API
- MongoDB
- Render
- UptimeRobot

# Autor

Victor Riki — [github.com/victor-rk](https://github.com/victor-rk/)
