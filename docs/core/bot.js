require('dotenv').config();
const { Telegraf } = require('telegraf');
const bot = new Telegraf(process.env.TELEGRAM_BOT_TOKEN);
bot.start((ctx) => ctx.reply('HADES ONLINE - DEPREDADOR90 ACTIVADO'));
bot.command('status', (ctx) => ctx.reply('SISTEMA ONLINE - MODO DIOS - N.C.P.C. x90'));
bot.launch().then(() => console.log('HADES ONLINE'));
