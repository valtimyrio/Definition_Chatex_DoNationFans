from discord.ext import commands
from discord.utils import get
import discord
from bd import *
from chatex_requests import *


class Discord:
    def __init__(self, bd):
        self.app_id = "891272172599910430"
        self.public_key = "8191ff43ffc6cf08e003ef4b2e692d0b98ab74ae566af14d3dd5c04b2a28f9c3"
        self.bot_token = "ODkxNjA5NzU2MDE4NTYxMDQ0.YVA2Sw.2tT-bWYli1n7ExRVflEgl82cIa0"
        self.bd = bd
        self.chatex = Chatex()
        self.info = """```Привет! 
        
Я - бот, управляющий твоим статусом на этом сервере!

Новый статус позволит открыть тебе много нового и неизведанного! Его можно приобрести за баллы.

Для оплаты баллов используется Chatex, для начала - 
узнай, как пополнить кошелек командой "Пополнить баланс"

Чтобы узнать, какие есть статусы - напиши "Покажи статусы"

Для покупки статуса введи "Дай статус 'статус'"```
        """
        self.members = {}
        self.guilds = {}

    def message_check_manageble(self, message):
        if "основной" in str(message.channel):
            return True
        return False

    def message_check_startswith(self, message, word):
        if message.content.lower().startswith(word.lower()):
            return True
        return False

    def start_bot(self):

        intents = discord.Intents()
        intents.all()
        intents.members = True
        client = discord.Client()

        bot = commands.Bot(command_prefix="!", intents=intents)

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return

            elif self.message_check_manageble(message):
                member = message.author
                guild = message.guild
                name = str(message.guild.name)

                if member not in self.members:
                    self.members[member.name] = member

                if member not in self.guilds:
                    self.guilds[guild.name] = guild

                if self.message_check_startswith(message, "дай статус"):
                    mess = message.content[11:]
                    if mess in self.bd.get_roles_list(name):
                        if self.bd.check_member_has_role(member.id, name, mess):
                            await message.channel.send("У вас уже есть такая роль!")
                        else:
                            try:
                                if self.bd.get_member_balance(member.id, member.name,
                                                              message.channel.id, name) >= self.bd.get_role_price(
                                    mess, name):
                                    self.bd.change_member_balance(member.id, member.name, message.guild.id, -1 * int(
                                        self.bd.get_role_price(mess, name)), name)
                                    role = discord.utils.get(message.guild.roles, name=mess)
                                    self.bd.add_role(member.id, member.name, message.guild.id, name, mess)
                                    await member.add_roles(role)
                                    await message.channel.send("Роль успешно добавлена")
                                else:
                                    await message.channel.send("У вас не хватает средств!")

                            except Exception:
                                await message.channel.send("Вас не найдено в системе!")


                    else:
                        await message.channel.send("Не понятно!")
                        await message.channel.send(self.info)

                elif self.message_check_startswith(message, "удали статус"):
                    mess = message.content[13:]
                    print(mess)
                    if mess in self.bd.get_roles_list(name):
                        if self.bd.check_member_has_role(member.id, name, mess):
                            try:
                                role = discord.utils.get(message.guild.roles, name=mess)
                                await member.remove_roles(role)
                                self.bd.delete_role(member.id, member.name, message.guild.id, name, mess)
                                await message.channel.send("Роль успешно удалена")
                            except Exception:
                                await message.channel.send("Вас не найдено в системе!")
                        else:
                            await message.channel.send("У вас еще нет такой роли!")
                    else:
                        await message.channel.send("Не понятно!")
                        await message.channel.send(self.info)

                elif self.message_check_startswith(message, "Покажи статусы"):
                    mes1s = ''
                    for role in self.bd.get_roles_list(name):
                        mes1s += str(self.bd.get_role_price(str(role), name)) + "\t\t\t\t" + str(role) + "\n"
                    await message.channel.send('```' + mes1s + '```')



                elif self.message_check_startswith(message, "баланс"):
                    await message.channel.send(
                       "Ваш баланс: " + str(self.bd.get_member_balance(member.id, member.name, message.channel.id, name))
                    )

                elif self.message_check_startswith(message, "пополнить баланс"):
                    coins = {"BTC": [1000000, 0.001], "USDT_ERC20": [1000, 100]}
                    coins_list = list(coins)
                    try:
                        await message.channel.send("""```
Пожалуйста, введите запрос в формате "пополнить баланс x coin", где:
x - количество
coin - валюта

Текущие доступные валюты: 

BTC:
предел - 0.001 BTC
курс 1000000 за 1 BTC 

USDT_ERC20:
предел - $100
курс 1000 за $1``` 
                        """)
                        x = float(message.content.split()[-2])
                        coin_type = message.content.split()[-1]
                        if x < 0:
                            await message.channel.send("**Отрицательное число**")
                            raise Exception
                        if coin_type not in coins_list:
                            await message.channel.send("**Не та валюта**")
                            raise Exception
                        if x > coins[coin_type][1]:
                            await message.channel.send("**Выход из лимита**")
                            raise Exception
                        print("cointype: " + coin_type)
                        temp_id, url = self.chatex.create_invoice(coin_type, x)
                        self.bd.change_member_last_id(member.id, member.name, message.channel.id, temp_id, name)
                        self.bd.change_member_last_amount(member.id, member.name, message.channel.id,
                                                          x * coins[coin_type][0], name)

                        await message.channel.send("Пожалуйста, оплатите, *ссылка* ниже")
                        await message.channel.send(url)
                        await message.channel.send('После оплаты напишите "Проверить"')
                    except Exception:
                        await message.channel.send(
                            "Введите, пожалуйста, положительное число, входящее в предел, и правильную валюту!")

                elif self.message_check_startswith(message, "проверить"):
                    status = self.chatex.get_invoice(
                        self.bd.get_member_last_id(member.id, member.name, message.channel.id, name))
                    if status == "COMPLETED":
                        await message.channel.send("Отлично!")
                        self.bd.change_member_balance(member.id, member.name, message.channel.id,
                                                      self.bd.get_member_last_amount(
                                                          member.id, member.name, message.channel.id, name), name)

                        await message.channel.send("На счет зачислено: " + str(
                            self.bd.get_member_last_amount(member.id, member.name, message.channel.id, name)))

                    elif status == "ACTIVE":
                        await message.channel.send("Вы еще не оплатили, или оплата не дошла!")

                    else:
                        await message.channel.send("Вы еще не оплатили, или оплата не дошла!")

                elif self.message_check_startswith(message, "даты"):
                    temp_member = None
                    temp_guild = None
                    temp_list = self.bd.check_all_dates()

                    for i in range(0, len(temp_list), 1):
                        self.bd.delete_role(temp_list[i][0],
                                            temp_list[i][1],
                                            temp_list[i][2],
                                            temp_list[i][3],
                                            temp_list[i][4],
                                            )

                        for member in self.members:
                            if temp_list[i][1] == self.members[member].name and self.members[member].guild.name == temp_list[i][5]:
                                temp_member = self.members[member]

                        for guild in self.guilds:
                            if temp_list[i][5] == self.guilds[guild].name:
                                temp_guild = self.guilds[guild]

                        role = discord.utils.get(temp_guild.roles, name=temp_list[i][4])
                        await temp_member.remove_roles(role)
                        await message.channel.send("Удалено! " + temp_list[i][4])

                elif self.message_check_startswith(message, "тестовая"):
                    print(message.guild.id, message.guild.name)
                    print(message.guild.roles)

                elif self.message_check_startswith(message, ""):
                    await message.channel.send(self.info)

        client.run(self.bot_token)
        # bot.run(self.bot_token)

