from __future__ import annotations

from typing import List, Literal, Union

from discord import Client, Embed, Message
from dispie.music import Node, MusicPlayer
from pomice import Player, NodePool, Track


class MusicClient:
    """
    A class representing a client for a music player bot.

    Parameters:
        - bot: The Discord bot client object.
        - nodes: A list of node objects or a single node object to connect to.
    """

    def __init__(self, bot: Client, nodes: list[Node] | Node) -> None:
        self.bot = bot
        self.nodes = [nodes] if isinstance(nodes, Node) else nodes
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
    async def handle_on_message(self, message: Message) -> None:
        """
        A coroutine that handles the message event.

        Parameters:
            - message: The message object.
        """
        # TODO: Implement message handling logic

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

