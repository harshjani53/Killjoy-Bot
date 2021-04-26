import discord
from discord.ext import commands
import requests
import json
import pyjokes
import wikipedia
import server
from datetime import datetime
import pytz
import random

user = commands.Bot(command_prefix="!")


def fetch_time():
    IST = pytz.timezone('Asia/Kolkata')
    now = datetime.now(IST)
    return now


def time_no():
    timeX = fetch_time()
    return timeX.strftime('%H:%M:%S')


def ret_quote_from_api():
    respond = requests.get("https://zenquotes.io/api/random")
    data = json.loads(respond.text)
    fetch_quote = data[0]['q']
    return fetch_quote


@user.command()
async def time(context):
    await context.channel.purge(limit=1)
    tN = time_no()
    embed = discord.Embed(
        title=f"{context.author.name}, the time is " + tN,
        color=discord.Color.random()
    )
    msg = await context.send(embed=embed)
    await msg.add_reaction("🕰️")


@user.command()
async def quote(context):
    await context.channel.purge(limit=1)
    ret_quote = ret_quote_from_api()
    embed = discord.Embed(
        title="Quote: " + ret_quote,
        color=discord.Color.random()
    )
    msg = await context.send(embed=embed)
    await msg.add_reaction("💯")
    await msg.add_reaction("🔥")


@user.command()
async def joke(context):
    await context.channel.purge(limit=1)
    fetch_joke = pyjokes.get_joke(language='en', category='all')
    embed = discord.Embed(
        title="Joke: " + fetch_joke,
        color=discord.Color.random()
    )
    msg = await context.send(embed=embed)
    await msg.add_reaction("😑")
    await msg.add_reaction("😂")


@user.command()
async def server_info(context):
    await context.channel.purge(limit=1)
    name = str(context.guild.name)
    description = str(context.guild.description)
    id = str(context.guild.id)
    region = str(context.guild.region)
    count = str(context.guild.member_count)
    icon = str(context.guild.icon_url)
    embed = discord.Embed(
        title="Server: " + name,
        description="Description: " + description,
        color=discord.Color.random()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Server Id:", value=id, inline=True)
    embed.add_field(name="Region:", value=region, inline=False)
    embed.add_field(name="Total Members:", value=count, inline=False)

    msg = await context.send(embed=embed)
    await msg.add_reaction("💬")


@user.command()
async def greet(context):
    await context.channel.purge(limit=1)
    greet_time = fetch_time()
    if 0 <= greet_time.hour < 6:
        await context.send("Good Night" + f" {context.author.name}")
    if 6 <= greet_time.hour < 12:
        await context.send("Good Morning" + f" {context.author.name}")
    if 12 <= greet_time.hour < 16:
        await context.send("Good Afternoon" + f" {context.author.name}")
    if 16 <= greet_time.hour < 20:
        await context.send("Good Evening" + f" {context.author.name}")
    if 20 <= greet_time.hour < 23 and 0 <= greet_time.minute < 59:
        await context.send("Good Night" + f" {context.author.name}")


@user.command()
async def ser(context, *args):
    inp_str = ''
    for arg in args:
        inp_str += arg + " "

    res = wikipedia.summary(inp_str, sentences=2)
    await context.send(res)


@user.command()
async def info(context):
    await context.channel.purge(limit=1)
    bot_command = "!info to find killjoy commands"
    greetInfo = "Greets You"
    quoteInfo = "Tells a Quote"
    timeInfo = "Tells Current Time"
    jokeInfo = "Tells a Joke(Mostly Lame)"
    serverInfo = "Tells information about Server"
    gameInfo = "Play a Game, from TicTacToe and RockPaperScissors"
    searchInfo = "Search the string you have provided after !ser, Highly Unstable"
    embed = discord.Embed(
        title="KILLJOY",
        colour=discord.Color.random()
    )
    embed.add_field(name="Commands", value=bot_command, inline=True)
    embed.add_field(name="!greet:- ", value=greetInfo, inline=False)
    embed.add_field(name="!quote:- ", value=quoteInfo, inline=False)
    embed.add_field(name="!time:- ", value=timeInfo, inline=False)
    embed.add_field(name="!joke:- ", value=jokeInfo, inline=False)
    embed.add_field(name="!server_info:- ", value=serverInfo, inline=False)
    embed.add_field(name="!game:-   ", value=gameInfo, inline=False)
    embed.add_field(name="!ser () :-  ", value=searchInfo, inline=False)

    msg = await context.send(embed=embed)
    await msg.add_reaction("💬")


@user.command()
async def game(context):
    await playGame(context, user)


nothing = "BLANK"
one = 0
two = 1
three = 2
four = 3
five = 4
six = 5
seven = 6
eight = 7
nine = 8
reactList = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "❗"]


