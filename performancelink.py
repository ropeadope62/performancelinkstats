import discord 
from redbot.core import commands
from redbot.core import Config, config, checks 
import random
import time
from typing import Literal
import asyncio
from redbot.core.utils.chat_formatting import (bold, box, humanize_list, humanize_number, pagify)
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
from redbot.core.utils.predicates import MessagePredicate
from dataclient import * 

class PerformanceLinkStats(commands.Cog):
    """Get Performance Link League stats. """

    def __init__(self, bot):
        """Function that initializes the cog.
        """
        self.bot = bot
        self.config = Config.get_conf(self, 2342561227844810023323455, force_registration=True)
        

        # Registering the default values for the server bot
        default_guild = {
                    "cooldown": None, #cooldown before the next bot command
                    "channels": [], #channels where the bot is listening
                    } 

        default_global = {
                    "stats_enabled": True #enable the bot by default
                    }
# Registering the default values for the config.
        default_user = {}
        self.config.register_user(**default_user)
        self.config.register_guild(**default_guild)
        self.config.register_global(**default_global)

    @commands.guild_only()
    @commands.group()
    async def stats(self, ctx):
        """Admin functions for Performance Link Stats."""
        # Reward tokens or adjust module settings
        if ctx.invoked_subcommand is None:
            guild_data = await self.config.guild(ctx.guild).all()
        if not guild_data["channels"]:
            channel_names = ["No channels set."]
        else:
            channel_names = []
            for channel_id in guild_data["channels"]:
                channel_obj = self.bot.get_channel(channel_id)
                if channel_obj:
                    channel_names.append(channel_obj.name)

        stats_cooldown = guild_data["cooldown"]
        channels = guild_data["channels"]

        msg = f"[Stats Active in]:                 {humanize_list(channel_names)}\n"
        msg += f"[Stats Cooldown]:               {guild_data['cooldown']}\n"

        for page in pagify(msg, delims=["\n"]):
            await ctx.send(box(page, lang="ini"))


    @stats.command()
    async def roster(self, ctx: commands.Context, league_id=8804):
        """Get League Roster."""
        
        roster_data = api.get_roster(league_id)
        await ctx.send(roster_data)

    @checks.mod_or_permissions(manage_guild=True)
    @stats.command()
    async def start(self, ctx, channel: discord.TextChannel = None):
        """Start Performance Link Stats"""
        if not channel:
            channel = ctx.channel

        if not channel.permissions_for(ctx.guild.me).send_messages:
            return await ctx.send(bold("I can't send messages in that channel!"))

        channel_list = await self.config.guild(ctx.guild).channels()
        if channel.id in channel_list:
            message = f"Performance Link Stats already started in {channel.mention}!"
        else:
            channel_list.append(channel.id)
            message = f"Performance Link Stats started in {channel.mention}."
            await self.config.guild(ctx.guild).channels.set(channel_list)

        await ctx.send(bold(message))

    @checks.mod_or_permissions(manage_guild=True)
    @stats.command()
    async def stop(self, ctx, channel: discord.TextChannel = None):
        """Stop Performance Link Stats"""
        if not channel:
            channel = ctx.channel
        channel_list = await self.config.guild(ctx.guild).channels()

        if channel.id not in channel_list:
            message = f"Performance Link Stats Disabled in {channel.mention}!"
        else:
            channel_list.remove(channel.id)
            message = f"Performance Link Stats has been stopped in {channel.mention}."
            await self.config.guild(ctx.guild).channels.set(channel_list)

        await ctx.send(bold(message))

def convtime(ms):
    delta = datetime.timedelta(milliseconds=(ms)).total_seconds()
    return delta

def lookup_driver(displayname):
    driver_id = api.lookup_drivers(displayname)[0]['cust_id']
    return driver_id   

def recentincidents(displayname):
    driver_id = lookup_driver(displayname)
    recentraces = api.stats_member_recent_races(driver_id)
    incidents = 0
    for race in recentraces['races']:
        incidents += race['incidents']
    return incidents

def get_roster(league_id=8804): 
    roster = []
    for eachdriver in api.league_get(league_id)['roster']:
        roster.append(tuple((eachdriver['display_name'], eachdriver['car_number'])))
    return roster
        
def get_seasons(league_id=8804):
    seasons = []
    for eachseason in api.league_seasons(league_id)['seasons']:
        seasons.append(tuple((eachseason['season_name'], eachseason['season_id'])))
    return seasons