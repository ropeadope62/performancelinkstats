from .performancelink import PerformanceLinkStats

async def setup(bot):
    bot.add_cog(PerformanceLinkStats(bot))
