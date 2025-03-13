import json
import math

import telegram.ext as tg_ext

from telegram.ext import filters, MessageHandler, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from .calculator import requested_config
from .cbr import get_cbr_currency_rate

text = f'Send me sizing:\n' \
       f'`/calculate vcpu=240 vram=480 vssd=12000`\n' \
       f'Options:\n' \
       f'`cpu_vendor=`(amd/intel, default=any)\n' \
       f'`cpu_min_frequency=`(default=0)\n' \
       f'`cpu_overcommit=`(default=3)\n' \
       f'`works_main=`(default=vsphere)\n' \
       f'`works_add=`(default=no)\n' \
       f'(no, vsphere, dr ,veeam, alb, tanzu, vdi, vdi\_public, vdi\_gpu, vdi\_gpu\_public, nsx)\n' \
       f'`network_card_qty=`(default=1)\n' \
       f'`slack_space=`(default=0.2)\n' \
       f'`capacity_disk_type=`(default=ssd)\n' \
       f'`currency=`(default=cbr or 100)\n'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Calculator",
                        web_app=WebAppInfo(url="https://vitaliyivanovspb.github.io/selectel_vmware"))]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text,
                                   parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = {item.split('=')[0]: item.split('=')[1] for item in context.args}
    required_keys = {'vcpu', 'vram', 'vssd'}
    missing_keys = required_keys - args.keys()

    if missing_keys:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Ошибка: отсутствуют параметры - {", ".join(missing_keys)}'
        )
        return

    vcpu = int(args['vcpu'])
    vram = int(args['vram'])
    vssd = int(args['vssd'])

    cpu_vendor = args.get('cpu_vendor', 'any')
    cpu_min_frequency = int(args.get('cpu_min_frequency', 0))
    cpu_overcommit = float(args.get('cpu_overcommit', 3))
    works_main = args.get('works_main', 'vsphere')
    works_add = args.get('works_add', 'no')
    network_card_qty = int(args.get('network_card_qty', 1))
    slack_space = float(args.get('slack_space', 0.2))
    capacity_disk_type = args.get('capacity_disk_type', 'ssd')
    usd = get_cbr_currency_rate()
    currency = int(args.get('currency', math.ceil(usd) if usd else 100))

    all_configs = requested_config(vcpu=vcpu, vram=vram, vssd=vssd,
                                   cpu_vendor=cpu_vendor, cpu_min_frequency=cpu_min_frequency,
                                   cpu_overcommit=cpu_overcommit,
                                   works_main=works_main.lower(), works_add=works_add.lower(),
                                   network_card_qty=network_card_qty,
                                   slack_space=slack_space, capacity_disk_type=capacity_disk_type.lower(),
                                   currency=currency)
    context.user_data['configs'] = all_configs
    context.user_data['page'] = 0
    await send_config_page(update, context)


async def send_config_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    page = context.user_data.get('page', 0)
    all_configs = context.user_data.get('configs', [])

    configs_per_page = 3
    start = page * configs_per_page
    end = start + configs_per_page
    paginated_configs = all_configs[start:end]

    text = "".join(format_config(i + start + 1, conf) for i, conf in enumerate(paginated_configs))

    keyboard = []
    if start > 0:
        keyboard.append(InlineKeyboardButton("⬅️ Prev", callback_data="prev"))
    if end < len(all_configs):
        keyboard.append(InlineKeyboardButton("Next ➡️", callback_data="next"))

    reply_markup = InlineKeyboardMarkup([keyboard]) if keyboard else None

    if update.message:  # Если это команда /calculate
        await update.message.reply_text(text, reply_markup=reply_markup)
    elif update.callback_query:  # Если это нажатие на кнопку "Вперёд" или "Назад"
        query = update.callback_query
        await query.answer()
        await query.message.edit_text(text, reply_markup=reply_markup)


async def change_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "prev":
        context.user_data['page'] = max(0, context.user_data['page'] - 1)
    elif query.data == "next":
        context.user_data['page'] = min(len(context.user_data['configs']) // 3, context.user_data['page'] + 1)

    await send_config_page(update, context)


def format_config(index, config):
    conf = [f'\nТоп {index}:\n']
    for key, value in config.items():
        conf.append(f'{key}: {value}\n')
    return "".join(conf)


def format_configs(sorted_configs):
    top5 = []
    for index, config in enumerate(sorted_configs, 1):
        conf = [f'\nТоп {index}:\n']
        for key, value in config.items():
            conf.append(f'{key}: {value}\n')
        top5.append(conf)
    return ''.join([item for sublist in top5 for item in sublist])


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


async def webapp_data(update: Update, context):
    json_str = update.message.web_app_data.data
    try:
        data = json.loads(json_str)
        usd = get_cbr_currency_rate()
        await update.message.reply_text(f'Received data: {data}')
        all_configs = requested_config(vcpu=int(data['vcpu']), vram=int(data['vram']), vssd=int(data['vssd']),
                                       cpu_vendor=data['cpu_vendor'],
                                       cpu_min_frequency=int(data['cpu_min_frequency']),
                                       cpu_overcommit=float(data['cpu_overcommit']),
                                       works_main=data['works_main'],
                                       works_add=data['works_add'],
                                       network_card_qty=int(data['network_card_qty']),
                                       slack_space=float(data['slack_space']),
                                       capacity_disk_type=data['capacity_disk_type'],
                                       currency=math.ceil(
                                           float(data['currency']) if data['currency'] != '' else (
                                               usd if usd else 100)))
        context.user_data['configs'] = all_configs
        context.user_data['page'] = 0
        await send_config_page(update, context)
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
        return None


def setup_all_handlers(application: tg_ext.Application) -> None:
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), start)
    calc_handler = CommandHandler('calculate', calculate)
    web_app_handler = MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data)
    change_page_handler = CallbackQueryHandler(change_page)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(echo_handler)
    application.add_handler(calc_handler)
    application.add_handler(web_app_handler)
    application.add_handler(change_page_handler)

    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
