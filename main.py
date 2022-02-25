import asyncio, requests, random, os, decimal, json, traceback, natsort, discord, math
from time import sleep, time_ns, time
from urllib.parse import unquote, quote

try:
  from replit import db
  import keep_alive
  is_beta = False
except Exception:
  import token_getter
  is_beta = True

decimal.getcontext().prec = 1998

intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents=intents)

def give_card(number, cards_list):
  returns = []
  for i in range(number):
    returns.append(cards_list.pop(random.randint(0, len(cards_list) - 1)))
  if number == 1:
    return returns[0]
  return cards_list, returns

def heist_level(person_id):
  level = get_value(person_id, "heist_level")
  if level != 11:
    sum_2 = level * 10000
    chance_2 = level * 10
    if level == 1:
      sum_1 = 1000
    elif level == 10:
      sum_1 = 0
    else:
      sum_1 = (level - 1) * 10000
  else:
    sum_2 = 1000000
    sum_1 = 0
    chance_2 = 100
  return 100 - chance_2, sum_1, chance_2, sum_2

def change_value(person_id, key, value, add=False):
  file = open("balances.json", "r")
  balances = json.load(file)
  try:
    if add:
      balances[str(person_id)][key] = value + balances[str(person_id)][key]
    else:
      balances[str(person_id)][key] = value
  except:
    balances[str(person_id)] = {key: value}
  file.close()
  file1 = open("balances.json", "w")
  json.dump(balances,  file1)
  file1.close()
  return value

def give_money(person_id, money, multi=True):
  if money >= 0:
    if get_value(person_id, "multiplier") == None:
      change_value(person_id, "multiplier", 1)
    if multi == True:
      money = money * get_value(person_id, "multiplier")
  value = change_value(person_id, "money", money, True)
  return add_commas(value)

def add_commas(inp):
  return f'{inp:,}'

def get_value(person_id, value):
  file = open("balances.json", "r")
  balances = json.load(file)
  file.close()
  try:
    result = balances[str(person_id)][value]
  except:
    change_value(str(person_id), value, None)
    result = None
  return result

async def generate(queston_body, question_type, setuper, question_contents=None):
    milenakos = bot.get_user(553093932012011520)
    if question_contents:
        if question_type == "3":
            question_contents.insert(0, 0)
        second_part = str(question_contents)
    else:
        second_part = question_type
    await milenakos.send("<@" + str(setuper.id) + "> suggested:\n\"" + queston_body + "\": " + second_part + ",")

def add_ad(embedVar):
  ad = random.randint(0, 5)
  if ad == 0 or ad == 1:
    embedVar.set_footer(text = "donate to teamseas.org!",icon_url="https://assets01.teamassets.net/assets/images/teamseas-logo.png")
  elif ad == 2 or ad == 3:
    embedVar.set_footer(text = "subscribe to my yt: youtube.com/c/Milenakos",icon_url="https://yt3.ggpht.com/ytc/AKedOLTBVtfNNsa1PvedSlLz9bzKYkNTDYF8dRVF46Bu=s88-c-k-c0x00ffffff-no-rj")
  elif ad == 4:
    embedVar.set_footer(text = "sub to pewds",icon_url="https://yt3.ggpht.com/5oUY3tashyxfqsjO5SGhjT4dus8FkN9CsAHwXWISFrdPYii1FudD4ICtLfuCw6-THJsJbgoY=s88-c-k-c0x00ffffff-no-rj")
  else:
    embedVar.set_footer(text = "sponsored by nord vpn (this is joke; vpns are bad)",icon_url="https://rents.ws/ru/image/good/800531/")
  return embedVar

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='bored help'))

simon_says = {"simon says talk in chat": "0",
              "simon says don't talk in chat": "1",
              "talk in chat": "1",
              "simon asks whos joe?": [0, "mama"],
              "simon says what is obamas last name?": ["obama"],
              "simon says how do you spell carl bot (CaSe SeNsEtIvE)": ["carl-bot"],
              "slmon says how much google results there are for query: \"funny image\" as of September 2021?": [0, "1,940", "1940"],
              "simon says what is most played among us color?": ["red"],
              "simon says copy-paste my about me section": ["oh my gosh why did you read it"],
              "simon says what is my status (i changed it for this round)": ["5854731"],
              "SIMON 5AYS name third difficulty of bored ttt": [0, "impossible"],
              "simon says what is extension of powerpoint document?": ["ppt", "pps"],
              "who owns minecraft?": [0, "microsoft", "xbox", "windows"],
              "There is an error happend: list index out of range (list simon_says)\nContinue anyway?": [0, "yes"],
              "simon says jasiodl2134fjasjdaiud=:{>}{>}:}>}{ja6sjahd8sav;dfuvsf": "0",
              "say banana": [0, "banana"],
              "simon says say banana": ["banana"],
              "simon says what is 2+2?": ["4", "four"],
              "what is 2 * 7?": [0, "14", "fourteen"],
              "simon says talk in chat ||to become loser||": "1",
              "simon says say my tag": ["1275"],
              "simon says chill out. free round.": "0",
              "simone says say im winner": [0, "im winner"],
              "simon says say im bored and shut": ["im bored and shut"],
              "simon says say name of this video https://youtu.be/NLAS5bS1EII": ["angry bords"],
              "simon says name any minecraft ore": ["iron", "gold", "coal", "redstone", "lapis", "diamond", "emerald", "quartz", "copper", "debris"],
              "simon says name any minecraft boss": ["dragon", "wither", "guardian"],
              "simon says whats 34 x 88?": ["2992", "2,992"],
              "simon say how much levels do geometry dash have (as of 2.1)?": [0, "21"],
              "simon says what line is next after never gonna give you up": ["never gonna let you down"],
              "simon says what is the capital of latvia": ["riga"],
              "simon says you stupid": "0",
              "simon says play rock paper scissors": ["rock", "paper", "scissors"],
              "sim0n says person below will win": "1",
              "simones says name any minecraft ore": [0, "iron", "gold", "coal", "redstone", "lapis", "diamond", "emerald", "quartz", "copper", "debris"]}

simon_active = False
ttt_active = False
channel_check = 0
b = "e"
players_, players, question_contents, passed_, failed, cards_list, players_list, cards_s, current_card, turn = [], [], [], [], [], [], [], [], [], []
state = False
setuper = question_type = queston_body = step = None
file = open("pi.json", "r")
pi_list = json.load(file)
req = False
pi = decimal.Decimal(pi_list[0])
pi_ = pi_list[2]
spam_allowed = True
pi1 = decimal.Decimal(pi_list[1])
file.close()
job = False
worker = None

