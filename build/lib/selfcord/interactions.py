"""
The MIT License (MIT)

Copyright (c) 2021-present Dolfies

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Union

from .enums import InteractionType, try_enum
from .mixins import Hashable
from .utils import cached_slot_property, find, MISSING

if TYPE_CHECKING:
    from .channel import DMChannel, GroupChannel, TextChannel, VoiceChannel
    from .guild import Guild
    from .message import Message
    from .modal import Modal
    from .state import ConnectionState
    from .threads import Thread
    from .types.snowflake import Snowflake
    from .types.user import User as UserPayload
    from .user import BaseUser, ClientUser

    MessageableChannel = Union[TextChannel, Thread, DMChannel, GroupChannel, VoiceChannel]

# fmt: off
__all__ = (
    'Interaction',
)
# fmt: on


class Interaction(Hashable):
    """Represents an interaction.

    .. versionadded:: 2.0

    .. container:: operations

        .. describe:: x == y

            Checks if two interactions are equal.

        .. describe:: x != y

            Checks if two interactions are not equal.

        .. describe:: hash(x)

            Return the interaction's hash.

    Attributes
    ------------
    id: :class:`int`
        The interaction ID.
    nonce: Optional[Union[:class:`int`, :class:`str`]]
        The interaction's nonce. Not always present.
    name: Optional[:class:`str`]
        The name of the application command, if applicable.
    type: :class:`InteractionType`
        The type of interaction.
    successful: :class:`bool`
        Whether the interaction succeeded.
        If this is your interaction, this is not immediately available.
        It is filled when Discord notifies us about the outcome of the interaction.
    user: Union[:class:`Member`, :class:`abc.User`]
        The :class:`Member` who initiated the interaction.
        If :attr:`channel` is a private channel or the
        user has the left the guild, then it is a :class:`User` instead.
    modal: Optional[:class:`Modal`]
        The modal that is in response to this interaction.
        This is not immediately available and is filled when the modal is dispatched.
    """

    __slots__ = ('id', 'type', 'nonce', 'user', 'name', 'successful', 'modal', '_cs_message', '_cs_channel', '_state')

    def __init__(
        self,
        id: int,
        type: int,
        nonce: Optional[Snowflake] = None,
        *,
        user: BaseUser,
        state: ConnectionState,
        name: Optional[str] = None,
        message: Optional[Message] = None,
        channel: Optional[MessageableChannel] = None,
    ) -> None:
        self.id = id
        self.nonce = nonce
        self.type = try_enum(InteractionType, type)
        self.user = user
        self.name = name
        self.successful: bool = MISSING
        self.modal: Optional[Modal] = None
        self._state = state
        if message is not None:
            self._cs_message = message
        if channel is not None:
            self._cs_channel = channel

    @classmethod
    def _from_self(
        cls,
        channel: MessageableChannel,
        *,
        id: Snowflake,
        type: int,
        nonce: Optional[Snowflake] = None,
        user: ClientUser,
        name: Optional[str],
    ) -> Interaction:
        return cls(int(id), type, nonce, user=user, name=name, state=user._state, channel=channel)

    @classmethod
    def _from_message(cls, message: Message, *, id: Snowflake, type: int, user: UserPayload, **data) -> Interaction:
        state = message._state
        name = data.get('name')
        user_cls = state.store_user(user)
        self = cls(int(id), type, user=user_cls, name=name, message=message, state=state)
        self.successful = True
        return self

    def __repr__(self) -> str:
        s = self.successful
        return f'<Interaction id={self.id} type={self.type}{f" successful={s}" if s is not None else ""} user={self.user!r}>'

    def __bool__(self) -> bool:
        if self.successful is not MISSING:
            return self.successful
        raise TypeError('Interaction has not been resolved yet')

    @cached_slot_property('_cs_message')
    def message(self) -> Optional[Message]:
        """Optional[:class:`Message`]: Returns the message that is the response to this interaction.
        May not exist or be cached.
        """

        def predicate(message: Message) -> bool:
            return message.interaction is not None and message.interaction.id == self.id

        return find(predicate, self._state.client.cached_messages)

    @property
    def guild(self) -> Optional[Guild]:
        """Optional[:class:`Guild`]: Returns the guild the interaction originated from."""
        return getattr(self.channel, 'guild', getattr(self.message, 'guild', None))

    @cached_slot_property('_cs_channel')
    def channel(self) -> MessageableChannel:
        """Union[:class:`TextChannel`, :class:`Thread`, :class:`DMChannel`, :class:`GroupChannel`]:
        Returns the channel this interaction originated from.
        """
        return getattr(self.message, 'channel', None)