async def playGame(context, bot):
    embed = discord.Embed(
        title="Please choose a game!",
        description="1: TicTacToe \n 2: RockPaperScissors"
    )
    await context.channel.purge(limit=1)
    msg = await context.send(embed=embed)

    await msg.add_reaction('1️⃣')
    await msg.add_reaction('2️⃣')

    def checkReaction(reaction, user):
        return user != bot.user and (str(reaction.emoji) == '1️⃣' or str(reaction.emoji) == '2️⃣')

    reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=checkReaction)
    if str(reaction.emoji) == '1️⃣':
        await ticTacToe(context, bot)
        pass
    elif str(reaction.emoji) == '2️⃣':
        await rockPaperScissors(context, bot)
        pass


async def rockPaperScissors(context, bot):
    emojiList = ["🧱", "📜", "✂"]

    def ifUser(reaction, user):
        return user != bot.user

    choice = await getUserCharForRPS(context, bot)
    await context.channel.purge(limit=2)
    index = random.randint(0, len(emojiList) - 1)
    bot_choice = emojiList[index]
    await context.send(f"{context.author.name}'s Choice--> " + choice + " " + bot_choice + " <-- Killjoy's Choice")
    if choice == bot_choice:
        await context.send("Tie, GG")
    if choice != bot_choice:
        if choice == "🧱":
            if bot_choice == "📜":
                await context.send("Killjoy Wins")
            else:
                await context.send("You Win")
        elif choice == "📜":
            if bot_choice == "✂":
                await context.send("Killjoy Wins")
            else:
                await context.send("You Win")
        elif choice == "✂":
            if bot_choice == "🧱":
                await context.send("Killjoy Wins")
            else:
                await context.send("You Win")
    msg = await context.send("Would you like to Play again??")
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")
    reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=ifUser)
    if str(reaction.emoji) == "✅":
        await context.channel.purge(limit=3)
        await rockPaperScissors(context, bot)
    else:
        await context.channel.purge(limit=3)
        return


async def ticTacToe(context, bot):
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "❗"]
    board = [nothing, nothing, nothing,
             nothing, nothing, nothing,
             nothing, nothing, nothing]

    currentPlayer = 2
    player_1 = await getUserCharForTTT(context, bot, currentPlayer - 1)
    player_2 = await getUserCharForTTT(context, bot, currentPlayer)

    await context.channel.purge(limit=3)

    def checkNotBot(reaction, user):
        return user != bot.user

    turn = 1
    while checkWin(player_1, player_2, board) == nothing and turn <= 9:
        await context.send(f"Player {currentPlayer % 2 + 1}'s turn")
        msg = await context.send(printBoard(player_1, player_2, board))
        for i in range(len(emojis)):
            await msg.add_reaction(emojis[i])

        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=checkNotBot)
        if user is None or reaction is None:
            await context.channel.purge(limit=1)
            await context.send("Session Timed out")

        print(str(reaction.emoji))

        if str(reaction.emoji) == "❗":
            print("Closed")
            turn = 100
            await context.channel.purge(limit=2)

        else:
            if currentPlayer % 2 == 0:
                makeMove(reaction.emoji, emojis, player_1, board)
            else:
                makeMove(reaction.emoji, emojis, player_2, board)

            await context.channel.purge(limit=2)

        winner = checkWin(player_1, player_2, board)
        if winner != nothing:
            await context.send(f"Player {currentPlayer % 2 + 1} won!\n Would you like to play again?")
            msg = await context.send(printBoard(player_1, player_2, board))
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=checkNotBot)
            if str(reaction.emoji) == "✅":
                emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "❗"]
                board = [nothing, nothing, nothing,
                         nothing, nothing, nothing,
                         nothing, nothing, nothing]
                turn = 0
                currentPlayer = 1
                await context.channel.purge(limit=2)
            else:
                await context.channel.purge(limit=2)
                await context.send("GG!!")

        elif turn >= 9:
            await context.send("Its a tie!\nWould you like to play again?")
            msg = await context.send(printBoard(player_1, player_2, board))
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=checkNotBot)

            if str(reaction.emoji) == "✅":
                emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "❗"]
                board = [nothing, nothing, nothing,
                         nothing, nothing, nothing,
                         nothing, nothing, nothing]
                turn = 0
                currentPlayer = 1
                await context.channel.purge(limit=2)
            else:
                await context.channel.purge(limit=2)
                await context.send("GG!!")

        currentPlayer += 1
        turn += 1


