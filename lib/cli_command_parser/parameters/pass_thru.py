"""
PassThru Parameters

:author: Doug Skrypa
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..context import ctx
from ..exceptions import ParamUsageError, MissingArgument
from ..nargs import Nargs
from ..utils import _NotSet, ValueSource
from .base import Parameter, parameter_action

if TYPE_CHECKING:
    from ..typing import Strings, ValSrc

__all__ = ['PassThru']


class PassThru(Parameter):
    """
    Collects all remaining arguments, without processing them.  Must be preceded by ``--`` and a space.

    :param action: The action to take on individual parsed values.  Only ``store_all`` (the default) is supported
      for this parameter type.
    :param kwargs: Additional keyword arguments to pass to :class:`.Parameter`.
    """

    nargs = Nargs('REMAINDER')
    missing_hint: str = " (missing pass thru args separated from others with '--')"  # leading space is intentional

    def __init__(self, action: str = 'store_all', **kwargs):
        super().__init__(action=action, **kwargs)

    def _init_default(self):
        return _NotSet if self.required else None

    @parameter_action
    def store_all(self, values: Strings):
        ctx.set_parsed_value(self, values)

    def take_action(  # pylint: disable=W0237
        self, values: Strings, short_combo: bool = False, opt_str: str = None, src: ValSrc = ValueSource.CLI
    ):
        if (value := ctx.get_parsed_value(self)) is not _NotSet:
            raise ParamUsageError(
                self, f'can only be specified once - found {values=} but a stored {value=} already exists'
            )

        ctx.record_action(self)
        normalized = list(map(self.prepare_value, values))
        return getattr(self, self._action_name)(normalized)

    def result_value(self, missing_default=_NotSet) -> Any:
        if (value := ctx.get_parsed_value(self)) is _NotSet:
            if self.required:
                if missing_default is _NotSet:
                    raise MissingArgument(self)
                return missing_default
            return self.default
        return value

    result = result_value
