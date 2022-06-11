.. currentmodule:: selfcord

API Reference
===============

The following section outlines the API of selfcord.py's command extension module.

.. _ext_commands_api_bot:

Bots
------

Bot
~~~~

.. attributetable:: selfcord.ext.commands.Bot

.. autoclass:: selfcord.ext.commands.Bot
    :members:
    :inherited-members:
    :exclude-members: after_invoke, before_invoke, check, check_once, command, event, group, listen

    .. automethod:: Bot.after_invoke()
        :decorator:

    .. automethod:: Bot.before_invoke()
        :decorator:

    .. automethod:: Bot.check()
        :decorator:

    .. automethod:: Bot.check_once()
        :decorator:

    .. automethod:: Bot.command(*args, **kwargs)
        :decorator:

    .. automethod:: Bot.event()
        :decorator:

    .. automethod:: Bot.group(*args, **kwargs)
        :decorator:

    .. automethod:: Bot.listen(name=None)
        :decorator:

Prefix Helpers
----------------

.. autofunction:: selfcord.ext.commands.when_mentioned

.. autofunction:: selfcord.ext.commands.when_mentioned_or

.. _ext_commands_api_events:

Event Reference
-----------------

These events function similar to :ref:`the regular events <selfcord-api-events>`, except they
are custom to the command extension module.

.. function:: selfcord.ext.commands.on_command_error(ctx, error)

    An error handler that is called when an error is raised
    inside a command either through user input error, check
    failure, or an error in your own code.

    A default one is provided (:meth:`.Bot.on_command_error`).

    :param ctx: The invocation context.
    :type ctx: :class:`.Context`
    :param error: The error that was raised.
    :type error: :class:`.CommandError` derived

.. function:: selfcord.ext.commands.on_command(ctx)

    An event that is called when a command is found and is about to be invoked.

    This event is called regardless of whether the command itself succeeds via
    error or completes.

    :param ctx: The invocation context.
    :type ctx: :class:`.Context`

.. function:: selfcord.ext.commands.on_command_completion(ctx)

    An event that is called when a command has completed its invocation.

    This event is called only if the command succeeded, i.e. all checks have
    passed and the user input it correctly.

    :param ctx: The invocation context.
    :type ctx: :class:`.Context`

.. _ext_commands_api_command:

Commands
----------

Decorators
~~~~~~~~~~~~

.. autofunction:: selfcord.ext.commands.command
    :decorator:

.. autofunction:: selfcord.ext.commands.group
    :decorator:

Command
~~~~~~~~~

.. attributetable:: selfcord.ext.commands.Command

.. autoclass:: selfcord.ext.commands.Command
    :members:
    :special-members: __call__
    :exclude-members: after_invoke, before_invoke, error

    .. automethod:: Command.after_invoke()
        :decorator:

    .. automethod:: Command.before_invoke()
        :decorator:

    .. automethod:: Command.error()
        :decorator:

Group
~~~~~~

.. attributetable:: selfcord.ext.commands.Group

.. autoclass:: selfcord.ext.commands.Group
    :members:
    :inherited-members:
    :exclude-members: after_invoke, before_invoke, command, error, group

    .. automethod:: Group.after_invoke()
        :decorator:

    .. automethod:: Group.before_invoke()
        :decorator:

    .. automethod:: Group.command(*args, **kwargs)
        :decorator:

    .. automethod:: Group.error()
        :decorator:

    .. automethod:: Group.group(*args, **kwargs)
        :decorator:

GroupMixin
~~~~~~~~~~~

.. attributetable:: selfcord.ext.commands.GroupMixin

.. autoclass:: selfcord.ext.commands.GroupMixin
    :members:
    :exclude-members: command, group

    .. automethod:: GroupMixin.command(*args, **kwargs)
        :decorator:

    .. automethod:: GroupMixin.group(*args, **kwargs)
        :decorator:

.. _ext_commands_api_cogs:

Cogs
------

Cog
~~~~

