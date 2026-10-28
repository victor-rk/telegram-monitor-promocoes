from getpass import getpass

from telethon.sync import TelegramClient
from telethon.sessions import StringSession


def main():
    print("Gerador de sessão do Telegram")
    print("Use o API ID e o API Hash da sua própria aplicação.")
    print()

    api_id_text = input("API ID: ").strip()
    api_hash = getpass("API Hash: ").strip()

    if not api_id_text.isdigit() or not api_hash:
        print("API ID ou API Hash inválido.")
        return

    with TelegramClient(
        StringSession(),
        int(api_id_text),
        api_hash,
    ) as client:
        session_string = client.session.save()

    print("\nSua SESSION_STRING:")
    print(session_string)
    print("\nGuarde essa string em local seguro e não a compartilhe.")


if __name__ == "__main__":
    main()
