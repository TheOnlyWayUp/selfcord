"""
The MIT License (MIT)

Copyright (c) 2015-present Rapptz

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

from asyncio import TimeoutError
from typing import Any, ClassVar, Dict, List, Optional, TYPE_CHECKING, Tuple, Union

from .enums import try_enum, ComponentType, ButtonStyle, TextStyle, InteractionType
from .errors import InvalidData
from .utils import _generate_nonce, get_slots, MISSING
from .partial_emoji import PartialEmoji, _EmojiTag

if TYPE_CHECKING:
    from typing_extensions import Self

    from .types.components import (
        Component as ComponentPayload,
        ButtonComponent as ButtonComponentPayload,
        SelectMenu as SelectMenuPayload,
        SelectOption as SelectOptionPayload,
        ActionRow as ActionRowPayload,
        TextInput as TextInputPayload,
    )
    from .emoji import Emoji
    from .interactions import Interaction
    from .message import Message


__all__ = (
    'Component',
    'ActionRow',
    'Button',
    'SelectMenu',
    'SelectOption',
    'TextInput',
)


class Component:
    """Represents a Discord Bot UI Kit Component.

    Currently, the only components supported by Discord are:

    - :class:`ActionRow`
    - :class:`Button`
    - :class:`SelectMenu`
    - :class:`TextInput`

    .. versionadded:: 2.0

    Attributes
    ------------
    type: :class:`ComponentType`
        The type of component.
    """

    __slots__: Tuple[str, ...] = ('type', 'message')

    __repr_info__: ClassVar[Tuple[str, ...]]
    type: ComponentType
    message: Message

    def __repr__(self) -> str:
        attrs = ' '.join(f'{key}={getattr(self, key)!r}' for key in self.__repr_info__)
        return f'<{self.__class__.__name__} {attrs}>'

    @classmethod
    def _raw_construct(cls, **kwargs) -> Self:
        self = cls.__new__(cls)
        for slot in get_slots(cls):
            try:
                value = kwargs[slot]
            except KeyError:
                pass
            else:
                setattr(self, slot, value)
        return self

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError


class ActionRow(Component):
    """Represents a Discord Bot UI Kit Action Row.

    This is a component that holds up to 5 children components in a row.

    This inherits from :class:`Component`.

    .. versionadded:: 2.0

    Attributes
    ------------
    type: :class:`ComponentType`
        The type of component.
    children: List[:class:`Component`]
        The children components that this holds, if any.
    message: :class:`Message`
        The originating message.
    """

    __slots__: Tuple[str, ...] = ('children',)

    __repr_info__: ClassVar[Tuple[str, ...]] = __slots__

    def __init__(self, data: ComponentPayload, message: Message):
        self.message = message
        self.type: ComponentType = try_enum(ComponentType, data['type'])
        self.children: List[Component] = [_component_factory(d, message) for d in data.get('components', [])]

    def to_dict(self) -> ActionRowPayload:
        return {
            'type': int(self.type),
            'components': [child.to_dict() for child in self.children],
        }  # type: ignore # Type checker does not understand these are the same


class Button(Component):
    """Represents a button from the Discord Bot UI Kit.

    This inherits from :class:`Component`.

    .. versionadded:: 2.0

    Attributes
    -----------
    style: :class:`.ButtonStyle`
        The style of the button.
    custom_id: Optional[:class:`str`]
        The ID of the button that gets received during an interaction.
        If this button is for a URL, it does not have a custom ID.
    url: Optional[:class:`str`]
        The URL this button sends you to.
    disabled: :class:`bool`
        Whether the button is disabled or not.
    label: Optional[:class:`str`]
        The label of the button, if any.
    emoji: Optional[:class:`PartialEmoji`]
        The emoji of the button, if available.
    message: :class:`Message`
        The originating message.
    """

    __slots__: Tuple[str, ...] = (
        'style',
        'custom_id',
        'url',
        'disabled',
        'label',
        'emoji',
    )

    __repr_info__: ClassVar[Tuple[str, ...]] = __slots__

    def __init__(self, data: ButtonComponentPayload, message: Message):
        self.message = message
        self.type: ComponentType = try_enum(ComponentType, data['type'])
        self.style: ButtonStyle = try_enum(ButtonStyle, data['style'])
        self.custom_id: Optional[str] = data.get('custom_id')
        self.url: Optional[str] = data.get('url')
        self.disabled: bool = data.get('disabled', False)
        self.label: Optional[str] = data.get('label')
        self.emoji: Optional[PartialEmoji]
        try:
            self.emoji = PartialEmoji.from_dict(data['emoji'])
        except KeyError:
            self.emoji = None

    def to_dict(self) -> dict:
        return {
            'component_type': self.type.value,
            'custom_id': self.custom_id,
        }

    async def click(self) -> Union[str, Interaction]:
        """|coro|

        Clicks the button.

        Raises
        -------
        InvalidData
            Didn't receive a response from Discord
            (doesn't mean the interaction failed).
        NotFound
            The originating message was not found.
        HTTPException
            Clicking the button failed.

        Returns
        --------
        Union[:class:`str`, :class:`Interaction`]
            The button's URL or the interaction that was created.
        """
        if self.url:
            return self.url

        message = self.message
        state = message._state
        nonce = _generate_nonce()
        type = InteractionType.component

        state._interaction_cache[nonce] = (int(type), None, message.channel)
        try:
            await state.http.interact(type, self.to_dict(), message.channel, message, nonce=nonce)
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


class SelectMenu(Component):
    """Represents a select menu from the Discord Bot UI Kit.

    A select menu is functionally the same as a dropdown, however
    on mobile it renders a bit differently.

    .. versionadded:: 2.0

    Attributes
    ------------
    custom_id: Optional[:class:`str`]
        The ID of the select menu that gets received during an interaction.
    placeholder: Optional[:class:`str`]
        The placeholder text that is shown if nothing is selected, if any.
    min_values: :class:`int`
        The minimum number of items that must be chosen for this select menu.
    max_values: :class:`int`
        The maximum number of items that must be chosen for this select menu.
    options: List[:class:`SelectOption`]
        A list of options that can be selected in this menu.
    disabled: :class:`bool`
        Whether the select is disabled or not.
    message: :class:`Message`
        The originating message, if any.
    """

    __slots__: Tuple[str, ...] = (
        'custom_id',
        'placeholder',
        'min_values',
        'max_values',
        'options',
        'disabled',
        'hash',
    )

    __repr_info__: ClassVar[Tuple[str, ...]] = __slots__

    def __init__(self, data: SelectMenuPayload, message: Message):
        self.message = message
        self.type = ComponentType.select
        self.custom_id: str = data['custom_id']
        self.placeholder: Optional[str] = data.get('placeholder')
        self.min_values: int = data.get('min_values', 1)
        self.max_values: int = data.get('max_values', 1)
        self.options: List[SelectOption] = [SelectOption.from_dict(option) for option in data.get('options', [])]
        self.disabled: bool = data.get('disabled', False)
        self.hash: str = data.get('hash', '')

    def to_dict(self, options: Tuple[SelectOption]) -> dict:
        return {
            'component_type': self.type.value,
            'custom_id': self.custom_id,
            'values': [option.value for option in options],
        }

    async def choose(self, *options: SelectOption) -> Interaction:
        """|coro|

        Chooses the given options from the select menu.

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
        message = self.message
        state = message._state
        nonce = _generate_nonce()
        type = InteractionType.component

        state._interaction_cache[nonce] = (int(type), None, message.channel)
        await state.http.interact(type, self.to_dict(options), message.channel, message, nonce=nonce)
        try:
            i = await state.client.wait_for(
                'interaction_finish',
                check=lambda d: d.nonce == nonce,
                timeout=7,
            )
        except TimeoutError as exc:
            raise InvalidData('Did not receive a response from Discord') from exc
        return i


class SelectOption:
    """Represents a select menu's option.

    .. versionadded:: 2.0

    Attributes
    -----------
    label: :class:`str`
        The label of the option. This is displayed to users.
        Can only be up to 100 characters.
    value: :class:`str`
        The value of the option. This is not displayed to users.
        If not provided when constructed then it defaults to the
        label. Can only be up to 100 characters.
    description: Optional[:class:`str`]
        An additional description of the option, if any.
        Can only be up to 100 characters.
    emoji: Optional[Union[:class:`str`, :class:`Emoji`, :class:`PartialEmoji`]]
        The emoji of the option, if available.
    default: :class:`bool`
        Whether this option is selected by default.
    """

    __slots__: Tuple[str, ...] = (
        'label',
        'value',
        'description',
        'emoji',
        'default',
    )

    def __init__(
        self,
        *,
        label: str,
        value: str = MISSING,
        description: Optional[str] = None,
        emoji: Optional[Union[str, Emoji, PartialEmoji]] = None,
        default: bool = False,
    ) -> None:
        self.label: str = label
        self.value: str = label if value is MISSING else value
        self.description: Optional[str] = description

        if emoji is not None:
            if isinstance(emoji, str):
                emoji = PartialEmoji.from_str(emoji)
            elif isinstance(emoji, _EmojiTag):
                emoji = emoji._to_partial()
            else:
                raise TypeError(f'expected emoji to be str, Emoji, or PartialEmoji not {emoji.__class__}')

        self.emoji: Optional[Union[str, Emoji, PartialEmoji]] = emoji
        self.default: bool = default

    def __repr__(self) -> str:
        return (
            f'<SelectOption label={self.label!r} value={self.value!r} description={self.description!r} '
            f'emoji={self.emoji!r} default={self.default!r}>'
        )

    def __str__(self) -> str:
        if self.emoji:
            base = f'{self.emoji} {self.label}'
        else:
            base = self.label

        if self.description:
            return f'{base}\n{self.description}'
        return base

    @classmethod
    def from_dict(cls, data: SelectOptionPayload) -> SelectOption:
        try:
            emoji = PartialEmoji.from_dict(data['emoji'])
        except KeyError:
            emoji = None

        return cls(
            label=data['label'],
            value=data['value'],
            description=data.get('description'),
            emoji=emoji,
            default=data.get('default', False),
        )


class TextInput(Component):
    """Represents a text input from the Discord Bot UI Kit.

    .. versionadded:: 2.0

    Attributes
    ------------
    custom_id: Optional[:class:`str`]
        The ID of the text input that gets received during an interaction.
    label: :class:`str`
        The label to display above the text input.
    style: :class:`TextStyle`
        The style of the text input.
    placeholder: Optional[:class:`str`]
        The placeholder text to display when the text input is empty.
    required: :class:`bool`
        Whether the text input is required.
    min_length: Optional[:class:`int`]
        The minimum length of the text input.
    max_length: Optional[:class:`int`]
        The maximum length of the text input.
    """

    __slots__: Tuple[str, ...] = (
        'style',
        'label',
        'custom_id',
        'placeholder',
        '_value',
        '_answer',
        'required',
        'min_length',
        'max_length',
    )

    __repr_info__: ClassVar[Tuple[str, ...]] = __slots__

    def __init__(self, data: TextInputPayload, _=MISSING) -> None:
        self.type: ComponentType = ComponentType.text_input
        self.style: TextStyle = try_enum(TextStyle, data['style'])
        self.label: str = data['label']
        self.custom_id: str = data['custom_id']
        self.placeholder: Optional[str] = data.get('placeholder')
        self._value: Optional[str] = data.get('value')
        self.required: bool = data.get('required', True)
        self.min_length: Optional[int] = data.get('min_length')
        self.max_length: Optional[int] = data.get('max_length')

    def to_dict(self) -> dict:
        return {
            'type': self.type.value,
            'custom_id': self.custom_id,
            'value': self.value,
        }

    @property
    def value(self) -> Optional[str]:
        """Optional[:class:`str`]: The current value of the text input. Defaults to :attr:`default`.

        This can be set to change the answer to the text input.
        """
        return getattr(self, '_answer', self._value)

    @value.setter
    def value(self, value: Optional[str]) -> None:
        length = len(value) if value is not None else 0
        if (self.required or value is not None) and (
            (self.min_length is not None and length < self.min_length)
            or (self.max_length is not None and length > self.max_length)
        ):
            raise ValueError(
                f'value cannot be shorter than {self.min_length or 0} or longer than {self.max_length or "infinity"}'
            )

        self._answer = value

    @property
    def default(self) -> Optional[str]:
        """Optional[:class:`str`]: The default value of the text input."""
        return self._value

    def answer(self, value: Optional[str], /) -> None:
        """A shorthand method to answer the text input.

        Parameters
        ----------
        value: Optional[:class:`str`]
            The value to set the answer to.

        Raises
        ------
        ValueError
            The answer is shorter than :attr:`min_length` or longer than :attr:`max_length`.
        """
        self.value = value


def _component_factory(data: ComponentPayload, message: Message = MISSING) -> Component:
    # The type checker does not properly do narrowing here
    component_type = data['type']
    if component_type == 1:
        return ActionRow(data, message)
    elif component_type == 2:
        return Button(data, message)  # type: ignore
    elif component_type == 3:
        return SelectMenu(data, message)  # type: ignore
    elif component_type == 4:
        return TextInput(data, message)  # type: ignore
    else:
        as_enum = try_enum(ComponentType, component_type)
        return Component._raw_construct(type=as_enum)
