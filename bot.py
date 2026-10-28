# Monitor de Promoções no Telegram
# Monitora mensagens em canais e grupos e envia alertas com base em filtros
# de texto e metas de preço. O processamento é baseado em regras; não usa IA.
#
# Autor: Victor Riki (https://github.com/victor-rk)
# Repositório: https://github.com/victor-rk/telegram-monitor-promocoes

import asyncio
import html
import logging
import os
import re
import time
from decimal import Decimal, InvalidOperation
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

import aiohttp
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from telethon import TelegramClient, events, utils
from telethon.sessions import StringSession
from telethon.tl.types import Channel, Chat

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("monitor")

load_dotenv()

def required(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Variável obrigatória ausente: {name}")
    return value

API_ID = int(required("API_ID"))
API_HASH = required("API_HASH")
BOT_TOKEN = required("BOT_TOKEN")
CHAT_ID = required("CHAT_ID")
SESSION_STRING = required("SESSION_STRING")
MONGO_URI = required("MONGO_URI")
OWNER_ID = int(required("OWNER_ID"))
PORT = int(os.environ.get("PORT", "10000"))

db_client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=8000)
collection = db_client["telegram_bot"]["config"]
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
http_session = None
last_message = None
last_alert = None
confirm_until = 0.0
selection = {}
COMMAND_NAMES = {"add", "rem", "remall", "cancelar", "list", "export", "help", "start", "status", "pausar", "retomar", "canais", "addcanal", "remcanal", "addall", "modo", "sem_preco", "margem"}
DEFAULTS = {"keywords": [], "monitored_channels": [], "paused": False,
            "mode": "todos", "no_price": True,
            "margins": {"ate300": 20, "ate5000": 15, "acima5000": 10}}

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/health"):
            self.send_error(404)
            return
        body = b"Servidor ativo\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass

def server():
    try:
        ThreadingHTTPServer(("0.0.0.0", PORT), HealthHandler).serve_forever()
    except OSError:
        log.exception("Falha ao iniciar servidor HTTP")

async def get_config():
    await collection.update_one({"_id": "main_config"}, {"$setOnInsert": DEFAULTS}, upsert=True)
    config = await collection.find_one({"_id": "main_config"})
    for key, value in DEFAULTS.items():
        config.setdefault(key, value)
    return config

async def update(field, value):
    await collection.update_one({"_id": "main_config"}, {"$set": {field: value}}, upsert=True)

def esc(value):
    return html.escape(str(value), quote=False)

def chunks(text, limit=3500):
    # Split plain text before escaping so HTML entities are never cut.
    while text:
        if len(text) <= limit:
            yield text
            return
        cut = text.rfind("\n", 0, limit)
        if cut < limit // 3:
            cut = limit
        yield text[:cut]
        text = text[cut:].lstrip("\n")

async def send(text):
    global last_alert
    if http_session is None:
        log.error("Sessão HTTP indisponível")
        return False
    for part in chunks(text):
        payload = {"chat_id": CHAT_ID, "text": esc(part), "parse_mode": "HTML"}
        ok = False
        for attempt in range(3):
            try:
                async with http_session.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data=payload) as response:
                    result = await response.json(content_type=None)
                    if response.status == 200 and result.get("ok"):
                        ok = True
                        break
                    log.warning("Envio Telegram falhou: HTTP %s", response.status)
                    if response.status != 429 and response.status < 500:
                        break
                    delay = min(30, int(result.get("parameters", {}).get("retry_after", 2 ** attempt)))
            except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
                log.warning("Falha temporária no envio Telegram (tentativa %s)", attempt + 1)
                delay = 2 ** attempt
            if attempt < 2:
                await asyncio.sleep(delay)
        if not ok:
            return False
    last_alert = time.time()
    return True

def money(value):
    return "R$ " + f"{value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")

def parse_money(raw):
    raw = raw.strip()
    if not re.fullmatch(r"(?:\d{1,3}(?:\.\d{3})+|\d+)(?:,\d{1,2})?", raw):
        raise ValueError("preço inválido")
    try:
        value = Decimal(raw.replace(".", "").replace(",", "."))
    except InvalidOperation:
        raise ValueError("preço inválido")
    if value <= 0:
        raise ValueError("preço deve ser maior que zero")
    return value

