import telegram.ext as tg_ext

from telegram.ext import filters, MessageHandler, CommandHandler, ContextTypes
from telegram import Update
from telegram.constants import ParseMode
from .calculator import requested_config

text = f'Send me sizing:\n' \
       f'`/calculate vcpu=240 vram=480 vssd=12000`\n' \
       f'Options:\n' \
       f'`cpu_vendor=`(amd/intel, default=any)\n' \
       f'`cpu_min_frequency=`(default=0)\n' \
       f'`cpu_overcommit=`(default=3)\n' \
       f'`works_main=`(default=vSphere)\n' \
       f'`works_add=`(default=Нет)\n' \
       f'(нет, vsphere, dr ,veeam, alb, tanzu, vdi, vdi public, vdi gpu, nsx)' \
       f'`network_card_qty=`(default=1)\n' \
       f'`slack_space=`(default=0.2)\n' \
       f'`capacity_disk_type=`(default=ssd)\n'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text,
                                   parse_mode=ParseMode.MARKDOWN)


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
    cpu_overcommit = int(args.get('cpu_overcommit', 3))
    works_main = args.get('works_main', 'vsphere')
    works_add = args.get('works_add', 'нет')
    network_card_qty = int(args.get('network_card_qty', 1))
    slack_space = float(args.get('slack_space', 0.2))
    capacity_disk_type = args.get('capacity_disk_type', 'ssd')

    top5 = requested_config(vcpu=vcpu, vram=vram, vssd=vssd,
                            cpu_vendor=cpu_vendor, cpu_min_frequency=cpu_min_frequency, cpu_overcommit=cpu_overcommit,
                            works_main=works_main.lower(), works_add=works_add.lower(), network_card_qty=network_card_qty,
                            slack_space=slack_space, capacity_disk_type=capacity_disk_type.lower())
    await context.bot.send_message(chat_id=update.effective_chat.id, text=top5,
                                   parse_mode=ParseMode.MARKDOWN)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def setup_all_handlers(application: tg_ext.Application) -> None:
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), start)
    calc_handler = CommandHandler('calculate', calculate)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(echo_handler)
    application.add_handler(calc_handler)

    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
