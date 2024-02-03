import importlib
import os


handles = []
for handle in os.listdir(os.path.dirname(__file__)):
    if handle in ("__init__.py", "__pycache__"):
        continue

    handle = handle.replace(".py", "")
    handles.append(importlib.import_module(f"handlers.{handle}"))


def get_embeds(feeds):
    embeds = []
    for handle in handles:
        try:
            args = feeds[handle.__name__.removeprefix("handlers.")]

            if type(args) is bool:
                embed = handle.get_embed(args)
                embeds.append(embed)
                continue
            for arg in args:
                embed = handle.get_embed(arg)
                embeds.append(embed)

        except KeyError:
            continue
    return embeds


def handle_exists(name):
    name = "handlers." + name
    for handle in handles:
        if handle.__name__ == name:
            return True
    return False