def parse_rule(raw):
    raw = raw.strip()
    if not raw or "," in raw and not re.search(r"<\s*[\d.,]+$", raw):
        raise ValueError("termo vazio ou vírgula no termo")
    if "<" not in raw:
        return raw, None
    term, price = raw.rsplit("<", 1)
    if not term.strip() or "<" in term or "," in term:
        raise ValueError("termo inválido")
    return term.strip(), parse_money(price)

def normalize_rule(raw):
    term, price = parse_rule(raw)
    term = " ".join(term.split())
    return term if price is None else f"{term} < {str(price).replace('.', ',')}"

def rule_key(raw):
    try:
        term, value = parse_rule(raw)
        return (" ".join(term.casefold().split()), value)
    except ValueError:
        return (" ".join(raw.casefold().split()), None)

def split_rules(raw):
    return [x.strip() for x in re.split(r",\s*(?!\d)", raw) if x.strip()]

def extract_price(text):
    # Ignore explicit installments, shipping, discounts and cashback. Multiple
    # distinct eligible prices are ambiguous, so do not guess a product price.
    num = r"(?:\d{1,3}(?:\.\d{3})+|\d+)(?:,\d{1,2})?"
    candidates = []
    for m in re.finditer(rf"(?i)(?:r\$\s*|\b(?:por|apenas|preço|preco|valor)\s*:?\s*)({num})", text):
        before = text[max(0, m.start()-35):m.start()].lower()
        after = text[m.end():m.end()+35].lower()
        if re.search(r"(?:desconto|cashback|cupom|frete|parcelas?|\d+\s*x|\bem\s+at[eé])\s*[:\-]?\s*$", before):
            continue
        if re.match(r"\s*(?:off\b|de\s+(?:desconto|cashback|cupom)|/\s*m[eê]s|por\s+m[eê]s)", after):
            continue
        try:
            candidates.append(parse_money(m.group(1)))
        except ValueError:
            pass
    unique = set(candidates)
    return next(iter(unique)) if len(unique) == 1 else None

def label_rule(rule):
    try:
        term, price = parse_rule(rule)
        return f"{term} — {money(price) if price else 'sem meta'}"
    except ValueError:
        return rule + " — regra antiga; revise"

async def selected_dialogs():
    found = []
    async for dialog in client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, (Channel, Chat)) and not getattr(entity, "left", False):
            found.append((utils.get_peer_id(entity), dialog.name or "Sem nome"))
    return found

