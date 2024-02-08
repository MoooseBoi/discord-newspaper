import importlib
import os

current_dir = os.path.dirname(__file__)
modules = [f.removesuffix(".py") for f in os.listdir(current_dir) if os.path.isfile(f) and f.endswith(".py") and f != "__init__.py"]


async def add_cogs(bot, records):
    for module_name in modules:
        cog = importlib.import_module(f"{__name__}.{module_name}").Cog(bot, records)
        bot.add_cog(cog)
