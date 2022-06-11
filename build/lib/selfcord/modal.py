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

from typing import List, Optional, TYPE_CHECKING, Union

from .components import _component_factory
from .enums import InteractionType
from .errors import InvalidData
from .mixins import Hashable
from .utils import _generate_nonce

if TYPE_CHECKING:
    from .appinfo import InteractionApplication
    from .components import Component
    from .interactions import Interaction

# fmt: off
__all__ = (
    'Modal',
)
# fmt: on


class Modal(Hashable):
    """Represents a modal from the Discord Bot UI Kit.

    .. versionadded:: 2.0

    .. container:: operations

        .. describe:: x == y

            Checks if two modals are equal.

        .. describe:: x != y

            Checks if two modals are not equal.

        .. describe:: hash(x)

            Return the modal's hash.

        .. describe:: str(x)

            Returns the modal's title.

    Attributes
    -----------
    id: :class:`int`
        The modal's ID. This is the same as the interaction ID.
    nonce: Optional[Union[:class:`int`, :class:`str`]]
        The modal's nonce. May not be present.
    title: :class:`str`
        The modal's title.
    custom_id: :class:`str`
        The ID of the modal that gets received during an interaction.
    components: List[:class:`Component`]
        A list of components in the modal.
    application: :class:`InteractionApplication`
        The application that sent the modal.
    """

    __slots__ = ('_state', 'interaction', 'id', 'nonce', 'title', 'custom_id', 'components', 'application')

    def __init__(self, *, data: dict, interaction: Interaction):
        self._state = interaction._state
        self.interaction = interaction
        self.id = int(data['id'])
        self.nonce: Optional[Union[int, str]] = data.get('nonce')
        self.title: str = data.get('title', '')
        self.custom_id: str = data.get('custom_id', '')
        self.components: List[Component] = [_component_factory(d) for d in data.get('components', [])]
        self.application: InteractionApplication = interaction._state.create_interaction_application(data['application'])

    def __str__(self) -> str:
        return self.title

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'custom_id': self.custom_id,
            'components': [c.to_dict() for c in self.components],
        }

    async def submit(self):
        """|coro|

        Submits the modal.

        All required components must be already answered.

        Raises
        -------
        InvalidData
            Didn't receive a response from Discord
            (doesn't mean the interaction failed).
        NotFound
            The originating message was not found.
        HTTPException
            Choosing the options failed.

        Returns
        --------
        :class:`Interaction`
            The interaction that was created.
        """
        interaction = self.interaction
        state = self._state
        nonce = _generate_nonce()
        type = InteractionType.modal_submit

        state._interaction_cache[nonce] = (int(type), None, interaction.channel)
        try:
            await state.http.interact(
                type, self.to_dict(), interaction.channel, nonce=nonce, application_id=self.application.id
            )
            i = await state.client.wait_for(
                'interaction_finish',
                check=lambda d: d.nonce == nonce,
                timeout=7,
            )
        except TimeoutError as exc:
            raise InvalidData('Did not receive a response from Discord') from exc
        finally:  # Cleanup even if we failed
            state._interaction_cache.pop(nonce, None)
        return i
