import re
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher.filters import ChatTypeFilter

from keyboards.inline.car_check_inline import admin_review_photo
from loader import dp
from utils.api.service import MachineCheckService, FaceCheckService


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.CHANNEL), lambda c: c.data.startswith('admin'))
async def check_car_team(call: types.CallbackQuery):
    data = call.data.split("_")[1]
    user_id = re.search(r'User ID: (\d+)', call.message.text).group(1)
    check_type = call.message.text.split("Tekshiruv: ")[1]
    if data == "yes":
        profile_link = f'tg://user?id={call.from_user.id}'
        text = f'{call.message.text}\n\n<b>Status: Approved✅\n\nSupport:</b><a href="{profile_link}">{call.from_user.full_name}</a>'
        text_to_user = f'{call.message.text}\n\n<b>Status: Approved✅</b>'
        await call.message.edit_text(text)
        await call.message.bot.send_message(chat_id=user_id, text=text_to_user)
        if check_type == '🚕 Moshina Tekshiruvi':
            MachineCheckService.update(telegram_id=user_id, status="approved")
        else:
            FaceCheckService.update(telegram_id=user_id, status="approved")
    else:
        text = "Rasmlarni rad etdingiz.Iltimos,rad etish sababini tanlang"
        await call.message.edit_text(text=text, reply_markup=admin_review_photo(user_id=user_id, check_type=check_type))


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.CHANNEL), lambda c: c.data.startswith('Rasmlar'))
async def check_car_team(call: types.CallbackQuery):
    data = call.data.split("_")
    if data[1] == "other":
        await call.message.edit_text(
            f"<b>User ID: <code>{data[-1]}</code>\nTekshiruv: {data[-2]}\n\nStatus: Rejected❌\n\n❗️Shart:</b>Rad Etish sababini "
            f"shu habarga reply qilib yozing!")
    else:
        user_id = data[-1]
        check_type = data[-2]
        reason = f"{data[0]} {data[1]} {data[2]}"
        profile_link = f'tg://user?id={call.from_user.id}'
        text = f'User ID: <code>{user_id}</code>\nTekshiruv: {check_type}\n\n<b>Status: Rejected❌\nSababi:{reason}\n\nSupport:</b><a href="{profile_link}">{call.from_user.full_name}</a>'
        await call.message.edit_text(text=text)
        text = f'User ID: <code>{user_id}</code>\nTekshiruv: {check_type}\n\n<b>Status: Rejected❌\nSababi:{reason}</b>'
        await call.message.bot.send_message(chat_id=user_id, text=text)
        if check_type == '🚕 Moshina Tekshiruvi':
            MachineCheckService.update(telegram_id=user_id, status="rejected", rejection_reason=reason)
        else:
            FaceCheckService.update(telegram_id=user_id, status="rejected", rejection_reason=reason)


@dp.channel_post_handler()
async def all_post(message: types.Message):
    if message.reply_to_message:
        try:
            user_id = re.search(r"User ID: (\d+)", message.reply_to_message.text).group(1)
            check_type = re.search(r"Tekshiruv:\s*(.+)", message.reply_to_message.text).group(1)
            lines = message.reply_to_message.text.splitlines()
            # Faqat kerakli qatorlarni ajratib olish
            result = "\n".join(
                [line for line in lines if "User ID:" in line or "Tekshiruv:" in line or "Status:" in line])
            text = f'<b>{result}\n\nSababi:</b>{message.text}\n<b>Support:</b>{message.author_signature}'
            await message.reply_to_message.edit_text(text=text)
            text = f'<b>{result}\n\nSababi:</b>{message.text}\n'
            await message.bot.send_message(chat_id=user_id, text=text)
            if check_type == '🚕 Moshina Tekshiruvi':
                MachineCheckService.update(telegram_id=user_id, status="rejected", rejection_reason=message.text)
            else:
                FaceCheckService.update(telegram_id=user_id, status="rejected", rejection_reason=message.text)
            await sleep(3)
            await message.delete()
        except:
            pass