async def commands(event):
    global confirm_until, selection
    if not event.is_private or event.sender_id != OWNER_ID:
        return
    text = event.raw_text or ""
    parts = text.split(maxsplit=1)
    cmd = parts[0].split("@", 1)[0].lower()[1:]
    if cmd not in COMMAND_NAMES:
        return
    args = parts[1].strip() if len(parts) > 1 else ""
    try:
        config = await get_config()
        keys = config["keywords"]
        if cmd in ("start", "help"):
            await send("🤖 MONITOR DE PROMOÇÕES\n\n\"/add termo < preço, termo 2\" — adicionar filtros\n\"/list\" — listar filtros\n\"/rem número ou regra\" — remover\n\"/remall\" — remover todos com confirmação\n\"/export\" — copiar filtros\n\"/canais\" — listar canais e grupos\n\"/addcanal número ou ID\" — monitorar uma origem\n\"/remcanal número ou ID\" — retirar uma origem\n\"/addall\" — monitorar todos os canais e grupos atuais\n\"/pausar\" ou \"/retomar\" — controlar o monitor\n\"/modo todos|proximos|meta\" — escolher alertas\n\"/sem_preco ligado|desligado\" — alertas sem preço\n\"/margem até300 até5000 acima5000\" — percentuais\n\"/status\" — consultar situação\n\nEnvie os comandos na mesma conversa privada utilizada antes.")
        elif cmd == "add":
            if not args:
                return await send("Use: \"/add notebook < 3.000,50, mouse < 100\"")
            added, duplicates, invalid = [], [], []
            existing = {rule_key(k) for k in keys}
            for raw in split_rules(args):
                try:
                    item = normalize_rule(raw)
                    if rule_key(item) in existing:
                        duplicates.append(item)
                    else:
                        existing.add(rule_key(item))
                        added.append(item)
                except ValueError as exc:
                    invalid.append(f"{raw}: {exc}")
            if added:
                await collection.update_one({"_id": "main_config"}, {"$addToSet": {"keywords": {"$each": added}}})
            sections = []
            for title, items in (("✅ Adicionados", added), ("⚠️ Já cadastrados", duplicates), ("❌ Inválidos", invalid)):
                if items:
                    sections.append(title + ":\n" + "\n".join("• " + x for x in items))
            await send("\n\n".join(sections) or "Nenhum filtro válido.")
        elif cmd == "list":
            await send("📋 FILTROS ATIVOS\n\n" + ("\n".join(f"{i}. {label_rule(k)}" for i, k in enumerate(keys, 1)) if keys else "Nenhum filtro cadastrado."))
        elif cmd == "rem":
            target = keys[int(args)-1] if args.isdigit() and 1 <= int(args) <= len(keys) else next((k for k in keys if k == args), None)
            if target is None:
                return await send("Filtro não encontrado. Use \"/list\" e \"/rem número\", ou informe a regra exata.")
            await collection.update_one({"_id": "main_config"}, {"$pull": {"keywords": target}})
            await send("🗑️ Removido: " + label_rule(target))
        elif cmd == "remall":
            if args.lower() == "confirmar" and time.monotonic() < confirm_until:
                await update("keywords", [])
                confirm_until = 0
                await send("🗑️ Todos os filtros foram removidos.")
            elif args:
                await send("Confirmação inexistente ou expirada. Envie \"/remall\" novamente.")
            else:
                confirm_until = time.monotonic() + 120
                await send(f"⚠️ Remover {len(keys)} filtro(s)? Envie \"/remall confirmar\" em até 2 minutos ou \"/cancelar\".")
        elif cmd == "cancelar":
            confirm_until = 0
            await send("Operação cancelada.")
        elif cmd == "export":
            if not keys:
                return await send("Nenhum filtro cadastrado.")
            # Each message is a complete /add command, ready to copy and paste.
            batch = "/add "
            for key in keys:
                candidate = batch + (", " if batch != "/add " else "") + key
                if len(candidate) > 3000 and batch != "/add ":
                    await send(batch)
                    batch = "/add " + key
                else:
                    batch = candidate
            await send(batch)
        elif cmd == "status":
            try:
                await db_client.admin.command("ping")
                mongo = "conectado"
            except Exception:
                mongo = "indisponível"
            scope = "todos os canais e grupos" if not config["monitored_channels"] else str(len(config["monitored_channels"])) + " origem(ns) selecionada(s)"
            await send(f"🤖 STATUS\nTelegram: {'conectado' if client.is_connected() else 'desconectado'}\nMongoDB: {mongo}\nMonitoramento: {'pausado' if config['paused'] else 'ativo'}\nFiltros: {len(keys)}\nOrigens: {scope}\nModo: {config['mode']}\nSem preço: {'ligado' if config['no_price'] else 'desligado'}")
        elif cmd in ("pausar", "retomar"):
            await update("paused", cmd == "pausar")
            await send("⏸ Monitoramento pausado." if cmd == "pausar" else "▶️ Monitoramento retomado.")
        elif cmd == "canais":
            dialogs = await selected_dialogs()
            selection = {i: item for i, item in enumerate(dialogs, 1)}
            ids = set(config["monitored_channels"])
            rows = [f"{i}. {'✅' if not ids or peer_id in ids else '▫️'} {name} (ID {peer_id})" for i, (peer_id, name) in selection.items()]
            await send("📺 CANAIS E GRUPOS\n" + ("Lista vazia = todos monitorados.\n" if not ids else "✅ = monitorado.\n") + "\n".join(rows) + "\n\nUse \"/addcanal número\" ou \"/remcanal número\". \"/addall\" monitora todos.")
        elif cmd in ("addcanal", "remcanal"):
            if not args.lstrip("-").isdigit():
                return await send("Use \"/canais\" e informe o número ou ID: \"/addcanal 1\".")
            num = int(args)
            peer_id, name = selection.get(num, (num, str(num)))
            dialogs = await selected_dialogs()
            all_ids = {p for p, _ in dialogs}
            if peer_id not in all_ids:
                return await send("Origem não encontrada entre os canais e grupos da conta. Use \"/canais\" novamente.")
            ids = set(config["monitored_channels"])
            if cmd == "remcanal" and not ids:
                ids = all_ids
            if cmd == "addcanal":
                if not ids:
                    return await send("Todas as origens já estão sendo monitoradas. Use \"/remcanal\" para excluir alguma.")
                ids.add(peer_id)
            else:
                ids.discard(peer_id)
                if not ids:
                    return await send("Não é possível deixar a seleção vazia: ela significa monitorar todos. Use \"/pausar\" para parar.")
            await update("monitored_channels", sorted(ids))
            await send(f"{'✅ Adicionado' if cmd == 'addcanal' else '🗑️ Removido'}: {name}")
        elif cmd == "addall":
            await update("monitored_channels", [])
            await send("✅ Monitorando todos os canais e grupos atuais e futuros em que a conta estiver.")
        elif cmd == "modo":
            if args not in ("todos", "proximos", "meta"):
                return await send("Use \"/modo todos\", \"/modo proximos\" ou \"/modo meta\".")
            await update("mode", args)
            await send("✅ Modo de alertas: " + args)
        elif cmd == "sem_preco":
            if args not in ("ligado", "desligado"):
                return await send("Use \"/sem_preco ligado\" ou \"/sem_preco desligado\".")
            await update("no_price", args == "ligado")
            await send("✅ Alertas sem preço: " + args)
        elif cmd == "margem":
            vals = args.split()
            try:
                nums = [int(x) for x in vals]
                if len(nums) != 3 or any(x < 0 or x > 100 for x in nums):
                    raise ValueError
            except ValueError:
                margins = config["margins"]
                return await send(f"Margens atuais: até R$ 300: {margins['ate300']}%; até R$ 5.000: {margins['ate5000']}%; acima: {margins['acima5000']}%.\nUse: \"/margem 20 15 10\" (percentuais de 0 a 100).")
            await update("margins", dict(zip(("ate300", "ate5000", "acima5000"), nums)))
            await send(f"✅ Margens atualizadas: {nums[0]}%, {nums[1]}% e {nums[2]}%.")
    except Exception:
        log.exception("Erro ao processar comando %s", cmd)
        await send("❌ Não foi possível concluir o comando. Verifique os logs do Render e a conexão com o MongoDB.")

