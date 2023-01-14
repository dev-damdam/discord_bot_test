import os
import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("token")
intents = discord.Intents.default()
bot = Bot(command_prefix='!kebi ', intents=intents)
bot.remove_command("help")

if __name__ == '__main__':

    @bot.event
    async def on_ready():
        print("Hi, logged in as " + bot.user.name, end='\n')

    @bot.command()
    async def hello(ctx):
        await ctx.reply('안녕하세요, 공부하는 케비에요.')

    @bot.command()
    async def help(ctx):
        cmds = ""
        cmds += ("channels : 채널 별 아이디 확인" + '\n')
        cmds += ("check {채널아이디} : 해당 채널에 접속한 멤버 리스트 확인" + '\n')
        await ctx.reply(cmds)

    @bot.command()
    async def channels(ctx):
        channels = bot.get_all_channels()
        msg = ""
        for ch in channels :
            if ch.guild is not ctx.channel.guild :
                continue
            if isinstance(ch, discord.TextChannel):
                msg += ("[채팅채널]" + '\t' + str(ch.name) + "\t" + str(ch.id) + '\n')
            elif isinstance(ch, discord.VoiceChannel):
                msg += ("[음성채널]" + '\t' + str(ch.name) + "\t" + str(ch.id) + '\n')
        await ctx.reply(msg)

    def isValidArgs(argNum, *args) :
        if args is None or args is [] :
            return False
        if len(args) is 0 :
            if argNum is 0 :
                return True
            else :
                return False
        if argNum != len(args) :
            return False
        return True

    @bot.command()
    async def check(ctx, *args):

        if not isValidArgs(1, *args) :
            msg = "명령어를 잘못 입력하셨네요." + '\n'
            msg += "check {채널아이디} : 해당 채널에 접속한 멤버 리스트 확인"
            await ctx.reply(msg)
            return

        channelId = int(args[0])

        channel = bot.get_channel(channelId)

        mems = channel.members
        if len(mems) is 0 :
            await ctx.reply("아무도 없습니다!")
            return

        msg = "== 현재 " + str(channel.name) + "채널 접속 멤버 ==" + '\n'
        msg += ("☑️ " + str(len(mems)) + "명 접속중" + '\n')
        msg += '\n'
        for mem in mems :
            msg += (str(mem.display_name) + '\n')

        else :
            await ctx.reply(msg)

    bot.run(token)
