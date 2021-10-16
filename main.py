import asyncio, requests, random, discord, os
from discord.utils import get
from discord.ext import commands
from time import sleep

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='bored ', intents=intents)

async def generate(queston_body, question_type, setuper, question_contents=None):
    milenakos = bot.get_user(553093932012011520)
    if question_contents:
        if question_type == "3":
            question_contents.insert(0, 0)
        second_part = str(question_contents)
    else:
        second_part = question_type
    await milenakos.send("<@" + str(setuper.id) + "> suggested:\n\"" + queston_body + "\": " + second_part + ",")

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
              "Critical Error: list index out of range (list simon_says)\nContinue anyway?": [0, "yes"],
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
failed = []
players = []
passed_ = []
question_contents = []
state = False
setuper = question_type = queston_body = step = None

@bot.event
async def on_message(message):
    original = message.content
    text = original.lower()
    global ttt_active
    global simon_active
    global channel_check
    global b
    global failed
    global state
    global players
    global passed_
    global question_type, queston_body, question_contents, step, setup, setuper
    try:
        if message.author == setuper:
            if step == 1:
                queston_body = text
                await message.delete()
                await setup.edit(content="Question setup (2/3):\n\n**What is type of your question?**\n\n0 - No eleminations." +
                    "\n1 - Eliminate everyone who chat.\n2 - Eleminate everyone who DIDNT said specific thing." +
                    "\n3 - Eleminate everyone who DID said specific thing.")
                step += 1
            elif step == 2:
                if not (text == "0" or text == "1" or text == "2" or text == "3"):
                    return
                question_type = text
                await message.delete()
                if text == "0" or text == "1":
                    await setup.edit(content="Got it! Setup was finished and question was submitted!")
                    await generate(queston_body, question_type, setuper)
                    setuper = question_type = queston_body = None
                    question_contents = []
                    await asyncio.sleep(10)
                    await setup.delete()
                else:
                    await setup.edit(content="Question setup (3/3):\n\n**What is contents of your question?**\n\nWhat is \"specific thing\"?" +
                        "\n(each message will be interpreted as serperate thing; type \"finish\" to exit.)")
                    step += 1
            elif step == 3:
                await message.delete()
                if text == "finish":
                    await setup.edit(content="Got it! Setup was finished and question was submitted!")
                    await generate(queston_body, question_type, setuper, question_contents)
                    setuper = question_type = queston_body = None
                    question_contents = []
                    await asyncio.sleep(10)
                    await setup.delete()
                else:
                    question_contents.append(text)
        if text == "bored leave":
            await message.channel.send("simon says <@" + str(message.author.id) + "> left game lol")
            players.remove(message.author)
        if text.startswith('?nuke'):
            await message.channel.send("CARL-BOT: NUKE ACTIVATED")
            await asyncio.sleep(2)
            await message.channel.send("NUKING USER " + text[6:] + "...")
            await asyncio.sleep(3)
            await message.channel.send("NUKE SENT SUCCESSFULLY")
            await asyncio.sleep(10)
            user1 = bot.get_user(int(text[9:-1]))
            for _ in range(0, 20):
                await user1.send(random.choice(["YOU GOT NUKED!!! KABOOM!!!", "BOOOM!! NUKE EXPLODED YOU!", "YOUR HOUSE WAS JUST BLOWN UP BY NUKE!!!", "BOOM BOOOM!! KAPOW!!!"]))
        if text == "nuke me":
            await message.channel.send("CARL-BOT: NUKE ACTIVATED")
            await message.channel.send("NUKING USER <@" + str(message.author.id) + ">...")
            await message.channel.send("NUKE SENT SUCCESSFULLY")
            user1 = message.author
            while True:
                await user1.send(random.choice(["YOU GOT NUKED!!! KABOOM!!!", "BOOOM!! NUKE EXPLODED YOU!", "YOUR HOUSE WAS JUST BLOWN UP BY NUKE!!!", "BOOM BOOOM!! KAPOW!!!"]))
        if text.startswith('bored '):
            text = text[6:]
            original = original[6:]
            if text == 'help':
                await message.channel.send("Help: 'bored simon says', 'bored ai <text>', bored ttt', 'bored leave', 'bored simon make', 'bored joke', 'bored fact")
            elif text == 'easter egg':
                await message.channel.send("owo how do you get here")
            elif text.startswith('ai '):
                original = original[3:]
                r = requests.post("https://api.deepai.org/api/text-generator", data={'text': original,}, headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'})
                await message.channel.send(r.json()["output"])
            elif text == "leave":
                await message.channel.send("simon says <@" + str(message.author.id) + "> left game lol")
                players.remove(message.author)
            elif text == "joke":
                response = requests.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist")
                joke = response.json()
                if joke["type"] == "twopart":
                    await message.channel.send(joke["setup"])
                    await asyncio.sleep(3)
                    await message.channel.send(joke["delivery"])
                elif joke["type"] == "single":
                    await message.channel.send(joke["joke"])
            elif text == "fact":
                response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
                fact = response.json()
                await message.channel.send(fact["text"])
            elif text == 'simon make':
                setuper = message.author
                step = 1
                await message.delete()
                setup = await message.channel.send("Question setup (1/3):\n\n**What is text of your question?**\n\nThis is what bot will send when round starts.")
            elif text[:10] == 'simon says' and not simon_active:
                lenght = text[11:]
                if not lenght:
                    lenght = "10"
                await message.channel.send("starting simon says game with "+lenght+" rounds in 3 seconds... 15 seconds per round")
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
                    await message.channel.send("simon says following failed: "+failed_+". "+str(len(failed))+" peeps in total.")
                    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='bored help'))
                    failed = []
                    passed_ = []
                    await asyncio.sleep(2)
                await message.channel.send("simon says game end nice job!!!!1!")
                simon_active = False
                players = []
            elif text[:3] == "ttt" and not ttt_active:
                active_ai = False
                if text == "ttt":
                    await message.channel.send("Choose player you want to play with using: bored ttt @user\nOR\nenter \"bored ttt ai\" to play with ai")
                    return
                if text == "ttt ai":
                    await message.channel.send("Choose difficulty:\nbored ttt easy\nbored ttt normal\nbored ttt impossible")
                    return
                if text == "ttt impossible" or text == "ttt normal" or text == "ttt easy":
                    active_ai = text[4:]
                    user1 = bot.user
                user2 = message.author
                if not active_ai:
                    try:
                        user1 = bot.get_user(int(text[7:-1]))
                    except:
                        await message.channel.send("Wdym (Error: User not found)")
                        return
                    if user1.bot:
                        await message.channel.send("I don't think you wanna play with bot.")
                        return
                    elif user1 == user2:
                        await message.channel.send("I don't think you wanna play with yourself.")
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
                game = await message.channel.send("Loading game.... <@" + str(user1.id) + "> VS <@" + str(user2.id) + ">.")
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

        if simon_active and message.channel == channel_check and int(message.author.id) != 834425748361445406:
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
    except Exception as e:
        await message.channel.send("There is an error happend: " + str(e))

my_secret = os.environ['token']
bot.run(my_secret)