@client.on(events.NewMessage)
async def handle(event):
    global last_message
    text = event.raw_text or ""
    if event.is_private and text.startswith("/"):
        await commands(event)
        return
    # Only channels and groups; never search personal conversations.
    if not (event.is_channel or event.is_group) or not text:
        return
    if event.sender_id == int(BOT_TOKEN.split(":", 1)[0]):
        return
    try:
        config = await get_config()
        if config["paused"]:
            return
        allowed = config["monitored_channels"]
        if allowed and event.chat_id not in allowed:
            return
        last_message = time.time()
        for raw in config["keywords"]:
            try:
                term, limit = parse_rule(raw)
            except ValueError:
                term, limit = raw, None
            if not term or not all(word in text.casefold() for word in term.casefold().split()):
                continue
            price = extract_price(text) if limit else None
            if limit:
                if price is None:
                    category = "unknown"
                    heading = "⚪ PREÇO NÃO IDENTIFICADO OU AMBÍGUO"
                elif price <= limit:
                    category, heading = "meta", "🟢 DENTRO DA META"
                else:
                    margins = config["margins"]
                    margin = margins["ate300" if limit <= 300 else "ate5000" if limit <= 5000 else "acima5000"]
                    category = "proximos" if price <= limit * (1 + Decimal(str(margin))/100) else "caro"
                    heading = "🟡 PRÓXIMO DA META" if category == "proximos" else "🔴 ACIMA DA META"
                if category == "unknown" and not config["no_price"]:
                    continue
                if category == "caro" and config["mode"] != "todos":
                    continue
                if category == "proximos" and config["mode"] == "meta":
                    continue
            else:
                heading = "🔔 FILTRO ENCONTRADO"
            info = f"{heading}\n\nFiltro: {term}\n"
            if limit:
                info += f"Preço identificado: {money(price) if price is not None else 'não identificado'}\nMeta: {money(limit)}\n"
            try:
                chat = await event.get_chat()
                origin = getattr(chat, "title", None) or "Canal/Grupo"
            except Exception:
                origin = "Canal/Grupo"
            await send(info + "\n📝 Mensagem original:\n" + text + "\n\nOrigem: " + origin)
            break
    except Exception:
        log.exception("Falha ao processar mensagem")

async def main():
    global http_session
    Thread(target=server, daemon=True).start()
    try:
        await db_client.admin.command("ping")
        await get_config()
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20)) as session:
            http_session = session
            await client.start()
            log.info("Monitor conectado")
            await client.run_until_disconnected()
    finally:
        http_session = None
        db_client.close()

if __name__ == "__main__":
    asyncio.run(main())