.. attributetable:: selfcord.ext.commands.Cog

.. autoclass:: selfcord.ext.commands.Cog
    :members:

CogMeta
~~~~~~~~

.. attributetable:: selfcord.ext.commands.CogMeta

.. autoclass:: selfcord.ext.commands.CogMeta
    :members:

.. _ext_commands_help_command:

Help Commands
---------------

HelpCommand
~~~~~~~~~~~~

.. attributetable:: selfcord.ext.commands.HelpCommand

.. autoclass:: selfcord.ext.commands.HelpCommand
    :members:

DefaultHelpCommand
~~~~~~~~~~~~~~~~~~~

.. attributetable:: selfcord.ext.commands.DefaultHelpCommand

.. autoclass:: selfcord.ext.commands.DefaultHelpCommand
    :members:
    :exclude-members: send_bot_help, send_cog_help, send_group_help, send_command_help, prepare_help_command

MinimalHelpCommand
~~~~~~~~~~~~~~~~~~~

.. attributetable:: selfcord.ext.commands.MinimalHelpCommand

.. autoclass:: selfcord.ext.commands.MinimalHelpCommand
    :members:
    :exclude-members: send_bot_help, send_cog_help, send_group_help, send_command_help, prepare_help_command

Paginator
~~~~~~~~~~

.. attributetable:: selfcord.ext.commands.Paginator

.. autoclass:: selfcord.ext.commands.Paginator
    :members:

Enums
------

.. class:: BucketType
    :module: selfcord.ext.commands

    Specifies a type of bucket for, e.g. a cooldown.

    .. attribute:: default

        The default bucket operates on a global basis.
    .. attribute:: user

        The user bucket operates on a per-user basis.
    .. attribute:: guild

        The guild bucket operates on a per-guild basis.
    .. attribute:: channel

        The channel bucket operates on a per-channel basis.
    .. attribute:: member

        The member bucket operates on a per-member basis.
    .. attribute:: category

        The category bucket operates on a per-category basis.
    .. attribute:: role

        The role bucket operates on a per-role basis.

        .. versionadded:: 1.3


.. _ext_commands_api_checks:

Checks
-------

.. autofunction:: selfcord.ext.commands.check(predicate)
    :decorator:

.. autofunction:: selfcord.ext.commands.check_any(*checks)
    :decorator:

.. autofunction:: selfcord.ext.commands.has_role(item)
    :decorator:

.. autofunction:: selfcord.ext.commands.has_permissions(**perms)
    :decorator:

.. autofunction:: selfcord.ext.commands.has_guild_permissions(**perms)
    :decorator:

.. autofunction:: selfcord.ext.commands.has_any_role(*items)
    :decorator:

.. autofunction:: selfcord.ext.commands.bot_has_role(item)
    :decorator:

.. autofunction:: selfcord.ext.commands.bot_has_permissions(**perms)
    :decorator:

.. autofunction:: selfcord.ext.commands.bot_has_guild_permissions(**perms)
    :decorator:

.. autofunction:: selfcord.ext.commands.bot_has_any_role(*items)
    :decorator:

.. autofunction:: selfcord.ext.commands.cooldown(rate, per, type=selfcord.ext.commands.BucketType.default)
    :decorator:

.. autofunction:: selfcord.ext.commands.dynamic_cooldown(cooldown, type=BucketType.default)
    :decorator:

.. autofunction:: selfcord.ext.commands.max_concurrency(number, per=selfcord.ext.commands.BucketType.default, *, wait=False)
    :decorator:

.. autofunction:: selfcord.ext.commands.before_invoke(coro)
    :decorator:

.. autofunction:: selfcord.ext.commands.after_invoke(coro)
    :decorator:

.. autofunction:: selfcord.ext.commands.guild_only(,)
    :decorator:

.. autofunction:: selfcord.ext.commands.dm_only(,)
    :decorator:

.. autofunction:: selfcord.ext.commands.is_owner(,)
    :decorator:

.. autofunction:: selfcord.ext.commands.is_nsfw(,)
    :decorator:

.. _ext_commands_api_context:

Cooldown
---------

.. attributetable:: selfcord.ext.commands.Cooldown

.. autoclass:: selfcord.ext.commands.Cooldown
    :members:

Context
--------

.. attributetable:: selfcord.ext.commands.Context

.. autoclass:: selfcord.ext.commands.Context
    :members:
    :inherited-members:
    :exclude-members: typing

    .. automethod:: selfcord.ext.commands.Context.typing
        :async-with:

.. _ext_commands_api_converters:

Converters
------------

.. autoclass:: selfcord.ext.commands.Converter
    :members:

.. autoclass:: selfcord.ext.commands.ObjectConverter
    :members:

.. autoclass:: selfcord.ext.commands.MemberConverter
    :members:

.. autoclass:: selfcord.ext.commands.UserConverter
    :members:

.. autoclass:: selfcord.ext.commands.MessageConverter
    :members:

.. autoclass:: selfcord.ext.commands.PartialMessageConverter
    :members:

.. autoclass:: selfcord.ext.commands.GuildChannelConverter
    :members:

.. autoclass:: selfcord.ext.commands.TextChannelConverter
    :members:

.. autoclass:: selfcord.ext.commands.VoiceChannelConverter
    :members:

.. autoclass:: selfcord.ext.commands.StageChannelConverter
    :members:

.. autoclass:: selfcord.ext.commands.CategoryChannelConverter
    :members:

.. autoclass:: selfcord.ext.commands.InviteConverter
    :members:

.. autoclass:: selfcord.ext.commands.GuildConverter
    :members:

.. autoclass:: selfcord.ext.commands.RoleConverter
    :members:

.. autoclass:: selfcord.ext.commands.GameConverter
    :members:

.. autoclass:: selfcord.ext.commands.ColourConverter
    :members:

.. autoclass:: selfcord.ext.commands.EmojiConverter
    :members:

.. autoclass:: selfcord.ext.commands.PartialEmojiConverter
    :members:

.. autoclass:: selfcord.ext.commands.ThreadConverter
    :members:

.. autoclass:: selfcord.ext.commands.GuildStickerConverter
    :members:

.. autoclass:: selfcord.ext.commands.ScheduledEventConverter
    :members:

.. autoclass:: selfcord.ext.commands.clean_content
    :members:

.. autoclass:: selfcord.ext.commands.Greedy()

.. autofunction:: selfcord.ext.commands.run_converters

Flag Converter
~~~~~~~~~~~~~~~

.. autoclass:: selfcord.ext.commands.FlagConverter
    :members:

.. autoclass:: selfcord.ext.commands.Flag()
    :members:

.. autofunction:: selfcord.ext.commands.flag


Defaults
--------

.. autoclass:: selfcord.ext.commands.Parameter()
    :members:

.. autofunction:: selfcord.ext.commands.parameter

.. autofunction:: selfcord.ext.commands.param

.. data:: selfcord.ext.commands.Author

    A default :class:`.Parameter` which returns the :attr:`~.Context.author` for this context.

    .. versionadded:: 2.0

.. data:: selfcord.ext.commands.CurrentChannel

    A default :class:`.Parameter` which returns the :attr:`~.Context.channel` for this context.

    .. versionadded:: 2.0

.. data:: selfcord.ext.commands.CurrentGuild

    A default :class:`.Parameter` which returns the :attr:`~.Context.guild` for this context. This will never be ``None``. If the command is called in a DM context then :exc:`~selfcord.ext.commands.NoPrivateMessage` is raised to the error handlers.

    .. versionadded:: 2.0

.. _ext_commands_api_errors:

Exceptions
-----------

.. autoexception:: selfcord.ext.commands.CommandError
    :members:

.. autoexception:: selfcord.ext.commands.ConversionError
    :members:

.. autoexception:: selfcord.ext.commands.MissingRequiredArgument
    :members:

.. autoexception:: selfcord.ext.commands.ArgumentParsingError
    :members:

.. autoexception:: selfcord.ext.commands.UnexpectedQuoteError
    :members:

.. autoexception:: selfcord.ext.commands.InvalidEndOfQuotedStringError
    :members:

.. autoexception:: selfcord.ext.commands.ExpectedClosingQuoteError
    :members:

.. autoexception:: selfcord.ext.commands.BadArgument
    :members:

.. autoexception:: selfcord.ext.commands.BadUnionArgument
    :members:

.. autoexception:: selfcord.ext.commands.BadLiteralArgument
    :members:

.. autoexception:: selfcord.ext.commands.PrivateMessageOnly
    :members:

.. autoexception:: selfcord.ext.commands.NoPrivateMessage
    :members:

.. autoexception:: selfcord.ext.commands.CheckFailure
    :members:

.. autoexception:: selfcord.ext.commands.CheckAnyFailure
    :members:

.. autoexception:: selfcord.ext.commands.CommandNotFound
    :members:

.. autoexception:: selfcord.ext.commands.DisabledCommand
    :members:

.. autoexception:: selfcord.ext.commands.CommandInvokeError
    :members:

.. autoexception:: selfcord.ext.commands.TooManyArguments
    :members:

.. autoexception:: selfcord.ext.commands.UserInputError
    :members:

.. autoexception:: selfcord.ext.commands.CommandOnCooldown
    :members:

.. autoexception:: selfcord.ext.commands.MaxConcurrencyReached
    :members:

.. autoexception:: selfcord.ext.commands.NotOwner
    :members:

.. autoexception:: selfcord.ext.commands.MessageNotFound
    :members:

.. autoexception:: selfcord.ext.commands.MemberNotFound
    :members:

.. autoexception:: selfcord.ext.commands.GuildNotFound
    :members:

.. autoexception:: selfcord.ext.commands.UserNotFound
    :members:

.. autoexception:: selfcord.ext.commands.ChannelNotFound
    :members:

.. autoexception:: selfcord.ext.commands.ChannelNotReadable
    :members:

.. autoexception:: selfcord.ext.commands.ThreadNotFound
    :members:

.. autoexception:: selfcord.ext.commands.BadColourArgument
    :members:

.. autoexception:: selfcord.ext.commands.RoleNotFound
    :members:

.. autoexception:: selfcord.ext.commands.BadInviteArgument
    :members:

.. autoexception:: selfcord.ext.commands.EmojiNotFound
    :members:

.. autoexception:: selfcord.ext.commands.PartialEmojiConversionFailure
    :members:

.. autoexception:: selfcord.ext.commands.GuildStickerNotFound
    :members:

.. autoexception:: selfcord.ext.commands.ScheduledEventNotFound
    :members:

.. autoexception:: selfcord.ext.commands.BadBoolArgument
    :members:

.. autoexception:: selfcord.ext.commands.MissingPermissions
    :members:

.. autoexception:: selfcord.ext.commands.BotMissingPermissions
    :members:

.. autoexception:: selfcord.ext.commands.MissingRole
    :members:

.. autoexception:: selfcord.ext.commands.BotMissingRole
    :members:

.. autoexception:: selfcord.ext.commands.MissingAnyRole
    :members:

.. autoexception:: selfcord.ext.commands.BotMissingAnyRole
    :members:

.. autoexception:: selfcord.ext.commands.NSFWChannelRequired
    :members:

.. autoexception:: selfcord.ext.commands.FlagError
    :members:

.. autoexception:: selfcord.ext.commands.BadFlagArgument
    :members:

.. autoexception:: selfcord.ext.commands.MissingFlagArgument
    :members:

.. autoexception:: selfcord.ext.commands.TooManyFlags
    :members:

.. autoexception:: selfcord.ext.commands.MissingRequiredFlag
    :members:

.. autoexception:: selfcord.ext.commands.ExtensionError
    :members:

