import discord
import random
from discord.ext import commands

client = commands.Bot(command_prefix = '-', case_insensitive = True)
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="-help"))
    print("Bot is ready!")
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("**Invalid command used.**")

#PurgeMessages
@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=2):
    if amount > 100 :
        await ctx.send(f"**[X] Please input a valid amount. (1-100)**")
        return
    elif amount <= 0 :
        await ctx.send(f'**[X] Please input a valid amount. (1-100)**')
    else:
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"**[✓] Successfully deleted {len(deleted)} message(s).**")

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**[X] You do not have permission to use this command.**")
    else:
        raise(error)

#kick
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked.\nReason = {reason}')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**[X] You do not have permission to use this command.**")
    else:
        raise(error)

#ban
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned.\nReason = {reason}')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**[X] You do not have permission to use this command.**")
    else:
        raise(error)
#unbann
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users :
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} has been unbanned.')
            return

#Help
@client.command(aliases=['h'])
async def help(ctx):
    embed = discord.Embed(title="Commands :", description="**Beta :**\n`game` - plays rock paper scissors.\n`avatar @example` - shows avatar of tagged person.\n`anime` - random anime reccomendations.\n`tod` - truth or dare. (unavailable)\n`topics` - sends a random conversation topic. (unavailable)\n`wyr` - would you rather. (unavailable)\n\n**General :**\n`help` - shows you the list of commands. \n`invite` - sends bot invite link.\n`ping` - checks ping. \n\n**Fun :**\n`8ball <insert question here>` - answers the question you ask. \n`coinflip <heads / tails>` - flips a coin. \n`diceroll` - rolls a dice. \n`love <insert person's name here>` - predicts your future love's initial.\n`ship <person1> <person2>` - rate ur love uwu\n\n**Admins only Commands :**\n`ban @example <reason>` - bans a member.\n`unban <example#0000>` - unban a bannned member.\n`kick @example <reason>` - kicks a member.\n`purge <amount>` - deletes stated amount of messages. [max. 100]", colour=discord.Color.red())
    embed.set_footer(text="By @blaze#5054. (Made with discord.py)")
    await ctx.send(embed=embed)

#invite
@client.command(aliases=['i'])
async def invite(ctx):
    embed = discord.Embed(title="**Invite**", description="**Bot Invite Link :**\n[Invite our bot to your server!](https://discord.com/api/oauth2/authorize?client_id=741997618019827774&permissions=8&scope=bot) \n\n**Test Server Link :**\n[Join our test server!](https://discord.gg/x4Ek7bJ)", colour = discord.Color.red())
    embed.set_footer(text="By @blaze#5054. (Made with discord.py)")
    await ctx.send("https://discord.gg/x4Ek7bJ", embed=embed)

#Ping
@client.command()
async def ping(ctx):
    msg = await ctx.send(f"Pong! ` {round(client.latency * 1000)}ms `")
    await msg.add_reaction("🏓")
    
#avatar
@client.command()
async def avatar(ctx, *, member: discord.Member=None): # set the member object to None
    if not member: # if member is no mentioned
        member = ctx.message.author # set member as the author
    userAvatar = member.avatar_url
    await ctx.send(userAvatar)
    
#coinflip
@client.command(aliases=['cf'])
async def coinflip(ctx, *, choice):
    result = ['won', 'lost']
    if choice.lower() == 'tails' :
        await ctx.send(f'**You chose __tails__ and you __{random.choice(result)}__ !**')
    elif choice.lower() == 'heads' :
        await ctx.send(f'**You chose __heads__ and you __{random.choice(result)}__ !**')
    else :
        msg = await ctx.send(f'**Please input a proper choice! (heads/tails)**')
        await msg.add_reaction("❌")

#dieroll
@client.command(aliases=['dr'])
async def diceroll(ctx):
    dice = ["1","2","3","4","5","6"]
    await ctx.send(f'**[🎲] You rolled a __{random.choice(dice)}__ !**')

#8 Ball
@client.command (aliases=['8ball', 'ask'])
async def _8ball(ctx, *, question):
    responses = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', 'It is certain.', 'It is decidedly so.', 'Most likely.', 'My reply is no.', 'My sources say no.', 'Yes.', 'Yes – definitely.', 'IDK', 'What? I don hear YOUUUUUU!', 'How can I know, zzz', 'Maybe yes.', 'I feel sorry bro...', 'Shut up! I wanna sleep, zzz.', 'Maybe nop', 'Nomor yg anda hubungi sedang sibuk, coba hubungi sebentar lagi :)']
    await ctx.send(f'**Question** : {question}\n**Answer** : {random.choice(responses)}')

