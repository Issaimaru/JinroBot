# -*- coding: utf-8 -*-

#######################

#Created by Issaimaru

#Created at 2021-04-30(Update)

#######################


import discord
import datetime
import time
import asyncio
import random
import linecache
from Jinro import Jinro
from collections import defaultdict
from statistics import mode
user_reaction_dic = defaultdict(dict)

_TOKEN=linecache.getline('Setting.txt',9).split(':')
TOKEN = _TOKEN[1]

intents = discord.Intents.default()
intents.members=True#membersがdefaultではFalseなのでTrueにする
client = discord.Client(intents=intents)

#グローバル変数
Playing_check=False
J_Mahou=False
J_Uranayer=False
J_Kaitouyer=False
J_kaitou=False
Votes=False
J_member=[]
J_memberid=[]
J_Uraned=[]
J_kaitoued=[]
Jinro_list=[]
Uranai_list=[]
Kaitou_list=[]
Vote=[]
Voted=[]
J_attend=0
job_dic={}
J_card = ["人狼","人狼","占い師","怪盗"]


@client.event
async def on_ready():
    print("Botの起動が終わりました")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    Morning = ["おはよう","おはようございます","おはこんばにちは"]
    Hello = ["こんにちは","おはこんばにちは"]
    Night = ["おやすみなさい","おやすみね！","おやすみなさい!"]

    #挨拶メッセージ
    user_name = message.author.name
    if message.content in Morning: await message.channel.send(user_name + ",おはようございます!")
    if message.content in Hello: await message.channel.send(user_name + ",こんにちは!")
    if message.content in Night: await message.channel.send(user_name + ",おやすみなさい!")

    #人狼ゲーム
    Jinro_txt = ["-T 人狼がしたい","-T　人狼しようぜ","-T j"]
    global Playing_check,J_attend,embed_GameStart,J_Mahou,J_kaitou,job_dic,J_member,J_memberid,Jinro_list,Kaitou_list,Uranai_list,J_card,J_Uraned,Votes,Vote,J_Kaitouyer,J_kaitoued,J_Uranayer,Voted

    if message.content in Jinro_txt and Playing_check==False and len(J_member)==0:
        await client.change_presence(activity=discord.Game(name="人狼の司会者", type=1))#ゲームアクティビティを変更する
        Playing_check=True
        returns=await Jinro.run(message)
        J_attend=returns[0]
        embed_GameStart=returns[1]
        await asyncio.sleep(60)#参加者募集時間
        Playing_check=False

        retu_two=await Jinro.moderator(J_attend,embed_GameStart,J_member,J_memberid,message,client,Jinro_list,Uranai_list,Kaitou_list,J_card,job_dic)
        J_Mahou=retu_two[0]
        if J_Mahou==False:
            await End(message)
            return
        job_dic=retu_two[1]
        await asyncio.sleep(30)#魔法使いの行動時間
        J_Mahou=False
        await message.channel.send("次に怪盗の方は行動してください(30秒間)")
        J_kaitou=True
        await asyncio.sleep(30)#怪盗の行動時間
        J_kaitou=False
        embed=discord.Embed(title="議論開始",description="昼になりました。\n参加者は議論を開始してください\n制限時間は5分間です",colour=0x7cfc00)
        image=linecache.getline('Setting.txt',15).split('>')
        embed.set_thumbnail(url=image[1])
        await message.channel.send(embed=embed)
        await asyncio.sleep(60*5)#議論の時間
        Votes=await Jinro.Vote_Send(message,J_member,J_memberid,client)#投票用のメッセージを送りつける
        await asyncio.sleep(60)#投票する時間
        Votes=False
        await Jinro.Judge(message,Vote,Jinro_list)
        await asyncio.sleep(5)#結果発表を見る時間
        await End(message)

    elif message.content in Jinro_txt and (Playing_check==True or len(J_member)>0):await message.channel.send("他の方がゲームをプレイ中です...")

    if J_Mahou==True and message.author.id in Uranai_list:J_Uranayer=await Jinro.Mahou_job(message,J_card,J_member,J_memberid,J_Uranayer,job_dic,J_Uraned)#魔法使いの処理
    if J_kaitou==True and message.author.id in Kaitou_list:J_Kaitouyer=await Jinro.Kaitou_Job(message,J_member,J_memberid,J_Kaitouyer,job_dic,Jinro_list,J_kaitoued)#怪盗の処理

    if Votes==True and message.author.id in J_memberid and not message.author.id in Voted:await Jinro.Votes_receive(message,J_member,Vote,Voted)
    elif Votes==True and message.author.id in Voted and isinstance(message.channel, discord.DMChannel):await message.author.send("あなたはすでに投票しています!")


@client.event
async def on_raw_reaction_add(payload):
    global J_attend,user_reaction_dic,embed_GameStart,J_member,J_memberid
    if J_attend==0 or Playing_check==False:return
    await Jinro.reaction_vote(payload,embed_GameStart,J_attend,user_reaction_dic,J_member,J_memberid,client)

@client.event
async def on_raw_reaction_remove(payload):
    global J_attend,user_reaction_dic,embed_GameStart,J_member,J_memberid
    if J_attend==0 or Playing_check==False:return
    await Jinro.reaction_remove(payload,embed_GameStart,J_attend,user_reaction_dic,J_member,J_memberid,client)


async def End(message):
    global Playing_check,J_Mahou,J_Uranayer,J_Kaitouyer,J_kaitou,Votes,J_member,J,memberid,J_Uraned,J_Kaitoued,Jinro_list,Uranai_list,Kaitou_list,Vote,Voted,J_attend,job_dic,J_card
    Playing_check=False
    J_Mahou=False
    J_Uranayer=False
    J_Kaitouyer=False
    J_kaitou=False
    Votes=False
    J_member.clear()
    J_memberid.clear()
    J_Uraned.clear()
    J_kaitoued.clear()
    Jinro_list.clear()
    Uranai_list.clear()
    Kaitou_list.clear()
    Vote.clear()
    Voted.clear()
    J_attend=0
    job_dic.clear()
    J_card = ["人狼","人狼","占い師","怪盗"]
    #すべてのグローバル変数を初期値に戻す
    await client.change_presence(activity=None)
    await message.channel.send("人狼ゲームが正常終了しました!")

client.run(TOKEN)#指定のトークンのBOTを起動させる
