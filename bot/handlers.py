import json
import math

import telegram.ext as tg_ext

from telegram.ext import filters, MessageHandler, CommandHandler, ContextTypes
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
    # inline_keyboard = [
    #     [InlineKeyboardButton("Open in app",
    #                           web_app=WebAppInfo(url="https://vitaliyivanovspb.github.io/selectel_vmware"),
    #                           callback_data=)]
    # ]
    # inline_reply_markup = InlineKeyboardMarkup(inline_keyboard)
    # await context.bot.send_message(chat_id=update.effective_chat.id,
    #                                text=text,
    #                                parse_mode=ParseMode.MARKDOWN, reply_markup=inline_reply_markup)


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

    top5 = requested_config(vcpu=vcpu, vram=vram, vssd=vssd,
                            cpu_vendor=cpu_vendor, cpu_min_frequency=cpu_min_frequency, cpu_overcommit=cpu_overcommit,
                            works_main=works_main.lower(), works_add=works_add.lower(),
                            network_card_qty=network_card_qty,
                            slack_space=slack_space, capacity_disk_type=capacity_disk_type.lower(), currency=currency)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=top5)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


async def webapp_data(update: Update, context):
    json_str = update.message.web_app_data.data
    try:
        data = json.loads(json_str)
        usd = get_cbr_currency_rate()
        await update.message.reply_text(f'Received data: {data}')
        top5 = requested_config(vcpu=int(data['vcpu']), vram=int(data['vram']), vssd=int(data['vssd']),
                                cpu_vendor=data['cpu_vendor'],
                                cpu_min_frequency=int(data['cpu_min_frequency']),
                                cpu_overcommit=float(data['cpu_overcommit']),
                                works_main=data['works_main'],
                                works_add=data['works_add'],
                                network_card_qty=int(data['network_card_qty']),
                                slack_space=float(data['slack_space']),
                                capacity_disk_type=data['capacity_disk_type'],
                                currency=math.ceil(float(data['currency']) if data['currency']!='' else (usd if usd else 100)))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=top5)
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
        return None


def setup_all_handlers(application: tg_ext.Application) -> None:
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), start)
    calc_handler = CommandHandler('calculate', calculate)
    web_app_handler = MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(echo_handler)
    application.add_handler(calc_handler)
    application.add_handler(web_app_handler)

    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
