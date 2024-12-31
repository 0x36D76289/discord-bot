import discord

def create_embed(title, description=None, color=discord.Color.blue(), fields=None, thumbnail=None, image=None, footer=None):
    """Crée un embed Discord avec un formatage moderne.

    Args:
        title (str): Titre de l'embed.
        description (str, optional): Description de l'embed. Defaults to None.
        color (discord.Color, optional): Couleur de l'embed. Defaults to discord.Color.blue().
        fields (list, optional): Liste de dictionnaires pour les champs. Chaque dictionnaire doit avoir les clés "name", "value" et "inline" (optionnel). Defaults to None.
        thumbnail (str, optional): URL de la miniature. Defaults to None.
        image (str, optional): URL de l'image. Defaults to None.
        footer (str, optional): Texte du pied de page. Defaults to None.

    Returns:
        discord.Embed: L'embed créé.
    """
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )

    if fields:
        for field in fields:
            embed.add_field(
                name=field.get("name"),
                value=field.get("value"),
                inline=field.get("inline", False)
            )

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    if image:
        embed.set_image(url=image)

    if footer:
        embed.set_footer(text=footer)

    return embed