@bot.event
async def on_message(message):
    original = message.content
    text = original.lower()
    global ttt_active, simon_active, players_, players_list, cards_s, cards_listcurrent_card, turn, channel_check, b, pi, pi1, pi_, job, failed, state, players, passed_, spam_allowed, question_type, queston_body, question_contents, step, setup, setuper, req, worker
    try:
        if message.guild != None and int(message.guild.id) == 776546039804330005 and text.startswith("pls"):
          role = discord.utils.get(message.guild.roles, name="(1) a chill sent a message person")

          if role not in message.author.roles:
            embedVar = discord.Embed(description="hi, you got kicked in a chill server for using dank memer commands before level 1, if you wanna get back in there you can use this link: discord.gg/tcSpWhnhTX\nsorry for inconviencene caused /shrug", color=0x00ff00)
            await message.author.send(embed=add_ad(embedVar))
            await message.author.kick(reason="[AUTOMATIC] using dank memer before level 1")
            await message.reply(embed=add_ad(discord.Embed(description="i kicked this idiot for using dank memer before level 1 lol noob get gud", color=0x00ff00)))
            return

        if message.guild == None and message.author.id != 834425748361445406 and message.author.id != 904047456327729172:
          if message.author not in players_:
            await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="no u my dms closed")))
          else:                  
            if turn == players_.index(message.author):
              make_move = True
              unoed = False

              if text == "uno" and len(cards_s[turn % len(players_list)]) == 1:
                if current_card[-1] == cards_s[turn % len(players_list)][0][-1] or current_card[:-1] == cards_s[turn % len(players_list)][0][:-1]:
                  text = "1"
                  unoed = True
              
              if text == "draw":
                ccarrds = cards_s[turn % len(players_list)]
                cards_list, new = give_card(1, cards_list)
                ccarrds.append(new)
                cards_s[turn % len(players_list)] = ccarrds
                turn += 1
                make_move = False
              
              if make_move:
                if current_card[-1] == cards_s[turn % len(players_list)][int(text) - 1][-1] or current_card[:-1] == cards_s[turn % len(players_list)][int(text) - 1][:-1]:
                  try:
                    ccarrds = cards_s[turn % len(players_list)]
                    current_card = ccarrds.pop(int(text) - 1)
                    if unoed:
                      cards_s[turn % len(players_list)] = 0
                    else:
                      cards_s[turn % len(players_list)] = ccarrds
                    turn += 1
                  except Exception as e:
                    print(e)
                else:
                  print(f"INCORRECT CARD {cards_s[turn % len(players_list)][int(text) - 1]}")
            elif text == "uno" and cards_s[turn % len(players_list)] != 0 and len(cards_s[turn % len(players_list)]) == 0:
              ccarrds = cards_s[turn % len(players_list)]
              cards_list, new = give_card(2, cards_list)
              ccarrds.append(new)
              cards_s[turn % len(players_list)] = ccarrds
          return

        if int(message.author.id) == 735147814878969968 and original.startswith("Thx for bumping our Server! We will remind you in 2 hours!") and int(message.guild.id) == 776546039804330005:
          await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="ty for bumping, you got 1000$")))
          person = text[-19:-1]
          if person[0] == "!":
              person = person[1:]
          give_money(person, 1000)
        
        if job == 3 and message.author == worker:
          try:
            num = int(text)
            if num > req:
              await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="My number is lower than this!")))
            if num < req:
              await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="My number is higher than this!")))
          except ValueError:
            pass

        if job == 5 and message.author == worker and text != req:
          await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="wrong nub try better next time")))
          req = False
          worker = False
          job = False
          change_value(message.author.id, "rep", -2, True)

        if job and text == str(req) and message.author == worker:
          if job == 1:
            income = random.randint(50, 250)
          elif job == 2:
            income = random.randint(100, 300)
          elif job == 3:
            income = random.randint(200, 500)
          elif job == 4:
            income = random.randint(20, 100)
          elif job == 5:
            income = random.randint(50, 200)
          await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="ok good job you got " + str(give_money(worker.id, income)) + "$ gg")))
          req = False
          worker = False
          job = False
          change_value(message.author.id, "rep", 7, True)
        
        if message.author == setuper:
            if step == 1:
                queston_body = text
                await setup.edit(embed=add_ad(discord.Embed(color=0x00ff00, description="Question setup (2/3):\n\n**What is type of your question?**\n\n0 - No eleminations." +
                    "\n1 - Eliminate everyone who chat.\n2 - Eleminate everyone who DIDNT said specific thing." +
                    "\n3 - Eleminate everyone who DID said specific thing.")))
                await message.delete()
                step += 1
            elif step == 2:
                if not (text == "0" or text == "1" or text == "2" or text == "3"):
                    return
                question_type = text
                await message.delete()
                if text == "0" or text == "1":
                    await setup.edit(embed=add_ad(discord.Embed(color=0x00ff00, description="Got it! Setup was finished and question was submitted!")))
                    await generate(queston_body, question_type, setuper)
                    setuper = question_type = queston_body = None
                    question_contents = []
                    await asyncio.sleep(10)
                    await setup.delete()
                else:
                    await setup.edit(embed=add_ad(discord.Embed(color=0x00ff00, description="Question setup (3/3):\n\n**What is contents of your question?**\n\nWhat is \"specific thing\"?" +
                        "\n(each message will be interpreted as serperate thing; type \"finish\" to exit.)")))
                    step += 1
            elif step == 3:
                await message.delete()
                if text == "finish":
                    await setup.edit(embed=add_ad(discord.Embed(color=0x00ff00, description="Got it! Setup was finished and question was submitted!")))
                    await generate(queston_body, question_type, setuper, question_contents)
                    setuper = question_type = queston_body = None
                    question_contents = []
                    await asyncio.sleep(10)
                    await setup.delete()
                else:
                    question_contents.append(text)
        
        if text.startswith('?nuke'):
            await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="CARL-BOT: NUKE ACTIVATED")))
            await asyncio.sleep(2)
            await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="NUKING USER " + text[6:] + "...")))
            await asyncio.sleep(3)
            await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="NUKE SENT SUCCESSFULLY")))
            await asyncio.sleep(10)
            user1 = bot.get_user(int(text[9:-1]))
            for _ in range(0, 20):
                await user1.send(embed=add_ad(discord.Embed(color=0x00ff00, description=random.choice(["YOU GOT NUKED!!! KABOOM!!!", "BOOOM!! NUKE EXPLODED YOU!", "YOUR HOUSE WAS JUST BLOWN UP BY NUKE!!!", "BOOM BOOOM!! KAPOW!!!"]))))
        
        if text == "nuke me":
            await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="CARL-BOT: NUKE ACTIVATED")))
            await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="NUKING USER <@" + str(message.author.id) + ">...")))
            await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="NUKE SENT SUCCESSFULLY")))
            user1 = message.author
            while True:
                await user1.send(embed=add_ad(discord.Embed(color=0x00ff00, description=random.choice(["YOU GOT NUKED!!! KABOOM!!!", "BOOOM!! NUKE EXPLODED YOU!", "YOUR HOUSE WAS JUST BLOWN UP BY NUKE!!!", "BOOM BOOOM!! KAPOW!!!"]))))
        
        if text == "ddg":
            pain = await message.channel.fetch_message(message.reference.message_id)
            await message.channel.send("https://duckduckgo.com/" + quote(pain.content))

        if text.startswith('bored '):
            text = text[6:]
            original = original[6:]

            if get_value(message.author.id, "rep") == None:
              change_value(message.author.id, "rep", 0)

            if random.randint(0, 20) == 14:
              val = give_money(message.author.id, get_value(message.author.id, "rep"), False)
              oh_prefix = "FUCK"
              if get_value(message.author.id, "rep") > 0:
                oh_prefix = "YEAH!"
              await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description=f"**OH " + oh_prefix + "**\n\nyou just gained money equal to your rep, or exactly {val}$!")))
            
            if text == "crash":
              raise UserCrashException

            if text == "leave":
              try:
                players.remove(message.author)
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="simon says <@" + str(message.author.id) + "> left game lol")))
                return
              except:
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="simon says <@" + str(message.author.id) + "> you dumb we are not playing")))
            
            elif text == "ping":
              await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description=f'Pong! Latency is {round(bot.latency * 1000)} ms!')))
            
            elif text == 'help':
                embed = discord.Embed(title="Help", description="'bored simon says', 'bored legal', 'bored delete', 'bored privacy_policy', 'bored trivia, 'bored idea', 'bored rickroll', bored ai <text>', bored ttt', 'bored leave', 'bored simon make', 'bored joke', 'bored fact', 'bored pi', 'bored ping', 'bored uno'", color=0x00ff00).set_author(name="By using this bot you agree to the Terms Of Service and Privacy Policy of it. `bored legal` for more.")
                embed.add_field(name="Economy commands", value="'bored passive, 'bored outside', 'bored bal', 'bored casino', 'bored rob', bored shop', 'bored reset', 'bored work', 'bored lb', 'bored murder', 'bored heist', bored weapon shop', 'bored heist shop' 'bored donate', 'bored daily', 'bored weekly'")
                await message.reply(embed=add_ad(embed))
            
            elif text == "casino":
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="gamble: bored coinflip, more commands later")))

            elif text == "legal":
                embed = discord.Embed(title="Legal", description="By using this bot you agree to the [Terms Of Service](https://docs.google.com/document/d/1SI7FZrKloBk_E7RyplW-tXiHKPcsE-7RWZ3AQZP1He0/edit?usp=sharing) and [Privacy Policy](https://docs.google.com/document/d/1xbeefSewYGOCP8gWDrw3I2rGt1MRZkS6ctluFuvkKvE/edit?usp=sharing) of it.")
                await message.reply(embed=add_ad(embed))

            elif text == "privacy_policy":
                embed = discord.Embed(title="Everything I know about you.", color=0x0066ff, description="Check [Privacy Policy](https://docs.google.com/document/d/1xbeefSewYGOCP8gWDrw3I2rGt1MRZkS6ctluFuvkKvE/edit?usp=sharing) for more info.")
                
                file = open("balances.json", "r")
                balances = json.load(file)
                embed.add_field(name="userid", value=str(message.author.id), inline=True)
                
                for a,b in balances[str(message.author.id)].items():
                  embed.add_field(name=a, value=b, inline=True)
                
                await message.reply(embed=add_ad(embed))
                
                file.close()

            elif text == "delete":
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="This will delete EVERYTHING bot knows about you. This includes all your money, multiplier, items, rep, passive income and everything else. Please use `bored delete agree` to progress.")))

            elif text == "delete agree":
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="Are You Sure? Reminder: This will delete EVERYTHING bot knows about you. Use `bored delete yes` to delete all your data.")))

            elif text == "delete yes":
                file = open("balances.json", "r")
                balances = json.load(file)
                balances.pop(str(message.author.id))
                file.close()
                file1 = open("balances.json", "w")
                json.dump(balances, file1)
                file1.close()
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="Done! You can now put word \"bored\" into your blacklist or something like that.")))

            elif text == "why is my luck bad":
                if random.randint(0, 1) == 0:
                  await message.reply("get good lol")
                else:
                  await message.reply("imagine being broke")

            elif text == "coinflip":
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="syntax: bored coinflip <money> <heads or tails>\n(with no <> ofc)")))

            elif text == "rickroll":
                rickrolls = ["https://youtu.be/vLRyJ0dawjM", "https://youtu.be/6vJwwRUtwMw", "https://youtu.be/aYsgsSo1aow", "https://youtu.be/bPZSDBvDmVw", "https://youtu.be/mW61VTLhNjQ", "https://youtu.be/s5wTiLJ9NVs", "https://youtu.be/dQw4w9WgXcQ"]
                await message.reply(random.choice(rickrolls))

            elif text == "idea":
                flist = ["go outside", "wait until m(._.)m goes online", "touch grass", "find user with 69 in their tag", "*H Y D R A T E*", "rickroll yourself"]
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description=random.choice(flist))))

            elif text.startswith("coinflip "):
                text = text[9:]
                things = text.split(" ")

                try:
                  sum = int(things[0])
                except:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you dumb money is number")))
                  return
                side = things[1]
                if get_value(message.author.id, "money") < sum:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="no u loop hole fixed ahahhaha")))
                  return

                if side == "heads" or side == "tails":
                  coinflip = await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="Flipping coin...")))
                  await asyncio.sleep(3)
                  choosen = random.choice(["Heads", "Tails"])
                  msg = "Flipping coin... " + choosen + "!"
                  await coinflip.edit(content=msg)
                  await asyncio.sleep(2)
                  if choosen.lower() == side:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="You won! You gained " + str(give_money(message.author.id, sum, False)) + "!")))
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="You lost! You lost " + str(give_money(message.author.id, -sum)) + "!")))
                else:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="dude it is head or tails i dont understand wtf you say")))

            elif text == "passive" or text == "p":
                if get_value(message.author.id, "passive_earnings_speed_cost") == None:
                  change_value(message.author.id, "passive_earnings_balance", 0)
                  change_value(message.author.id, "passive_earnings_max", 50)
                  change_value(message.author.id, "passive_earnings_time", 0)
                  change_value(message.author.id, "passive_earnings_speed", 0)
                  change_value(message.author.id, "passive_earnings_speed_cost", 100)
                  change_value(message.author.id, "passive_earnings_max_cost", 100)

                difference = time() - get_value(message.author.id, "passive_earnings_time")
                to_add = (difference / 60) * get_value(message.author.id, "passive_earnings_speed")
                change_value(message.author.id, "passive_earnings_balance", to_add, True)
                change_value(message.author.id, "passive_earnings_time", time())

                if get_value(message.author.id, "passive_earnings_balance") > get_value(message.author.id, "passive_earnings_max"):
                  change_value(message.author.id, "passive_earnings_balance", get_value(message.author.id, "passive_earnings_max"))

                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, title="Passsive earnings dashboard", description="Balance: " + str(round(get_value(message.author.id, "passive_earnings_balance"))) + "/" + str(get_value(message.author.id, "passive_earnings_max")) + "$ (collect using bored collect)\n\n" +
                  "You are getting " + str(get_value(message.author.id, "passive_earnings_speed")) + " per minute.\n\nUpgrades:\n" +
                  "bored upgrade speed - " + str(get_value(message.author.id, "passive_earnings_speed_cost")) + "$\nbored upgrade max - " + str(get_value(message.author.id, "passive_earnings_max_cost")) + "$\n\nTertia Optio:registered:")))

            elif text == "collect":
              try:
                difference = time() - get_value(message.author.id, "passive_earnings_time")
                to_add = (difference / 60) * get_value(message.author.id, "passive_earnings_speed")
                change_value(message.author.id, "passive_earnings_balance", to_add, True)
                change_value(message.author.id, "passive_earnings_time", time())

                if get_value(message.author.id, "passive_earnings_balance") > get_value(message.author.id, "passive_earnings_max"):
                  change_value(message.author.id, "passive_earnings_balance", get_value(message.author.id, "passive_earnings_max"))

                give_money(message.author.id, round(get_value(message.author.id, "passive_earnings_balance")), False)
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="Added " + str(round(get_value(message.author.id, "passive_earnings_balance"))) + "$ to your balance!")))
                change_value(message.author.id, "passive_earnings_balance", get_value(message.author.id, "passive_earnings_balance") - round(get_value(message.author.id, "passive_earnings_balance")))
              except TypeError:
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="u got 0 bruh skill issue")))
              except Exception:
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="idiot how im supposed to give you passive money if you never ran bored p")))

            elif text == "upgrade speed":
                if get_value(message.author.id, "money") >= get_value(message.author.id, "passive_earnings_speed_cost"):
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="ok upgraded")))
                    give_money(message.author.id, -get_value(message.author.id, "passive_earnings_speed_cost"))
                    if get_value(message.author.id, "passive_earnings_speed") == 0:
                      change_value(message.author.id, "passive_earnings_speed", 1)
                    else:
                      change_value(message.author.id, "passive_earnings_speed", get_value(message.author.id, "passive_earnings_speed") * 2)
                    change_value(message.author.id, "passive_earnings_speed_cost", get_value(message.author.id, "passive_earnings_speed_cost") * 2)
                else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))

            elif text == "upgrade max":
                if get_value(message.author.id, "money") >= get_value(message.author.id, "passive_earnings_max_cost"):
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="ok upgraded")))
                    give_money(message.author.id, -get_value(message.author.id, "passive_earnings_max_cost"))
                    change_value(message.author.id, "passive_earnings_max", get_value(message.author.id, "passive_earnings_max") * 2)
                    change_value(message.author.id, "passive_earnings_max_cost", get_value(message.author.id, "passive_earnings_max_cost") * 2)
                else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))

            elif text == "donate":
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="syntax: bored donate <amount> @reciever")))
            
            elif text.startswith("donate "):
                text = text[7:]
                things = text.split()
                amount = int(things[0])
                if "trashcan" in text:
                  person = "834425748361445406"
                else:
                  person = text[-19:-1]
                  if person[0] == "!":
                    person = person[1:]

                if amount > 0 and str(person) != str(message.author.id):
                  if get_value(message.author.id, "money") >= amount:
                    give_money(message.author.id, -amount)
                    give_money(person, amount, False)
                    change_value(message.author.id, "rep", 5, True)
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="gave " + str(amount) + "$ to <@" + person + ">")))
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                else:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="what the fuck are you doing?")))
            
            elif text == "bal" or text == "balance":
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="Your balance is: " + add_commas(get_value(message.author.id, "money")) + "$ :coin: (" + str(get_value(message.author.id, "multiplier")) + "x multiplier)\nYour rep: " + str(get_value(message.author.id, "rep")))))
            
            elif text == "weapon shop":
                if get_value(message.author.id, "weaponpass"):
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="weapon shop: (use bored weapon buy <number>)\n1. small knife - 1 000$\n2. ok knife - 3 000$\n3. big knife - 5 000$\n4. small gun - 10 000$\n5. ok gun - 15 000$\n6. super gun - 25 000$\n7. shotgun - 30 000$\n8. grenade - 75 000$ (0 caught chance)")))
                else:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you dont have weapon shop pass. you can buy it in normal shop.")))
            
            elif (text.startswith("weapon buy ") or text.startswith("buy weapon")) and get_value(message.author.id, "weaponpass"):
                item = text[11:]
                if item == "1":
                  if get_value(message.author.id, "money") >= 1000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="ok now you equipped this thing")))
                    give_money(message.author.id, -1000)
                    change_value(message.author.id, "murder_chance", 25)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "2":
                  if get_value(message.author.id, "money") >= 3000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="ok now you equipped this thing")))
                    give_money(message.author.id, -3000)
                    change_value(message.author.id, "murder_chance", 35)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "3":
                  if get_value(message.author.id, "money") >= 5000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="ok now you equipped this thing")))
                    give_money(message.author.id, -5000)
                    change_value(message.author.id, "murder_chance", 45)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "4":
                  if get_value(message.author.id, "money") >= 10000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="ok now you equipped this thing")))
                    give_money(message.author.id, -10000)
                    change_value(message.author.id, "murder_chance", 55)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "5":
                  if get_value(message.author.id, "money") >= 15000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="ok now you equipped this thing")))
                    give_money(message.author.id, -15000)
                    change_value(message.author.id, "murder_chance", 70)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "6":
                  if get_value(message.author.id, "money") >= 25000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="ok now you equipped this thing")))
                    give_money(message.author.id, -25000)
                    change_value(message.author.id, "murder_chance", 80)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "7":
                  if get_value(message.author.id, "money") >= 30000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="ok now you equipped this thing")))
                    give_money(message.author.id, -30000)
                    change_value(message.author.id, "murder_chance", 90)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "8":
                  if get_value(message.author.id, "money") >= 75000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="ok now you equipped this thing")))
                    give_money(message.author.id, -75000)
                    change_value(message.author.id, "murder_chance", 100)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                else:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="are you 9 year old or smth? there is none such a thing to buy dumbass")))
            
            elif text == "lb":
                file = open("balances.json", "r")
                balances = json.load(file)
                file.close()
                results = []
                results1 = []
                for i in balances.keys():
                  try:
                    value = balances[i]["money"]
                    if int(i) == 834425748361445406 or int(i) == 904047456327729172:
                      if value >= 0:
                        results.append(str(value) + "$: Trashcan")
                      else:
                        results1.append(str(value) + "$: Trashcan")
                    else:
                      if value >= 0:
                        results.append(str(value) + "$: <@" + i + ">")
                      else:
                        results1.append(str(value) + "$: <@" + i + ">")
                  except:
                    pass
                results = natsort.natsorted(results, reverse=True)
                results1 = natsort.natsorted(results1)
                string = ""
                for i in results:
                  value, rest = i.split("$")
                  value = float(value)
                  try:
                    if int(value) == value:
                      value = int(value)
                  except Exception:
                    pass

                  value = '{:,}'.format(value)
                  string = string + value + "$" + rest + "\n"
                for i in results1:
                  value, rest = i.split("$")
                  if int(value) == float(value):
                    value = int(value)
                  else:
                    value = float(value)

                  value = '{:,}'.format(value)
                  string = string + value + "$" + rest + "\n"
                embedVar = discord.Embed(title="Leaderboards:", description=string, color=0x00ff00).set_author(name="By using this bot you agree to the Terms Of Service and Privacy Policy of it. `bored legal` for more.")
                await message.reply(embed=add_ad(embedVar))
            
            elif text == "daily":
                change_value(message.author.id, "rep", 5, True)
                last_time = get_value(message.author.id, "daily_time")
                try:
                  difference = time() - last_time
                except:
                  difference = 86400
                if difference >= 86400:
                  income = random.randint(500, 3000)
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you got your daily " + str(give_money(message.author.id, income)) + "$")))
                  change_value(message.author.id, "daily_time", time())
                else:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="there is " + str(round(86400 - difference)) + " seconds left!")))

            elif text == "weekly":
                change_value(message.author.id, "rep", 5, True)
                last_time = get_value(message.author.id, "weekly_time")
                try:
                  difference = time() - last_time
                except:
                  difference = 604800
                if difference >= 604800:
                  income = random.randint(1000, 6000)
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you got your weekly " + str(give_money(message.author.id, income)) + "$")))
                  change_value(message.author.id, "weekly_time", time())
                else:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="there is " + str(round(604800 - difference)) + " seconds left!")))

            elif text == "trivia":
              a = requests.get("https://opentdb.com/api.php?amount=1&encode=url3986").json()["results"][0]

              correct = random.randint(0, len(a["incorrect_answers"]))
              
              answers = []
              for i in a["incorrect_answers"]:
                answers.append(unquote(i))
              
              answers.insert(correct, unquote(a["correct_answer"]))
              
              q = unquote(a["question"])
              if a["type"] == "boolean":
                msg = await message.channel.send(f"{q}\n\n**1.** {answers[0]}\n**2.** {answers[1]}")
              else:
                msg = await message.channel.send(f"{q}\n\n**1.** {answers[0]}\n**2.** {answers[1]}\n**3.** {answers[2]}\n**4.** {answers[3]}")

              reactions_list = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
              for i in reactions_list:
                await msg.add_reaction(i)

              await asyncio.sleep(1)
              
              def check(reaction, user):
                return user != bot.user
              
              reaction, user = await bot.wait_for('reaction_add', check=check, timeout=60.0)
              if reactions_list.index(reaction.emoji) == correct:
                await message.channel.send(embed=add_ad(discord.Embed(color=0x00ff00, description="correct lel. correct answer: " + unquote(a["correct_answer"]))))
              else:
                await message.channel.send(embed=add_ad(discord.Embed(color=0x00ff00, description="incorrect bruh. correct answer: " + unquote(a["correct_answer"]))))
              
              for i in reactions_list:
                await msg.clear_reaction(i)

            elif text.startswith("set "):
                if int(message.author.id) == 553093932012011520:
                  text = original[4:]
                  things = text.split()
                  amount = things[0]
                  try:
                    amount = int(amount)
                  except ValueError:
                    if amount == "False":
                      amount = False
                    elif amount == "True":
                      amount = True
                    elif amount == "None":
                      amount = None
                    else:
                      amount = amount
                  value = things[1]
                  person = text[-18:]
                  if person[0] == "!":
                    person = person[1:]

                  change_value(person, value, amount)
                  result = "<@" + person + "> " + str(value) + " was set to " + str(amount) + "!"
                  embedVar = discord.Embed(title="Success!", description=result, color=0x00ff00).set_author(name="By using this bot you agree to the Terms Of Service and Privacy Policy of it. `bored legal` for more.")
                  await message.reply(embed=add_ad(embedVar))
                else:
                  embedVar = discord.Embed(title="Failure!", description="You dont have permissions for this, dummy!", color=0xff2D00).set_author(name="By using this bot you agree to the Terms Of Service and Privacy Policy of it. `bored legal` for more.")
                  await message.reply(embed=add_ad(embedVar))
            
            elif text == "shop":
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="shop: (use bored buy <number>)\n\nPasses:\n1. weapon shop pass - 500$\n2. heist shop pass - 10 000$\n\nMultipliers:\n3. 1.25x multiplier - 100 000$\n4. 1.75x multiplier - 2 000 000$\n5. 2.5x multiplier - 10 000 000$\n6. 5x multiplier - 100 000 000$\n\nmultipliers last forever for now")))
            
            elif text.startswith("buy "):
                item = text[4:]
                if item == "1" or item == "weapon pass":
                  if get_value(message.author.id, "money") >= 500:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought weapon shop pass.")))
                    give_money(message.author.id, -500)
                    change_value(message.author.id, "weaponpass", True)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "heist pass" or item == "2":
                  if get_value(message.author.id, "money") >= 10000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought heist shop pass.")))
                    give_money(message.author.id, -10000)
                    change_value(message.author.id, "heistpass", True)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "3":
                  if get_value(message.author.id, "money") >= 100000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought multiplier.")))
                    give_money(message.author.id, -100000)
                    change_value(message.author.id, "multiplier", 1.25)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "4":
                  if get_value(message.author.id, "money") >= 2000000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought multiplier.")))
                    give_money(message.author.id, -2000000)
                    change_value(message.author.id, "multiplier", 1.75)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "5":
                  if get_value(message.author.id, "money") >= 10000000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought multiplier.")))
                    give_money(message.author.id, -10000000)
                    change_value(message.author.id, "multiplier", 2.5)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "6":
                  if get_value(message.author.id, "money") >= 100000000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought multiplier.")))
                    give_money(message.author.id, -100000000)
                    change_value(message.author.id, "multiplier", 5)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                else:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="are you 9 year old or smth? there is none such a thing to buy dumbass")))

            elif text == "heist shop":
                if get_value(message.author.id, "heistpass"):
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="heist shop: (use bored heist buy <number>)\n1. bad heist gear - 10 000$\n2. ok heist gear - 25 000$\n3. good heist gear - 50 000$\n4. epic heist gear - 75 000$\n5. really good heist gear - 100 000$\n6. amazing heist gear - 250 000$\n7. fantastic heist gear - 500 000$\n8. pro heist gear - 1 000 000$\n9. master heist gear - 5 000 000$\n10. godlike heist gear - 10 000 000$")))
            
            elif (text.startswith("heist buy ") or text.startswith("buy heist ")) and get_value(message.author.id, "heistpass"):
                item = text[10:]
                if item == "1":
                  if get_value(message.author.id, "money") >= 10000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought heist gear.")))
                    give_money(message.author.id, -10000)
                    change_value(message.author.id, "heist_level", 1)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "2":
                  if get_value(message.author.id, "money") >= 25000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought heist gear.")))
                    give_money(message.author.id, -25000)
                    change_value(message.author.id, "heist_level", 2)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "3":
                  if get_value(message.author.id, "money") >= 50000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought heist gear.")))
                    give_money(message.author.id, -50000)
                    change_value(message.author.id, "heist_level", 3)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "4":
                  if get_value(message.author.id, "money") >= 75000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought heist gear.")))
                    give_money(message.author.id, -75000)
                    change_value(message.author.id, "heist_level", 4)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "5":
                  if get_value(message.author.id, "money") >= 100000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought heist gear.")))
                    give_money(message.author.id, -100000)
                    change_value(message.author.id, "heist_level", 5)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "6":
                  if get_value(message.author.id, "money") >= 250000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought heist gear.")))
                    give_money(message.author.id, -250000)
                    change_value(message.author.id, "heist_level", 6)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "7":
                  if get_value(message.author.id, "money") >= 500000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought heist gear.")))
                    give_money(message.author.id, -500000)
                    change_value(message.author.id, "heist_level", 7)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "8":
                  if get_value(message.author.id, "money") >= 1000000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought heist gear.")))
                    give_money(message.author.id, -1000000)
                    change_value(message.author.id, "heist_level", 8)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "9":
                  if get_value(message.author.id, "money") >= 5000000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought heist gear.")))
                    give_money(message.author.id, -5000000)
                    change_value(message.author.id, "heist_level", 9)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "10":
                  if get_value(message.author.id, "money") >= 10000000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought heist gear.")))
                    give_money(message.author.id, -10000000)
                    change_value(message.author.id, "heist_level", 10)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="get gud you dont have enough money")))
                elif item == "11":
                  if get_value(message.author.id, "money") >= 100000000:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you bought heist gear.")))
                    give_money(message.author.id, -100000000)
                    change_value(message.author.id, "heist_level", 11)
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="are you 9 year old or smth? there is none such a thing to buy dumbass")))
                else:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="are you 9 year old or smth? there is none such a thing to buy dumbass")))
            
            elif text == "murder" or text == "murderbored murder" or text == "murderbored murderbored murder":
                if not get_value(message.author.id, "murder_chance"):
                  change_value(message.author.id, "murder_chance", 20)
                if get_value(message.author.id, "is_max_money") == True:
                  change_value(message.author.id, "is_max_money", False)
                if get_value(message.author.id, "murder_chance") == 20:
                  nt = "nt"
                else:
                  nt = ""
                if random.randint(0, 100) > get_value(message.author.id, "murder_chance"):
                  if not get_value(message.author.id, "is_max_money"):
                    money = random.randint(40, 60)
                  else:
                    money = 80
                  change_value(message.author.id, "rep", -10, True)
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="**LOSS**: you tried to murder a random person from server. you did" + nt + " have a weapon, but cops catched you. you payed them " + str(give_money(message.author.id, -money)) + "$ to let you out."))) 
                else:
                  money = random.randint(225, 275)
                  change_value(message.author.id, "rep", -5, True)
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="**GAIN**: you tried to murder a random person from server. you did" + nt + " have a weapon, and managed to kill them uncatched. you got " + str(give_money(message.author.id, money)) + "$ for that.")))
                change_value(message.author.id, "murder_time", time())

            elif text == "heist":
                last_time = get_value(message.author.id, "heist_time")
                try:
                  difference = time() - last_time
                except:
                  difference = 99999
                if difference >= 1800:
                  if get_value(message.author.id, "heist_level"):
                    chance_1, sum_1, chance_2, sum_2 = heist_level(message.author.id)
                    if random.randint(0, 100) < chance_1:
                      change_value(message.author.id, "rep", -30, True)
                      await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="**SMALL GAIN**: you went to local bank and got small portion of possible earnings, or exactly " + str(give_money(message.author.id, sum_1)) + "$. try harder next time ig")))    
                    else:
                      change_value(message.author.id, "rep", -50, True)
                      await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="**BIG GAIN**: you went to bank and totally destroyed it, getting maximum you could have. you got " + str(give_money(message.author.id, sum_2)) + "$ for that.")))
                    change_value(message.author.id, "heist_time", time())
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="sadly you dont have any heist gear, to buy some go to bored heist shop")))
                else:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="there is " + str(round(1800 - difference)) + " seconds left!")))
            
            elif text == "rob":
              await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="who do you want to rob lol")))

            elif text.startswith("rob "):
                last_time = get_value(message.author.id, "rob_time")
                try:
                  difference = time() - last_time
                except:
                  difference = 99999
                if difference >= 60:
                  to_rob = text[6:-1]
                  if to_rob[0] == "!":
                    to_rob = to_rob[1:]
                  if get_value(to_rob, "money") != None:
                    if random.randint(0, 100) > 40:
                      money = random.randint(80, 120)
                      change_value(message.author.id, "rep", -10, True)
                      result = "**LOSS**: you tried to rob <@" + to_rob + ">, but he catched you. you paid him " + str(give_money(to_rob, money, False)) + "$ as a compensation."
                      color = 0xff2D00
                      give_money(message.author.id, -money, False)
                    else:
                      money = random.randint(450, 550)
                      change_value(message.author.id, "rep", -3, True)
                      result = "**GAIN**: you tried to rob <@" + to_rob + ">, and managed to rob them uncatched. you got " + str(give_money(message.author.id, money, False)) + "$ for that."
                      color = 0x00ff00
                      give_money(to_rob, -money, False)
                    embedVar = discord.Embed(title="Rob result:", description=result, color=color).set_author(name="By using this bot you agree to the Terms Of Service and Privacy Policy of it. `bored legal` for more.")
                    await message.reply(embed=add_ad(embedVar))
                    change_value(message.author.id, "rob_time", time())
                  else:
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="idk who it is")))
                else:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="there is " + str(round(60 - difference)) + " seconds left!")))
            
            elif text == "work":
                if worker == False or worker == None:
                  worker = message.author
                if worker == message.author:
                  worker = message.author
                  job = random.randint(0, 5)
                  if job == 0:
                    clicker = await message.reply("CLICKER JOB FOR <@" + str(message.author.id) + ">\n\nclick reaction 10 times for money")
                    await clicker.add_reaction("💰")
                    clicks = 0
                    while clicks != 10:
                      reaction, user = await bot.wait_for('reaction_add')
                      if int(user.id) != 834425748361445406 and int(user.id) != 904047456327729172:
                        await reaction.remove(user)
                      if user == worker:
                        clicks += 1
                    income = random.randint(100, 300)
                    await clicker.clear_reaction("💰")
                    await message.reply("ok good job you got " + str(give_money(worker.id, income)) + "$ gg")
                    worker = False
                    job = False
                    await asyncio.sleep(1)
                    await clicker.clear_reaction("💰")
                    change_value(message.author.id, "rep", 7, True)
                  elif job == 1:
                    sentances = ["give me money for work", "i working hard pay me", "hey can i get my salary", "please gimme my money", "i worked so give cash", "im done with work pay me", "work done give money now"]
                    replacers = {"a": "а", "b": "Ь", "c": "с", "d": "đ", "e": "е", "f": "𝓕", "g": "𝓰", "h": "н", "i": "𝓲", "j": "𝒿", "k": "к", "l": "𝓛", "m": "м", "n": "п", "o": "о", "p": "р", "q": "𝓺", "r": "г", "s": "𝓢", "t": "Т", "u": "и", "v": "𝓥", "w": "𝓦", "x": "х", "y": "у", "z": "𝔃"}
                    sen = random.choice(sentances)
                    res = ""
                    for i in sen:
                      try:
                        res = res + replacers[i]
                      except:
                        res = res + i
                    await message.reply("TYPER JOB FOR <@" + str(message.author.id) + ">\n\ntype following text for money (lowercase): `" + res + "`")
                    req = sen
                  elif job == 2:
                    dos = ["*", "/", "+", "-"]
                    problem = str(random.randint(1, 15)) + random.choice(dos) + str(random.randint(1, 15)) + random.choice(dos) + str(random.randint(1, 15))
                    await message.reply("MATH JOB FOR <@" + str(message.author.id) + ">\n\nsolve this math problem (round if not intenger): `" + problem + "`")
                    req = str(round(eval(problem)))
                  elif job == 3:
                    req = random.randint(0, 100)
                    await message.reply("GUESSER JOB FOR <@" + str(message.author.id) + ">\n\ni thinked of a number. guess it using my hints. you can start by saying 50.")
                  elif job == 4:
                    req = str(random.randint(100000, 999999))
                    memory = await message.reply("MEMORY JOB FOR <@" + str(message.author.id) + ">\n\nremember this number: `" + req + "`")
                    await asyncio.sleep(3)
                    string = "MEMORY JOB FOR <@" + str(message.author.id) + ">\n\nnow, send it to me"
                    await memory.edit(content=string)
                  elif job == 5:
                    try:
                      response = requests.get("https://opentdb.com/api.php?amount=1&type=boolean")
                      result = response.json()
                      req = result["results"][0]["correct_answer"].lower()
                    except:
                      await message.reply("Trivia api got an error, please try again later.")
                    question = result["results"][0]["question"].replace("&amp;", "&").replace("&quot;", '"').replace("&apos;", "'").replace("&gt;", ">").replace("&lt;", "<")
                    await message.reply("TRIVIA JOB FOR <@" + str(message.author.id) + ">\n\nis this true or false: `" + question + "`")
                else:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="im sorry but you cant do work while other person working sorry")))
            
            elif text == "reset":
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="bored cash reset, bored passive reset, bored weapon reset, bored full reset, bored heist reset")))

            if text == "reset cash" or text == "cash reset" or text == "full reset" or text == "reset full":
                change_value(message.author.id, "money", 0)
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="money resetted")))

            if text == "passive reset" or text == "reset passive" or text == "full reset" or text == "reset full":
                change_value(message.author.id, "passive_earnings_balance", 0)
                change_value(message.author.id, "passive_earnings_max", 50)
                change_value(message.author.id, "passive_earnings_time", 0)
                change_value(message.author.id, "passive_earnings_speed", 0)
                change_value(message.author.id, "passive_earnings_speed_cost", 100)
                change_value(message.author.id, "passive_earnings_max_cost", 100)
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="passive resetted")))

            if text == "weapon reset" or text == "reset weapon" or text == "full reset" or text == "reset full":
                change_value(message.author.id, "weaponpass", False)
                change_value(message.author.id, "murder_chance", 20)
                change_value(message.author.id, "is_max_money", False)
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="weapon resetted")))

            if text == "heist reset" or text == "reset heist" or text == "full reset" or text == "reset full":
                change_value(message.author.id, "heistpass", False)
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="heist resetted")))

            if text == "full reset" or text == "reset full":
                change_value(message.author.id, "rob_time", 99999)
                change_value(message.author.id, "daily_time", 99999)
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="cooldowns resetted")))
                change_value(message.author.id, "rep", 0)
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="rep resetted")))
                change_value(message.author.id, "multiplier", 1)
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="multiplier resetted")))
            
            elif text == "outside":
                meet = random.randint(0, 100)
                if meet != 69:
                  income = random.randint(0, 20)
                  change_value(message.author.id, "rep", 1, True)
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you went outside and found "+ str(give_money(message.author.id, income)) + "$ laying on floor, congrats i guess")))
                elif meet == 69:
                  income = random.randint(500, 2000)
                  change_value(message.author.id, "rep", 15, True)
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="you went outside and met putin, he gave you "+ str(give_money(message.author.id, income)) + "$ congrats i guess")))
            
            elif text == 'easter egg':
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="owo how do you get here")))
            
            elif text.startswith('ai '):
                if message.author == bot.user:
                  return
                original = original[3:]
                try:
                  my_secret = os.environ['textgen']
                  r = requests.post("https://api.deepai.org/api/text-generator", data={'text': original,}, headers={'api-key': my_secret})
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description=r.json()["output"])))
                except KeyError:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="Well damn you cant generate stuff on beta version of bot am sorry")))
                except Exception:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="Text generator api got an error, please try again later.")))
            
            elif text == "pi":
                for _ in range(0, 100):
                  if pi_ == 0:
                    pi = pi - (4/pi1)
                    pi_ = 1
                  else:
                    pi = pi + (4/pi1)
                    pi_ = 0
                  pi1 += 2
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description=pi)))
                file = open("pi.json", "w")
                json.dump([str(pi), str(pi1), pi_], file)
                file.close()
            
            elif text == "leave":
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="simon says <@" + str(message.author.id) + "> left game lol")))
                players.remove(message.author)
            
            elif text == "joke":
                try:
                  response = requests.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist")
                  joke = response.json()
                  if joke["type"] == "twopart":
                      await message.reply(joke["setup"])
                      await asyncio.sleep(3)
                      await message.channel.send(joke["delivery"])
                  elif joke["type"] == "single":
                      await message.reply(joke["joke"])
                except:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="Jokes api got an error, please try again later.")))

            elif text == "j0ke":
                try:
                  response = requests.get("https://v2.jokeapi.dev/joke/Any")
                  joke = response.json()
                  if joke["type"] == "twopart":
                      await message.reply(joke["setup"])
                      await asyncio.sleep(3)
                      await message.channel.send(joke["delivery"])
                  elif joke["type"] == "single":
                      await message.reply(joke["joke"])
                except:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="Jokes api got an error, please try again later.")))
            
            elif text == "fact":
                try:
                  response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
                  fact = response.json()
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description=fact["text"])))
                except:
                  await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="Facts api got an error, please try again later.")))
            
            elif text == 'simon make':
                setuper = message.author
                step = 1
                setup = await message.reply("Question setup (1/3):\n\n**What is text of your question?**\n\nThis is what bot will send when round starts.")
                await message.delete()

            elif text[:10] == 'simon says' and not simon_active:
                lenght = text[11:]
                if not lenght:
                    lenght = "10"
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="starting simon says game with "+lenght+" rounds in 3 seconds... 15 seconds per round")))
                channel_check = message.channel
                simon_active = True
                await asyncio.sleep(3)
                for _ in range(0, int(lenght)):
                    a, b = random.choice(list(simon_says.items()))
                    await message.channel.send(a)
                    await asyncio.sleep(15)
                    if state:
                        failed += list(set(players) - set(passed_))
                    failed = list(set(failed))
                    if len(failed) == 0:
                        failed_ = "no one failed"
                    else:
                        failed_ = "<@"+">, <@".join(failed)+">"
                    await message.channel.send(embed=add_ad(discord.Embed(color=0x00ff00, description="simon says following failed: "+failed_+". "+str(len(failed))+" peeps in total.")))
                    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='bored help'))
                    failed = []
                    passed_ = []
                    await asyncio.sleep(2)
                await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="simon says game end nice job!!!!1!")))
                simon_active = False
                players = []

            elif text == "uno" and 2 == 3:
                uno = await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="kk uno then ig. to enter game react to this message with :black_joker:, staring in 60 (15 for now for testing purposes) seconds if more than 1 person reacts.")))
                await uno.add_reaction("🃏")
                players_ = []
                players_list = []
                terminated = False

                async def collect():
                  global bot
                  while True:
                    reaction, user = await bot.wait_for('reaction_add', timeout=60.0)
                    players_.append(user)
                    players_list.append("<@" + str(user.id) + ">")
                
                task = asyncio.create_task(collect())
                await asyncio.sleep(15)
                task.cancel()
                
                await uno.clear_reaction("🃏")

                try:
                  yuuu = players_list.index("<@904047456327729172>")
                  players_list.pop(yuuu)
                  players_.pop(yuuu)
                except:
                  pass

                try:
                  yuuu = players_list.index("<@834425748361445406>")
                  players_list.pop(yuuu)
                  players_.pop(yuuu)
                except:
                  pass
                
                if len(players_list) > 15:
                  await uno.edit(content=add_ad(discord.Embed(color=0x00ff00, description="ok im very sorry but i just dont have enough of cards for everyone of you. my limit is 15 players.")))
                elif len(players_list) > 1:
                  await uno.edit(content=add_ad(discord.Embed(color=0x00ff00, description="ok game is starting with following peeps entered: " + ", ".join(players_list) + ". check your dms to start")))
                  dms = []
                  
                  for player in players_:
                    dm_me = bot.get_user(player.id)

                    try:
                      await dm_me.send(embed=add_ad(discord.Embed(color=0x00ff00, description="**Controls**: I will show you list of your cards, to throw card, say me number of it when it is your turn,\n" +
                      "`draw` to draw card from deck\n`uno` to uno someone else\n`1uno` or `2uno` to throw card 1 or card 2 in " +
                      "uno mode")))

                      dms.append([dm_me, player])
                    except Exception:
                      await message.channel.send(embed=add_ad(discord.Embed(color=0x00ff00, description="so bruh <@" + str(player.id) + "> has their dms disabled, he is not playing with you ig")))
                      yuuu = players_.index(player)
                      players_list.pop(yuuu)
                      players_.pop(yuuu)

                  game_alive = True

                  numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "🔄", "🚫", "+2"]
                  blacks = ["+4⬛", "⬛"]
                  colors = ["🟥", "🟨", "🟩", "🟦"]

                  cards_list = []
                  for i in colors:
                    for j in numbers:
                      cards_list.append(j + i)
                      cards_list.append(j + i)
                    cards_list.append("0" + i)
                  for i in blacks:
                    cards_list.append(i)
                    cards_list.append(i)
                    cards_list.append(i)
                    cards_list.append(i)

                  cards_list, current_card = give_card(1, cards_list)

                  turn = 0
                  save_turn = -1
                  direction = 1
                  cards_s = []

                  for i in players_list:
                    cards_list, cards_s.append(give_card(7, cards_list))

                  render_card = math.ceil(len(players_list) / 2) - 1

                  while game_alive:
                    await asyncio.sleep(1)
                    if save_turn != turn:
                      cards_left = len(cards_list)
                      gen_turn = ""
                      save_turn = turn

                      for i in range(0, len(players_list)):
                        card_suffix = ""
                        turn_prefix = ""
                        if i == render_card:
                          card_suffix = "              Current card: " + current_card
                        if i == turn % len(players_list):
                          turn_prefix = " ⬅️"
                        gen_turn = gen_turn + str(len(cards_s[i])) + " - " + players_list[i] + turn_prefix + card_suffix + "\n"

                      direction_emoji = "⬇️"
                      if direction == -1:
                        direction_emoji = "⬆️"
                      gen_turn = gen_turn + "\n*Direction*: " + direction_emoji + "\n*Cards in deck*: " + str(cards_left) + "\n\n**Your cards**:\n"

                      for value_ in dms:
                        dm_me, player = value_
                        inv = ""
                        my_order = players_.index(player)
                        
                        try:
                          for num, i in enumerate(cards_s[my_order]):
                            inv = inv + "*" + str(num + 1) + "* - " + i + "\n"
                        except Exception:
                            inv = "Empty\n"
                        
                        if turn % len(players_list) == my_order:
                          if len(cards_s[turn % len(players_list)]) == 0:
                            game_alive = False
                          inv = inv + "\n**IT'S YOUR TURN NOW!!!!**"
                        await dm_me.send(gen_turn + inv)

                  for value_ in dms:
                    dm_me, player = value_
                    await dm_me.send(embed=add_ad(discord.Embed(color=0x00ff00, description="GG game ended. Check main channel for winner.")))
                  await uno.edit(embed=add_ad(discord.Embed(color=0x00ff00, description="GG game ended. And winner was... " + players_list[turns % len(players_list)] + "! Congrats bruh lmao lel kekw.")))
                
                elif len(players_list) == 1:
                  await uno.edit(embed=add_ad(discord.Embed(color=0x00ff00, description=", ".join(players_list) + " dude imagine having no friends to play with lmao. 1 person entered, game didnt start.")))
                else:
                  await uno.edit(embed=add_ad(discord.Embed(color=0x00ff00, description="ok imagine staring uno game yourself but then not playing it lmao kekw. 0 people entered, game didnt start.")))
            
            elif text[:3] == "ttt" and not ttt_active:
                active_ai = False
                if text == "ttt":
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="Choose player you want to play with using: bored ttt @user\nOR\nenter \"bored ttt ai\" to play with ai")))
                    return
                if text == "ttt ai":
                    await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="Choose difficulty:\nbored ttt easy\nbored ttt normal\nbored ttt impossible")))
                    return
                if text == "ttt impossible" or text == "ttt normal" or text == "ttt easy":
                    active_ai = text[4:]
                    user1 = bot.user
                user2 = message.author
                if not active_ai:
                    try:
                        user1 = bot.get_user(int(text[7:-1]))
                    except:
                        await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="Wdym (Error: User not found)")))
                        return
                    if user1 == user2:
                        await message.reply(embed=add_ad(discord.Embed(color=0x00ff00, description="I don't think you wanna play with yourself.")))
                        return
                ttt = [['▪', '▪', '▪'],
                        ['▪', '▪', '▪'],
                        ['▪', '▪', '▪']]
                reactions = ["", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
                place_to = tie = is_middle = False
                if active_ai == "impossible":
                    ttt[2][0] = "X"
                    turn = user2
                    move = 1
                else:
                    turn = user1
                    move = 0
                game = await message.reply("Loading game.... <@" + str(user1.id) + "> VS <@" + str(user2.id) + ">.")
                for i in reactions[1:]:
                    await game.add_reaction(i)
                await game.edit(content="Battle start. <@" + str(user1.id) + "> VS <@" + str(user2.id) + ">.\n" +
                    "```\n " +
                    ttt[0][0] + "▐ " + ttt[0][1]+"▐ " + ttt[0][2] + "\n▬▬▬▬▬▬▬▬▬\n " +
                    ttt[1][0] + "▐ " + ttt[1][1]+"▐ " + ttt[1][2] + "\n▬▬▬▬▬▬▬▬▬\n " +
                    ttt[2][0] + "▐ " + ttt[2][1]+"▐ " + ttt[2][2] + "\n" +
                    "```\n" +
                    "It is <@" + str(turn.id) + "> turn.")
                while not (ttt[0][0] == ttt[0][1] == ttt[0][2] != '▪' or ttt[1][0] == ttt[1][1] == ttt[1][2] != '▪' or ttt[2][0] == ttt[2][1] == ttt[2][2] != '▪' or ttt[0][0] == ttt[1][0] == ttt[2][0] != '▪' or ttt[0][1] == ttt[1][1] == ttt[2][1] != '▪' or ttt[0][2] == ttt[1][2] == ttt[2][2] != '▪' or  ttt[0][0] == ttt[1][1] == ttt[2][2] != '▪' or ttt[0][2] == ttt[1][1] == ttt[2][0] != '▪' or (ttt[0][0] != '▪' and ttt[0][1] != '▪' and ttt[0][2] != '▪' and ttt[1][0] != '▪' and ttt[1][1] != '▪' and ttt[1][2] != '▪' and ttt[2][0] != '▪' and ttt[2][1] != '▪' and ttt[2][2] != '▪')):
                    if active_ai and turn == user1:
                        if active_ai == "impossible":
                            if move == 1:
                                if ttt[1][0] == "O" or ttt[0][0] == "O" or ttt[1][2] == "O":
                                    ttt[2][2] = "X"
                                elif ttt[2][1] == "O" or ttt[2][2] == "O" or ttt[0][1] == "O" or ttt[0][2] == "O":
                                    ttt[0][0] = "X"
                                elif ttt[1][1] == "O":
                                    ttt[0][2] = "X"
                                    is_middle = True

                                if ttt[1][0] == "O" or ttt[2][1] == "O" or ttt[0][0] == "O" or ttt[2][2] == "O":
                                    place_to = 2
                                elif ttt[1][2] == "O":
                                    place_to = 1
                                elif ttt[0][1] == "O" or ttt[0][2] == "O":
                                    place_to = 3
                            elif move == 2 and is_middle:
                                if ttt[0][0] == "O":
                                    ttt[2][2] = "X"
                                elif ttt[2][2] == "O":
                                    ttt[0][0] = "X"
                                else:
                                    active_ai = "normal"
                                    if ttt[0][1] == "O":
                                        ttt[2][1] = "X"
                                    elif ttt[2][1] == "O":
                                        ttt[0][1] = "X"
                                    elif ttt[1][0] == "O":
                                        ttt[1][2] = "X"
                                    elif ttt[1][2] == "O":
                                        ttt[1][0] = "X"
                            elif move == 2 and not is_middle:
                                if ttt[2][2] == "X" and ttt[0][0] == "X" and ttt[2][1] != "O":
                                    ttt[2][1] = "X"
                                elif ttt[0][0] == "X" and ttt[0][0] == "X" and ttt[1][0] != "O":
                                    ttt[1][0] = "X"
                                elif ttt[2][2] == "X" and ttt[0][2] == "X" and ttt[1][2] != "O":
                                    ttt[1][2] = "X"
                                elif ttt[0][0] == "X" and ttt[0][2] == "X" and ttt[0][1] != "O":
                                    ttt[0][1] = "X"
                                else:
                                    if place_to == 1:
                                        ttt[0][0] = "X"
                                    elif place_to == 2:
                                        ttt[0][2] = "X"
                                    elif place_to == 3:
                                        ttt[2][2] = "X"
                            elif move == 3:
                                if ttt[1][1] != "O":
                                    ttt[1][1] = "X"
                                else:
                                    if ttt[2][2] == "X" and ttt[0][0] == "X" and ttt[2][1] != "O":
                                        ttt[2][1] = "X"
                                    elif ttt[0][0] == "X" and ttt[0][0] == "X" and ttt[1][0] != "O":
                                        ttt[1][0] = "X"
                                    elif ttt[2][2] == "X" and ttt[0][2] == "X" and ttt[1][2] != "O":
                                        ttt[1][2] = "X"
                                    elif ttt[0][0] == "X" and ttt[0][2] == "X" and ttt[0][1] != "O":
                                        ttt[0][1] = "X"
                        if active_ai == "normal":
                            if ttt[2][2] == "O" and ttt[0][0] == "O" and ttt[2][1] == "▪":
                                ttt[2][1] = "X"
                            elif ttt[0][0] == "O" and ttt[0][0] == "O" and ttt[1][0] == "▪":
                                ttt[1][0] = "X"
                            elif ttt[2][2] == "O" and ttt[0][2] == "O" and ttt[1][2] == "▪":
                                ttt[1][2] = "X"
                            elif ttt[0][0] == "O" and ttt[0][2] == "O" and ttt[0][1] == "▪":
                                ttt[0][1] = "X"
                            elif ttt[0][0] == "O" and ttt[0][1] == "O" and ttt[0][2] == "▪":
                                ttt[0][2] = "X"
                            elif ttt[1][0] == "O" and ttt[1][1] == "O" and ttt[1][2] == "▪":
                                ttt[1][2] = "X"
                            elif ttt[2][0] == "O" and ttt[2][1] == "O" and ttt[2][2] == "▪":
                                ttt[2][2] = "X"
                            elif ttt[0][2] == "O" and ttt[0][1] == "O" and ttt[0][0] == "▪":
                                ttt[0][0] = "X"
                            elif ttt[1][2] == "O" and ttt[1][1] == "O" and ttt[1][0] == "▪":
                                ttt[1][0] = "X"
                            elif ttt[2][2] == "O" and ttt[2][1] == "O" and ttt[2][0] == "▪":
                                ttt[2][0] = "X"
                            elif ttt[1][0] == "O" and ttt[1][2] == "O" and ttt[1][1] == "▪":
                                ttt[1][1] = "X"
                            elif ttt[2][2] == "O" and ttt[1][2] == "O" and ttt[0][2] == "▪":
                                ttt[0][2] = "X"
                            elif ttt[2][1] == "O" and ttt[1][1] == "O" and ttt[0][1] == "▪":
                                ttt[0][1] = "X"
                            elif ttt[2][0] == "O" and ttt[1][0] == "O" and ttt[0][0] == "▪":
                                ttt[0][0] = "X"
                            elif ttt[0][1] == "O" and ttt[2][1] == "O" and ttt[1][1] == "▪":
                                ttt[1][1] = "X"
                            elif ttt[0][2] == "O" and ttt[1][2] == "O" and ttt[2][2] == "▪":
                                ttt[2][2] = "X"
                            elif ttt[0][1] == "O" and ttt[1][1] == "O" and ttt[2][1] == "▪":
                                ttt[2][1] = "X"
                            elif ttt[0][0] == "O" and ttt[1][0] == "O" and ttt[2][0] == "▪":
                                ttt[2][0] = "X"
                            elif ttt[0][0] == "O" and ttt[1][1] == "O" and ttt[2][2] == "▪":
                                ttt[2][2] = "X"
                            elif ttt[2][2] == "O" and ttt[1][1] == "O" and ttt[0][0] == "▪":
                                ttt[0][0] = "X"
                            elif ttt[2][2] == "O" and ttt[0][0] == "O" and ttt[1][1] == "▪":
                                ttt[1][1] = "X"
                            elif ttt[0][2] == "O" and ttt[1][1] == "O" and ttt[2][0] == "▪":
                                ttt[2][0] = "X"
                            elif ttt[2][0] == "O" and ttt[1][1] == "O" and ttt[0][2] == "▪":
                                ttt[0][2] = "X"
                            elif ttt[2][0] == "O" and ttt[0][2] == "O" and ttt[1][1] == "▪":
                                ttt[1][1] = "X"
                            else:
                                gen_a = random.randint(0, 2)
                                gen_b = random.randint(0, 2)
                                while ttt[gen_a][gen_b] != "▪":
                                    gen_a = random.randint(0, 2)
                                    gen_b = random.randint(0, 2)
                                ttt[gen_a][gen_b] = "X"
                        if active_ai == "easy":
                            gen_a = random.randint(0, 2)
                            gen_b = random.randint(0, 2)
                            while ttt[gen_a][gen_b] != "▪":
                                gen_a = random.randint(0, 2)
                                gen_b = random.randint(0, 2)
                            ttt[gen_a][gen_b] = "X"

                        turn = user2
                        move += 1
                    else:
                        reaction, user = await bot.wait_for('reaction_add')
                        if user == turn:
                            stop = False
                            try:
                                z = reactions.index(reaction.emoji)
                            except:
                                stop = True
                            if not stop:
                                x = (z - 1) % 3
                                y = (z - 1) // 3
                                if ttt[y][x] == '▪':
                                    if turn == user1:
                                        ttt[y][x] = "X"
                                        turn = user2
                                    else:
                                        ttt[y][x] = "O"
                                        turn = user1
                        await reaction.remove(user)
                    await game.edit(content="Battle start. <@" + str(user1.id) + "> VS <@" + str(user2.id) + ">.\n" +
                    "```\n " +
                    ttt[0][0] + "▐ " + ttt[0][1]+"▐ " + ttt[0][2] + "\n▬▬▬▬▬▬▬▬▬\n " +
                    ttt[1][0] + "▐ " + ttt[1][1]+"▐ " + ttt[1][2] + "\n▬▬▬▬▬▬▬▬▬\n " +
                    ttt[2][0] + "▐ " + ttt[2][1]+"▐ " + ttt[2][2] + "\n" +
                    "```\n" +
                    "It is <@" + str(turn.id) + "> turn.")
                if ttt[0][0] == ttt[0][1] == ttt[0][2] != '▪' or ttt[1][0] == ttt[1][1] == ttt[1][2] != '▪' or ttt[2][0] == ttt[2][1] == ttt[2][2] != '▪' or ttt[0][0] == ttt[1][0] == ttt[2][0] != '▪' or ttt[0][1] == ttt[1][1] == ttt[2][1] != '▪' or ttt[0][2] == ttt[1][2] == ttt[2][2] != '▪' or  ttt[0][0] == ttt[1][1] == ttt[2][2] != '▪' or ttt[0][2] == ttt[1][1] == ttt[2][0] != '▪':
                    if turn == user1:
                        winner = user2
                        winner_symbol = "O"
                    else:
                        winner = user1
                        winner_symbol = "X"
                elif not tie:
                    await game.edit(content="Game ended. It was tie.\n```\n " +
                    ttt[0][0] + "▐ " + ttt[0][1]+"▐ " + ttt[0][2] + "\n▬▬▬▬▬▬▬▬▬\n " +
                    ttt[1][0] + "▐ " + ttt[1][1]+"▐ " + ttt[1][2] + "\n▬▬▬▬▬▬▬▬▬\n " +
                    ttt[2][0] + "▐ " + ttt[2][1]+"▐ " + ttt[2][2] + "\n" +
                    "```")
                    winner = winner_symbol = False

                if winner:
                    await game.edit(content="Game ended. <@" + str(winner.id) +"> won as " + winner_symbol + ".\n```\n " +
                    ttt[0][0] + "▐ " + ttt[0][1]+"▐ " + ttt[0][2] + "\n▬▬▬▬▬▬▬▬▬\n " +
                    ttt[1][0] + "▐ " + ttt[1][1]+"▐ " + ttt[1][2] + "\n▬▬▬▬▬▬▬▬▬\n " +
                    ttt[2][0] + "▐ " + ttt[2][1]+"▐ " + ttt[2][2] + "\n" +
                    "```")
                    
                for i in reactions[1:]:
                    await game.clear_reaction(i)

                ttt_active = False
        
        if simon_active and message.channel == channel_check and (int(message.author.id) != 834425748361445406 and int(user.id) != 904047456327729172):
            players.append(str(message.author.id))
            players = list(set(players))
            if b[0] == "5854731":
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='5854731'))
            if isinstance(b, list):
                if b[0] != 0:
                    state = True
                    for i in b:
                        if i in text.lower():
                            passed_.append(str(message.author.id))
                            break
                else:
                    state = False
                    for i in b[1:]:
                        if i in text.lower():
                            failed.append(str(message.author.id))
                            break
            elif b == "1":
                state = False
                failed.append(str(message.author.id))
            else:
                state = False
    except discord.errors.HTTPException as e:
        print(str(traceback.format_exc()))
        await message.channel.send(embed=add_ad(discord.Embed(color=0x00ff00, description="So basiclly message is over 2000 symbols so i have no clue what is happening, command maybe ran maybe it crashed idk not my fault")))
    except Exception as e:
        await message.reply(embed=add_ad(discord.Embed(color=0xff0000, title="There is an error happend", description=str(traceback.format_exc()))))
        try:
          milenakoos = bot.get_user(553093932012011520)
          
          try:
            msg = message
            print(message)
          except Exception as e:
            msg = "Error getting"
          
          try:
            link = "https://discord.com/channels/" + str(message.guild.id) + "/" + str(message.channel.id) + "/" + str(message.id)
            print(link)
          except Exception as e:
            link = "Error getting"
          
          try:
            cont = message.content
            print(cont)
          except Exception as e:
            cont = "Error getting"
          
          await milenakoos.send("There is an error happend:\n" + str(traceback.format_exc()) + "\n\nMore info on error:\n\nMessage: " + str(msg) + "\n\nMessage link: " + link + "\n\nMessage text: " + cont)
        except Exception as e:
          await message.reply(embed=add_ad(discord.Embed(color=0xff0000, title="There is an error happend in error handler (note: this is not good)", description=str(traceback.format_exc()))))

if not is_beta:
  my_secret = os.environ['token']
  keep_alive.keep_alive()
  bot.run(my_secret)
else:
  bot.run(token_getter.token())
