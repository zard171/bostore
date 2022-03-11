from typing import Union

from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from database import cur, save
from utils import create_mention, get_info_wallet


@Client.on_message(filters.command(["start", "menu"]))
@Client.on_callback_query(filters.regex("^start$"))
async def start(c: Client, m: Union[Message, CallbackQuery]):
    user_id = m.from_user.id

    rt = cur.execute(
        "SELECT id, balance, balance_diamonds, refer FROM users WHERE id=?", [user_id]
    ).fetchone()

    if isinstance(m, Message):
        """refer = (
            int(m.command[1])
            if (len(m.command) == 2)
            and (m.command[1]).isdigit()
            and int(m.command[1]) != user_id
            else None
        )

        if rt[3] is None:
            if refer is not None:
                mention = create_mention(m.from_user, with_id=False)

                cur.execute("UPDATE users SET refer = ? WHERE id = ?", [refer, user_id])
                try:
                    await c.send_message(
                        refer,
                        text=f"<b>O usuário {mention} se tornou seu referenciado.</b>",
                    )
                except BadRequest:
                    pass"""

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("💳 Comprar", callback_data="comprar_cc"),
            ],
            [
                InlineKeyboardButton("💸 Add saldo", callback_data="add_saldo"),
                InlineKeyboardButton("👤 Suas informações", callback_data="user_info"),
            ],
        ]
    )

    bot_logo, news_channel, support_user = cur.execute(
        "SELECT main_img, channel_user, support_user FROM bot_config WHERE ROWID = 0"
    ).fetchone()

    start_message = f"""OLÁ {m.from_user.first_name},
______________________________________
Seja bem vindo ao C$ BRUXO STORE bot!
______________________________________
✅ Checkadas na hora pelo bot!
👤 Todas com nome e CPF!
💰 Faça recargas rapidamente pelo /pix!
💳 CC's virgens diretamente do painel!
______________________________________
ℹ️ Grupo ref:
 @Bruxorefs
ℹ️ Grupo:
@Bruxo7Ccs
______________________________________
ANTES DECOMPRAR LEIA TUDO!
COMPRE SE ESTIVER DE ACORDO COM MEUS TERMOS DE USO. 
_____________________________________
⚠️NÃO GARANTO SALDO NA INFO 
⚠️NÃO GARANTO APROVAÇÃO 
⚠️NÃO GARANTO QUE A INFO SERÁ VINCULADA EM APLICATIVOS 
⚠️O BOT MANDA APENAS LIVE.
⚠️LEMBRANDO QUE, APÓS O PAGAMENTO SEU SALDO SERÁ CREDITADO E VC CONSEGUE CONFERIR LÁ NA OPÇÃO SEU PERFIL.
_____________________________________
{get_info_wallet(user_id)}
_____________________________________
💬 Dúvidas?
https://t.me/BruXodu7"""

    if isinstance(m, CallbackQuery):
        send = m.edit_message_text
    else:
        send = m.reply_text
    save()
    await send(start_message, reply_markup=kb)
