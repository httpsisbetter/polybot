#os.system("pip install -U py-cord==2.1.1")
# Remove the comment if you want to auto install pycord


import time
import datetime
import requests
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord_webhook import DiscordWebhook, DiscordEmbed
import logging
import json
import os
import socket
import subprocess
import random
import psutil
from uptime import uptime
import cpuinfo


NODE_NAME = "PolyServer"
wait = time.sleep
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f'Logged In As > {bot.user.name}') 


@bot.slash_command(description="Shows VPS stats",)
async def stats(ctx):
    await ctx.defer()
    up = uptime()
    time = float(up)
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    uptime_stamp = ("%dd %dh %dm %ds" % (day, hour, minutes, seconds))
    cpu = cpuinfo.get_cpu_info()["brand_raw"]
    threads = cpuinfo.get_cpu_info()["count"]
    cpu_usage = f"CPU Usage: {psutil.cpu_percent(interval=1)}%"
    ram_usage = f"Ram Usage: {round(psutil.virtual_memory().used/1000000000, 2)}GB / {round(psutil.virtual_memory().total/1000000000, 2)}GB"
    swap_usage = f"SWAP Usage: {round(psutil.swap_memory().used/1000000000, 2)}GB / {round(psutil.swap_memory().total/1000000000, 2)}GB"
    disk_usage = f"Disk Usage: {round(psutil.disk_usage('/').used/1000000000, 2)}GB / {round(psutil.disk_usage('/').total/1000000000, 2)}GB"
    response = requests.get(f"http://ip-api.com/json/").json()
    physical_info = f"CPU: {threads} Threads | {cpu}\nIP: {response['query']}"


    embed = discord.Embed(title=f"{NODE_NAME} Stats", description=f"**----- Node Info ----**\n**```\n{cpu_usage} \n{ram_usage}\n{swap_usage}\n{disk_usage}```**\n**----- Physical Info -----**\n**```\n{physical_info}```**", color=discord.Color.blue())
    embed.set_footer(text=f"Uptime: {uptime_stamp}")
    await ctx.respond(embed=embed)

@bot.slash_command(description="Resolver a sites DNS", )
async def dnsresolver(ctx, host):
    try:
        host2 = host.lower()
        dnsresolve = socket.gethostbyname(host2)
        embed = discord.Embed(title="__**DNS Resolver**__", color=0x268bd2)
        embed.add_field(name="Host ↓", value=f"```ini\n[{host}]```", inline=True)
        embed.add_field(name="DNS  ↓", value=f"```ini\n[{dnsresolve}]```", inline=True)
        await ctx.respond(embed=embed)
    except Exception as e:
        embed = discord.Embed(description=f"__**Error**__\n ```{e}```", color=0x880808)
        await ctx.respond(embed=embed)
        print(e)

@bot.slash_command(description="IP information", )
async def geoip(ctx, ip):
    r = requests.get(f'https://json.geoiplookup.io/{ip}')
    ISP = r.json()['isp']
    hostname = r.json()['hostname']
    Country = r.json()['country_name']
    Continent = r.json()['continent_name']
    state = r.json()['region']
    City = r.json()['city']
    Zipcode = r.json()["postal_code"] 
    latitude = r.json()["latitude"] 
    longitude = r.json()["longitude"] 
    embed = discord.Embed(color=0x268bd2)
    embed.add_field(name='__**Geo Lookup**__', value=f'```• IP: {ip}\n• ISP: {ISP}\n• Hostname: {hostname}\n• Country: {Country}\n• Continent: {Continent}\n• State: {state}\n• City: {City}\n• Zipcode: {Zipcode}```', inline=False)
    embed.set_footer(text=f'Requested By {ctx.author}', icon_url="https://cdn.discordapp.com/attachments/1018595433448222854/1018597427126738964/unknown.png")
    await ctx.respond(embed=embed)

@bot.slash_command(description="pee pee", )
async def pinger(ctx, host):
    try:
        await ctx.defer()
        pingR = subprocess.getoutput(f"ping {host} -n 5")
        pingP = pingR.split("\n")
        embed = discord.Embed(title="__**Ping**__",description=f"```{pingP[3]}\n{pingP[4]}\n{pingP[5]}\n{pingP[6]}{pingP[7]}```", color=0x268bd2)
        embed.set_footer(text=f'Requested By {ctx.author}')
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(description=f"__**Error**__\n ```{e}```", color=0x880808)
        await ctx.respond(embed=embed)
        print(e)

@bot.slash_command(description="help menu",)
async def help(ctx):
   embed =discord.Embed(description="__**PolyC2 Menu**__\n```int\n /stats            | Gets the server stats```", color=0x268bd2)
   embed.add_field(name="__**Tools**__", value="```ini\n /geoip           | Looks up the geolocation info of an ip\n /pinger          | Sends an ICMP packet to ping an ip\n /dnsresolver     | Resolves DNS```", inline=False)
   await ctx.respond(embed=embed)

bot.run("TOKENHERE")