#wyr
@client.command(aliases=["wouldyourather","either"])
async def wyr(ctx):
    #stuffs = ["lmao"]
    await ctx.send("**[X] This command is currently unavailable.**")

#tod
@client.command(aliases=["truthordare"])
async def tod(ctx):
    #tord = ["truth","dare"]
    await ctx.send("**[X] This command is currently unavailable.**")

#topics
@client.command(aliases=["t","topic"])
async def topics(ctx):
    #topicos = ['']
    await ctx.send("**[X] This command is currently unavailable.**")

#Initial Prediction
@client.command(aliases=['love'])
async def predict(ctx, *, target):
    initial = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','C','G','L which stands for LONELY, LMAO','N as in NOBODY LOLOLOL','YOU BELIEVE IN THIS KIND OF STUFFS?','YOU BELIEVE IN THIS KIND OF STUFFS?','I think you will be Gay lmao','Do not believe in this, find someone who suits you :)']
    msg = await ctx.send(f'**Person 1 : __{target}__\nHis/Her Initial : __{random.choice(initial)}__**')
    await msg.add_reaction("💖")

#love2
@client.command(aliases=['rate'])
async def ship(ctx, target1, *, target2):
    number = random.randint(1,100)
    await ctx.send(f'**Person 1 : __{target1}__\nPerson 2 : __{target2}__\n>Love Percentage : {number}%.**')
    if number == 0:
        await ctx.send("`Sorry bro, very very very bad luck :(`")
    elif number >= 1 and number <= 20:
        await ctx.send("`Better luck next time.`")
    elif number >= 21 and number <= 50 :
        await ctx.send("`Not bad, Good Luck!`")
    elif number >= 51 and number <= 80 :
        await ctx.send("`Wow, this is an outstanding result!`")
    elif number >= 81 and number <= 99 :
        await ctx.send("`Congrats!`")
    else:
        await ctx.send("OMG you can get married now!")

#rps
@client.command(pass_context=True, aliases=['rps'])
@commands.guild_only()
async def game(ctx):
    
    await ctx.send("**[🛠️] Command is under maintenance, thank you for your patience.**")
    '''
    await ctx.send(
        'Hello, ' + ctx.message.author.mention + '? Wanna play a round of Rock, Paper, Scissors?')

    wins = 0
    losses = 0
    ties = 0

    while True:
        await ctx.send('%s Wins, %s Losses, %s Draws \n' % (wins, losses, ties))
        while True:
            await ctx.send('What is your choice? (r)ock, (p)aper, (s)cissors or (q)uit')  
            player = await client.wait_for('message') 
            print(str(player))
            if player.content == 'q':
                await ctx.send('Game succesfully quitted.')
                return
            if player.content == 'r' or player.content == 'p' or player.content == 's':
                break

        if player.content == 'r':
            await ctx.send('Rock against...')
        elif player.content == 'p':
            await ctx.send('Paper against...')
        elif player.content == 's':
            await ctx.send('Scissors against...')

        randomnum = random.randint(1, 3)
        if randomnum == 1:
            computer = 'r'
            await ctx.send('Rock!')
        elif randomnum == 2:
            computer = 'p'
            await ctx.send('Paper!')
        elif randomnum == 3:
            computer = 's'
            await ctx.send('Scissors!')

        if player.content == computer:
            await ctx.send("It's a Draw!")
            ties = ties + 1
        elif player.content == 'r' and computer == 's':
            await ctx.send('You win!')
            wins = wins + 1
        elif player.content == 'r' and computer == 'p':
            await ctx.send('The bot wins!')
            losses = losses + 1
        elif player.content == 'p' and computer == 'r':
            await ctx.send('You win!')
            wins = wins + 1
        elif player.content == 'p' and computer == 's':
            losses = losses + 1
            await ctx.send('The bot wins!')
        elif player.content == 's' and computer == 'p':
            await ctx.send('You win!')
            wins = wins + 1
        elif player.content == 's' and computer == 'r':
            await ctx.send('The bot wins!')
            losses = losses + 1
'''
#anime
@client.command()
async def anime(ctx):
    animename = ["Fire Force", "Jojo's Bizzare Adventure", "Hunter X Hunter", "Haikyuu!", "Demon Slayer", "Flame of Rekka"]
    await ctx.send(f">>> __**Here's a random anime reccomendation**__\n ->> {random.choice(animename)}\n\n`Tips : You might as well add your reccomendations by sending them in our Test Server!\nDo '-invite' for Server Link!`")

client.run("NzQxOTk3NjE4MDE5ODI3Nzc0.Xy_tIQ.KZerR1oZwMNeL8l8ej6DjGsOLgM")

#command under repair ("**[🛠️] Command is under maintenance, thank you for your patience.**")
