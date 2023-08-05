from __future__ import annotations

from typing import TYPE_CHECKING
from dispie import View

if TYPE_CHECKING:
    ...

__all__ = ("SelectPrompt", "ChannelPrompt", "MemberPrompt")


class SelectPrompt(View):
    ...

class ChannelPrompt(View):
    ...


class MemberPrompt(View):
    ...