def makeMove(emoji, emojiList, player, board):
    for index in range(len(reactList)):
        if reactList[index] == emoji:
            board[index] = player
            emojiList.remove(emoji)
            break


def checkWin(player1, player2, board):
    lineHOne = checkDirection(one, two, three, player1, player2, board)
    if lineHOne != nothing:
        return lineHOne
    lineHTwo = checkDirection(four, five, six, player1, player2, board)
    if lineHTwo != nothing:
        return lineHTwo
    lineHThree = checkDirection(seven, eight, nine, player1, player2, board)
    if lineHThree != nothing:
        return lineHThree
    lineVOne = checkDirection(one, four, seven, player1, player2, board)
    if lineVOne != nothing:
        return lineVOne
    lineVTwo = checkDirection(two, five, eight, player1, player2, board)
    if lineVTwo != nothing:
        return lineVTwo
    lineVThree = checkDirection(three, six, nine, player1, player2, board)
    if lineVThree != nothing:
        return lineVThree
    lineDOne = checkDirection(one, five, nine, player1, player2, board)
    if lineDOne != nothing:
        return lineDOne
    lineDTwo = checkDirection(three, five, seven, player1, player2, board)
    if lineDTwo != nothing:
        return lineDTwo
    return nothing


def checkDirection(pos1, pos2, pos3, player1, player2, board):
    if (board[pos1] == board[pos2] == board[pos3]) and (board[pos3] != nothing):
        if board[pos1] == player1:
            return player1
        elif board[pos1] == player2:
            return player2
    else:
        return nothing


def printBoard(player1, player2, board):
    nothing_char = "⬜"
    boardMessage = ""
    tile = 1
    for x in range(len(board)):
        if board[x] == nothing:
            if tile % 3 == 0:
                boardMessage = boardMessage + nothing_char + '\n'
            else:
                boardMessage = boardMessage + nothing_char
        elif board[x] == player1:
            if tile % 3 == 0:
                boardMessage = boardMessage + player1 + '\n'
            else:
                boardMessage = boardMessage + player1
        elif board[x] == player2:
            if tile % 3 == 0:
                boardMessage = boardMessage + player2 + '\n'
            else:
                boardMessage = boardMessage + player2
        tile += 1
    return boardMessage


async def getUserCharForTTT(context, bot, currentPlayer):
    await context.send("Player " + str(currentPlayer) + " Pick your character! (React with an Emoji)")

    def checkNotBot(reaction, user):
        return user != bot.user

    reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=checkNotBot)

    return str(reaction.emoji)


async def getUserCharForRPS(context, bot):
    msg = await context.send("Rock Paper Scissors (React Below)")
    await msg.add_reaction("🧱")
    await msg.add_reaction("📜")
    await msg.add_reaction("✂")

    def ifUser(reaction, user):
        return user != bot.user

    reaction, user = await bot.wait_for("reaction_add", timeout=20.0, check=ifUser)
    return str(reaction.emoji)


user.run() #<-- In this line you have to put your bot_token provided to you at the time of creating bot in the form of string
server.server()
