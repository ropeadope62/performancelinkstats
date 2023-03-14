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
from .dataclient import api, lookup_driver, recentincidents, get_roster, get_seasons, get_seasonstandings

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
    @commands.group()
    async def stats(self, ctx):
        """Admin functions for Performance Link Stats."""
        # Reward tokens or adjust module settings

    @stats.command()
    async def roster(self, ctx: commands.Context, league_id=8804):
        """Get Active League Roster."""
        
        roster_data = get_roster(league_id)
        await ctx.send(roster_data)
    @stats.command()
    async def seasons(self, ctx: commands.Context, league_id=8804):
        """Get League Seasons."""
        seasons_data = get_seasons(league_id)
        await ctx.send(seasons_data)

    @stats.command()
    async def standings(self, ctx: commands.Context, season_number: int, league_id=8804):
        """Get League Standings."""
        
        season_standings = get_seasonstandings(season_number, league_id)
        await ctx.send(season_standings)
        
    @checks.mod_or_permissions(manage_guild=True)
    @stats.command()
    async def admin(self, ctx):
        """Admin functions for Performance Link Stats."""
        # Reward tokens or adjust module settings

        guild_data = await self.config.guild(ctx.guild).all()
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


    