.. autoexception:: selfcord.ext.commands.ExtensionAlreadyLoaded
    :members:

.. autoexception:: selfcord.ext.commands.ExtensionNotLoaded
    :members:

.. autoexception:: selfcord.ext.commands.NoEntryPointError
    :members:

.. autoexception:: selfcord.ext.commands.ExtensionFailed
    :members:

.. autoexception:: selfcord.ext.commands.ExtensionNotFound
    :members:

.. autoexception:: selfcord.ext.commands.CommandRegistrationError
    :members:


Exception Hierarchy
~~~~~~~~~~~~~~~~~~~~~

.. exception_hierarchy::

    - :exc:`~.DiscordException`
        - :exc:`~.commands.CommandError`
            - :exc:`~.commands.ConversionError`
            - :exc:`~.commands.UserInputError`
                - :exc:`~.commands.MissingRequiredArgument`
                - :exc:`~.commands.TooManyArguments`
                - :exc:`~.commands.BadArgument`
                    - :exc:`~.commands.MessageNotFound`
                    - :exc:`~.commands.MemberNotFound`
                    - :exc:`~.commands.GuildNotFound`
                    - :exc:`~.commands.UserNotFound`
                    - :exc:`~.commands.ChannelNotFound`
                    - :exc:`~.commands.ChannelNotReadable`
                    - :exc:`~.commands.BadColourArgument`
                    - :exc:`~.commands.RoleNotFound`
                    - :exc:`~.commands.BadInviteArgument`
                    - :exc:`~.commands.EmojiNotFound`
                    - :exc:`~.commands.GuildStickerNotFound`
                    - :exc:`~.commands.ScheduledEventNotFound`
                    - :exc:`~.commands.PartialEmojiConversionFailure`
                    - :exc:`~.commands.BadBoolArgument`
                    - :exc:`~.commands.ThreadNotFound`
                    - :exc:`~.commands.FlagError`
                        - :exc:`~.commands.BadFlagArgument`
                        - :exc:`~.commands.MissingFlagArgument`
                        - :exc:`~.commands.TooManyFlags`
                        - :exc:`~.commands.MissingRequiredFlag`
                - :exc:`~.commands.BadUnionArgument`
                - :exc:`~.commands.BadLiteralArgument`
                - :exc:`~.commands.ArgumentParsingError`
                    - :exc:`~.commands.UnexpectedQuoteError`
                    - :exc:`~.commands.InvalidEndOfQuotedStringError`
                    - :exc:`~.commands.ExpectedClosingQuoteError`
            - :exc:`~.commands.CommandNotFound`
            - :exc:`~.commands.CheckFailure`
                - :exc:`~.commands.CheckAnyFailure`
                - :exc:`~.commands.PrivateMessageOnly`
                - :exc:`~.commands.NoPrivateMessage`
                - :exc:`~.commands.NotOwner`
                - :exc:`~.commands.MissingPermissions`
                - :exc:`~.commands.BotMissingPermissions`
                - :exc:`~.commands.MissingRole`
                - :exc:`~.commands.BotMissingRole`
                - :exc:`~.commands.MissingAnyRole`
                - :exc:`~.commands.BotMissingAnyRole`
                - :exc:`~.commands.NSFWChannelRequired`
            - :exc:`~.commands.DisabledCommand`
            - :exc:`~.commands.CommandInvokeError`
            - :exc:`~.commands.CommandOnCooldown`
            - :exc:`~.commands.MaxConcurrencyReached`
        - :exc:`~.commands.ExtensionError`
            - :exc:`~.commands.ExtensionAlreadyLoaded`
            - :exc:`~.commands.ExtensionNotLoaded`
            - :exc:`~.commands.NoEntryPointError`
            - :exc:`~.commands.ExtensionFailed`
            - :exc:`~.commands.ExtensionNotFound`
    - :exc:`~.ClientException`
        - :exc:`~.commands.CommandRegistrationError`
