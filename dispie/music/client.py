from __future__ import annotations

from typing import Literal, Optional

from discord import Embed, Message, TextChannel
from discord.ext.commands import Bot
from .types import Node
from pomice import NodePool, Track
from logging import getLogger

log = getLogger("Dispie Music Client")

# https://github.com/freyacodes/Lavalink/releases/download/3.7.5/Lavalink.jar

class MusicClient:
    """
    A class representing a client for a music player bot.

    Parameters:
    - bot: The Discord bot client object.
    - nodes: A list of node objects or a single node object to connect to.
    """

    def __init__(self, bot: Bot, nodes: list[Node] | Node) -> None:
        self.bot = bot
        self.nodes = [nodes] if isinstance(nodes, dict) else nodes
        self._node_pool = NodePool()
        self._no_playing_embed = Embed(title="No track playing")
        self._playing_embed = Embed(title="Now playing")
        self._paused_embed = Embed(title="Track paused")

    @property
    def no_playing_embed(self) -> Embed:
        """
        Returns the no playing embed.
        """
        return self._no_playing_embed

    @no_playing_embed.setter
    def no_playing_embed(self, value: Embed) -> None:
        """
        Sets the no playing embed.

        Parameters:
            - value: The new no playing embed.
        """
        self._no_playing_embed = value

    @property
    def playing_embed(self) -> Embed:
        """
        Returns the playing embed.
        """
        return self._playing_embed

    @playing_embed.setter
    def playing_embed(self, value: Embed) -> None:
        """
        Sets the playing embed.

        Parameters:
        - value: The new playing embed.
        """
        self._playing_embed = value

    @property
    def paused_embed(self) -> Embed:
        """
        Returns the paused embed.
        """
        return self._paused_embed

    @paused_embed.setter
    def paused_embed(self, value: Embed) -> None:
        """
        Sets the paused embed.

        Parameters:
        - value: The new paused embed.
        """
        self._paused_embed = value

    @property
    def node_pool(self) -> NodePool:
        """
        Returns the node pool object.
        """
        return self._node_pool

    @node_pool.setter
    def node_pool(self, value: NodePool) -> None:
        """
        Sets the node pool object.

        Parameters:
        - value: The new node pool object.
        """
        self._node_pool = value


    def get_player_embed(self, player_type: Literal["no_playing", "playing", "paused"]) -> Embed:
        """
        Get the embed for the player.
        
        Parameters:
        - player_type: Type of the player.
        """
        # TODO: Return later


    def get_message(self, message_id: int, channel_id: int) -> Optional[Message]:
        if (mable := self.bot.get_partial_messageable(channel_id)):
            if (message := mable.get_partial_message(message_id)):
                return Message


    async def setup_player_embed(self, channel: TextChannel) -> Message:
        """
        Setup the player embed.
        Parameters:
        - channel: The channel you want to setup the player. 
        """
        return await channel.send(
            embed=self.get_player_embed(player_type="no_playing")
        )

    async def handle_on_message(self, message: Message, player_message_id: int) -> None:
        """
        A coroutine that handles the message event.

        Parameters:
        - message: The message object.
        - player_message_id: The message id of the player embed.
        """
        if message.author.bot:
            if message.author.id == self.bot.user.id:
                await message.delete(delay=5)
            await message.delete()
            return
        await self.bot.process_commands(message)
        


    async def handle_track_start(self, track: Track) -> None:
        """
        A coroutine that handles the start of a new track.

        Parameters:
        - track: The new track object.
        """
        # TODO: Implement track start handling logic

    async def handle_track_end(self, track: Track) -> None:
        """
        A coroutine that handles the end of a track.

        Parameters:
        - track: The ending track object.
        """
        # TODO: Implement track end handling logic

    async def start_nodes(self):
        for nodes in self.nodes:
            node = await self._node_pool.create_node(
                bot=self.bot,
                host=nodes.get("host"),
                port=nodes.get("port"),
                password=nodes.get("password"),
                identifier=nodes.get("identifier")
            )
            log.info(f"{node._identifier} has been created.")
