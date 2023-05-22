"""
Optional Parameters

:author: Doug Skrypa
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from functools import partial, update_wrapper
from typing import TYPE_CHECKING, Any, Optional, Callable, Union, TypeVar, Tuple

from ..context import ctx
from ..exceptions import ParameterDefinitionError, BadArgument, CommandDefinitionError, ParamUsageError, ParamConflict
from ..inputs import normalize_input_type
from ..nargs import Nargs, NargsValue
from ..typing import T_co, TypeFunc
from ..utils import _NotSet, ValueSource, str_to_bool
from .base import BasicActionMixin, BaseOption, parameter_action
from .option_strings import TriFlagOptionStrings

if TYPE_CHECKING:
    from ..typing import Bool, ChoicesType, InputTypeFunc, CommandCls, CommandObj, OptStr, ValSrc, LeadingDash

__all__ = ['Option', 'Flag', 'TriFlag', 'ActionFlag', 'Counter', 'action_flag', 'before_main', 'after_main']
log = logging.getLogger(__name__)

TD = TypeVar('TD')
TC = TypeVar('TC')
TA = TypeVar('TA')


class Option(BasicActionMixin, BaseOption[Union[T_co, TD]]):
    """
    A generic option that can be specified as ``--foo bar`` or by using other similar forms.

    :param option_strs: The long and/or short option prefixes for this option.  If no long prefixes are specified,
      then one will automatically be added based on the name assigned to this parameter.
    :param nargs: The number of values that are expected/required when this parameter is specified.  Defaults to ``+``
      when ``action='append'``, and to ``1`` otherwise. See :class:`.Nargs` for more info.
    :param action: The action to take on individual parsed values.  Actions must be defined as methods in classes
      that extend Parameter, and must be registered via :class:`.parameter_action`.  Defaults to ``store`` when
      ``nargs=1``, and to ``append`` otherwise.  A single value will be stored when ``action='store'``, and a list
      of values will be stored when ``action='append'``.
    :param default: The default value for this parameter if it is not specified.  Defaults to ``None`` if
      this parameter is not required; not used if it is required.
    :param required: Whether this parameter is required or not.  If it is required, then an exception will be
      raised if the user did not provide a value for this parameter.  Defaults to ``False``.
    :param type: A callable (function, class, etc.) that accepts a single string argument, which should be called
      on every value for this parameter to transform the value.  By default, no transformation is performed, and
      values will be strings.  If not specified, but a type annotation is detected, then that annotation will be
      used as if it was provided here.  When both are present, this argument takes precedence.
    :param choices: A container that holds the specific values that users must pick from.  By default, any value is
      allowed.
    :param allow_leading_dash: Whether string values may begin with a dash (``-``).  By default, if a value begins with
      a dash, it is only accepted if it appears to be a negative numeric value.  Use ``True`` / ``always`` /
      ``AllowLeadingDash.ALWAYS`` to allow any value that begins with a dash (as long as it is not an option string for
      an Option/Flag/etc).  To reject all values beginning with a dash, including numbers, use ``False`` / ``never`` /
      ``AllowLeadingDash.NEVER``.
    :param kwargs: Additional keyword arguments to pass to :class:`.BaseOption`.
    """

    default: TD

    def __init__(
        self,
        *option_strs: str,
        nargs: NargsValue = None,
        action: str = _NotSet,
        default: TD = _NotSet,
        required: Bool = False,
        type: InputTypeFunc = None,  # noqa
        choices: ChoicesType = None,
        allow_leading_dash: LeadingDash = None,
        **kwargs,
    ):
        if nargs is not None:
            self.nargs = nargs = Nargs(nargs)
        elif action == 'append':
            self.nargs = nargs = Nargs('+')
        else:
            nargs = self.nargs  # default: Nargs(1)

        if 0 in nargs:
            nargs = nargs._orig
            details = 'use Flag or Counter for Options that can be specified without a value'
            if isinstance(nargs, range) and nargs.start == 0 and nargs.step != nargs.stop:
                suffix = f', {nargs.step}' if nargs.step != 1 else ''
                details = f'try using range({nargs.step}, {nargs.stop}{suffix}) instead, or {details}'
            raise ParameterDefinitionError(f'Invalid {nargs=} - {details}')

        if action is _NotSet:
            action = 'store' if nargs == 1 else 'append'
        elif action == 'store' and nargs != 1:
            raise ParameterDefinitionError(f'Invalid {nargs=} for {action=}')
        elif action in ('store_const', 'append_const'):
            raise ParameterDefinitionError(f'Invalid {action=} for {self.__class__.__name__} - use Flag instead')

        super().__init__(*option_strs, action=action, default=default, required=required, **kwargs)
        self.type = normalize_input_type(type, choices)
        self._validate_nargs_and_allow_leading_dash(allow_leading_dash)


class _Flag(BaseOption[T_co], ABC):
    nargs = Nargs(0)
    type = staticmethod(str_to_bool)  # Without staticmethod, this would be interpreted as a normal method
    strict_env: bool
    use_env_value: bool = False
    _use_opt_str: bool = False

    def __init_subclass__(cls, use_opt_str: bool = False, **kwargs):  # pylint: disable=W0222
        super().__init_subclass__(**kwargs)
        cls._use_opt_str = use_opt_str

    def __init__(
        self,
        *option_strs: str,
        type: TypeFunc = None,  # noqa
        strict_env: bool = True,
        use_env_value: bool = False,
        **kwargs,
    ):
        if 'metavar' in kwargs:
            raise TypeError(f"{self.__class__.__name__}.__init__() got an unexpected keyword argument: 'metavar'")
        super().__init__(*option_strs, **kwargs)
        self.strict_env = strict_env
        if use_env_value:
            self.use_env_value = use_env_value
        if type is not None:
            self.type = type

    def _init_value_factory(self):
        if self.action == 'store_const':
            return self.default
        else:
            return []

    def take_action(
        self, value: Optional[str], short_combo: bool = False, opt_str: str = None, src: ValSrc = ValueSource.CLI
    ):
        # log.debug(f'{self!r}.take_action({value!r})')
        ctx.record_action(self)
        if value is None:
            action_method = getattr(self, self.action)
            return action_method(opt_str) if self._use_opt_str else action_method()
        elif src != ValueSource.CLI:
            src, env_var = src
            try:
                return self.take_env_var_action(value, env_var)
            except ParamUsageError as e:
                if not self.strict_env:
                    log.warning(e)
                    return
                raise

        raise ParamUsageError(self, f'received {value=} but no values are accepted for action={self.action!r}')

    def prepare_env_var_value(self, value: str, env_var: str) -> T_co:
        try:
            return self.type(value)
        except Exception as e:
            raise ParamUsageError(self, f'unable to parse {value=} from {env_var=}: {e}') from e

    @abstractmethod
    def take_env_var_action(self, value: str, env_var: str):
        raise NotImplementedError

    def would_accept(self, value: Optional[str], short_combo: bool = False) -> bool:  # noqa
        return value is None

    def result_value(self, missing_default=_NotSet) -> Any:
        return ctx.get_parsed_value(self)

    result = result_value


class Flag(_Flag[Union[TD, TC]], accepts_values=False, accepts_none=True):
    """
    A (typically boolean) option that does not accept any values.

    :param option_strs: The long and/or short option prefixes for this option.  If no long prefixes are specified,
      then one will automatically be added based on the name assigned to this parameter.
    :param action: The action to take on individual parsed values.  Actions must be defined as methods in classes
      that extend Parameter, and must be registered via :class:`.parameter_action`.  Defaults to ``store_const``, but
      accepts ``append_const`` to build a list of the specified constant.
    :param default: The default value for this parameter if it is not specified.  Defaults to ``False`` when
      ``const=True`` (the default), and to ``True`` when ``const=False``.  Defaults to ``None`` for any other
      constant.
    :param const: The constant value to store/append when this parameter is specified.  Defaults to ``True``.
    :param type: A callable (function, class, etc.) that accepts a single string argument and returns a boolean value,
      which should be called on environment variable values, if any are configured for this Flag via
      :paramref:`.BaseOption.env_var`.  It should return a truthy value if any action should be taken (i.e., if the
      constant should be stored/appended), or a falsey value for no action to be taken.  The
      :func:`default function<.str_to_bool>` handles parsing ``1`` / ``true`` / ``yes`` and similar as ``True``,
      and ``0`` / ``false`` / ``no`` and similar as ``False``.  If :paramref:`use_env_value` is ``True``, then this
      function should return either the default or constant value instead.
    :param strict_env: When ``True`` (the default), if an :paramref:`.BaseOption.env_var` is used as the source of a
      value for this parameter and that value is invalid, then parsing will fail.  When ``False``, invalid values from
      environment variables will be ignored (and a warning message will be logged).
    :param use_env_value: If ``True``, when an :paramref:`.BaseOption.env_var` is used as the source of a value for
      this Flag, the parsed value will be stored as this Flag's value (it must match either the default or constant
      value).  If ``False`` (the default), then the parsed value will be used to determine whether this Flag's normal
      action should be taken as if it was specified via a CLI argument.
    :param kwargs: Additional keyword arguments to pass to :class:`.BaseOption`.
    """

    __default_const_map = {True: False, False: True, _NotSet: True}
    default: TD
    const: TC

    def __init__(
        self, *option_strs: str, action: str = 'store_const', default: TD = _NotSet, const: TC = _NotSet, **kwargs
    ):
        if const is _NotSet:
            try:
                const = self.__default_const_map[default]
            except KeyError as e:
                raise ParameterDefinitionError(
                    f"A 'const' value is required for {self.__class__.__name__} since {default=} is not True or False"
                ) from e
        if default is _NotSet:
            default = self.__default_const_map.get(const)  # will be True, False, or None
        if default is False:  # Avoid surprises for custom non-truthy values
            kwargs.setdefault('show_default', False)
        super().__init__(*option_strs, action=action, default=default, **kwargs)
        self.const = const

    def take_env_var_action(self, value: str, env_var: str):
        parsed = self.prepare_env_var_value(value, env_var)
        if self.use_env_value:
            if parsed == self.const:
                getattr(self, self.action)()
            elif parsed != self.default:
                raise BadArgument(self, f'invalid value={parsed!r} from {env_var=}')
        elif parsed:
            getattr(self, self.action)()

    @parameter_action
    def store_const(self):
        ctx.set_parsed_value(self, self.const)

    @parameter_action
    def append_const(self):
        ctx.get_parsed_value(self).append(self.const)


class TriFlag(_Flag[Union[TD, TC, TA]], accepts_values=False, accepts_none=True, use_opt_str=True):
    """
    A trinary / ternary Flag.  While :class:`.Flag` only supports 1 constant when provided, with 1 default if not
    provided, this class accepts a pair of constants for the primary and alternate values to store, along with a
    separate default.

    :param option_strs: The primary long and/or short option prefixes for this option.  If no long prefixes are
      specified, then one will automatically be added based on the name assigned to this parameter.
    :param consts: A 2-tuple containing the ``(primary, alternate)`` values to store.  Defaults to ``(True, False)``.
    :param alt_prefix: The prefix to add to the assigned name for the alternate long form.  Ignored if ``alt_long`` is
      specified.  Defaults to ``no`` if ``alt_long`` is not specified.
    :param alt_long: The alternate long form to use.
    :param alt_short: The alternate short form to use.
    :param alt_help: The help text to display with the alternate option strings.
    :param action: The action to take on individual parsed values.  Only ``store_const`` (the default) is supported.
    :param default: The default value to use if neither the primary or alternate options are provided.  Defaults
      to None.
    :param name_mode: Override the configured :ref:`configuration:Parsing Options:option_name_mode` for this TriFlag.
    :param type: A callable (function, class, etc.) that accepts a single string argument and returns a boolean value,
      which should be called on environment variable values, if any are configured for this TriFlag via
      :paramref:`.BaseOption.env_var`.  It should return a truthy value if the primary constant should be stored, or a
      falsey value if the alternate constant should be stored.  The :func:`default function<.str_to_bool>` handles
      parsing ``1`` / ``true`` / ``yes`` and similar as ``True``, and ``0`` / ``false`` / ``no`` and similar
      as ``False``.  If :paramref:`use_env_value` is ``True``, then this function should return the primary or
      alternate constant or the default value instead.
    :param strict_env: When ``True`` (the default), if an :paramref:`.BaseOption.env_var` is used as the source of a
      value for this parameter and that value is invalid, then parsing will fail.  When ``False``, invalid values from
      environment variables will be ignored (and a warning message will be logged).
    :param use_env_value: If ``True``, when an :paramref:`.BaseOption.env_var` is used as the source of a value for
      this TriFlag, the parsed value will be stored as this TriFlag's value (it must match the primary or alternate
      constant, or the default value).  If ``False`` (the default), then the parsed value will be used to determine
      whether this TriFlag's normal action should be taken as if it was specified via a CLI argument.
    :param kwargs: Additional keyword arguments to pass to :class:`.BaseOption`.
    """

    _opt_str_cls = TriFlagOptionStrings
    option_strs: TriFlagOptionStrings
    alt_help: OptStr = None
    default: TD
    consts: Tuple[TC, TA]

    def __init__(
        self,
        *option_strs: str,
        consts: Tuple[TC, TA] = (True, False),
        alt_prefix: str = None,
        alt_long: str = None,
        alt_short: str = None,
        alt_help: str = None,
        action: str = 'store_const',
        default: TD = _NotSet,
        **kwargs,
    ):
        if alt_short and '-' in alt_short[1:]:
            raise ParameterDefinitionError(f"Bad alt_short option - may not contain '-': {alt_short}")
        elif alt_prefix and ('=' in alt_prefix or alt_prefix.startswith('-')):
            raise ParameterDefinitionError(f"Bad alt_prefix - may not contain '=' or start with '-': {alt_prefix}")
        elif not alt_prefix and not alt_long:
            alt_prefix = 'no'

        try:
            _pos, _neg = consts
        except (ValueError, TypeError) as e:
            msg = f'Invalid {consts=} - expected a 2-tuple of (positive, negative) constants to store'
            raise ParameterDefinitionError(msg) from e

        if default is _NotSet and not kwargs.get('required', False):
            default = None
        if default in consts:
            raise ParameterDefinitionError(
                f'Invalid {default=} with {consts=} - the default must not match either value'
            )

        alt_opt_strs = (opt for opt in (alt_short, alt_long) if opt)
        super().__init__(*option_strs, *alt_opt_strs, action=action, default=default, **kwargs)
        self.consts = consts
        self.option_strs.add_alts(alt_prefix, alt_long, alt_short)
        if alt_help:
            self.alt_help = alt_help

    def __set_name__(self, command: CommandCls, name: str):
        super().__set_name__(command, name)
        self.option_strs.update_alts(name)

    def _get_const(self, opt_str: str) -> Union[TC, TA]:
        if opt_str in self.option_strs.alt_allowed:
            return self.consts[1]
        else:
            return self.consts[0]

    @parameter_action
    def store_const(self, opt_str: str):
        self._store_const(self._get_const(opt_str))

    def _store_const(self, const: Union[TC, TA]):
        ctx.set_parsed_value(self, const)

    def take_action(
        self, value: Optional[str], short_combo: bool = False, opt_str: str = None, src: ValSrc = ValueSource.CLI
    ):
        if value is None:
            prev_parsed = ctx.get_parsed_value(self)
            const = self._get_const(opt_str)
            if prev_parsed is not self.default and prev_parsed != const:
                raise ParamConflict([self])
        return super().take_action(value, short_combo, opt_str, src)

    def take_env_var_action(self, value: str, env_var: str):
        parsed = self.prepare_env_var_value(value, env_var)
        if self.use_env_value:
            if parsed in self.consts:
                self._store_const(parsed)
            elif parsed != self.default:
                raise BadArgument(self, f'invalid value={parsed!r} from {env_var=}')
        else:
            self._store_const(self.consts[0] if parsed else self.consts[1])


# region Action Flag


class ActionFlag(Flag, repr_attrs=('order', 'before_main')):
    """
    A :class:`.Flag` that triggers the execution of a function / method / other callable when specified.

    :param option_strs: The long and/or short option prefixes for this option.  If no long prefixes are specified,
      then one will automatically be added based on the name assigned to this parameter.
    :param order: The priority / order in which this ActionFlag should be executed, relative to other ActionFlags, if
      others would also be executed.  Two ActionFlags in a given :class:`.Command` may not have the same combination
      of ``before_main`` and ``order`` values.  ActionFlags with lower ``order`` values are executed before those with
      higher values.  The ``--help`` action is implemented as an ActionFlag with ``order=float('-inf')``.
    :param func: The function to execute when this parameter is specified.
    :param before_main: Whether this ActionFlag should be executed before the :meth:`.Command.main` method or
      after it.
    :param always_available: Whether this ActionFlag should always be available to be called, even if parsing
      failed.  Only allowed when ``before_main=True``.  The intended use case is for actions like ``--help`` text.
    :param kwargs: Additional keyword arguments to pass to :class:`.Flag`.
    """

    def __init__(
        self,
        *option_strs: str,
        order: Union[int, float] = 1,
        func: Callable = None,
        before_main: Bool = True,  # noqa  # pylint: disable=W0621
        always_available: Bool = False,
        **kwargs,
    ):
        expected = {'action': 'store_const', 'default': False, 'const': _NotSet}
        if bad := {k: fv for k, ev in expected.items() if (fv := kwargs.setdefault(k, ev)) != ev}:
            raise ParameterDefinitionError(f'Unsupported kwargs for {self.__class__.__name__}: {bad}')
        elif always_available and not before_main:
            raise ParameterDefinitionError('always_available=True cannot be combined with before_main=False')
        super().__init__(*option_strs, **kwargs)
        self.func = func
        self.order = order
        self.before_main = before_main
        self.always_available = always_available

    @property
    def func(self):
        return self._func

    @func.setter
    def func(self, func: Optional[Callable]):
        self._func = func
        if func is not None:
            if self.help is None:
                try:
                    self.help = func.__doc__
                except AttributeError:
                    pass
            update_wrapper(self, func)

    def __hash__(self) -> int:
        result = hash(self.__class__)
        for attr in (self.name, self.command, self.func, self.order, self.before_main):
            result ^= hash(attr)
        return result

    def __eq__(self, other: ActionFlag) -> bool:
        if not isinstance(other, ActionFlag):
            return NotImplemented
        return all(getattr(self, a) == getattr(other, a) for a in ('name', 'func', 'command', 'order', 'before_main'))

    def __lt__(self, other: ActionFlag) -> bool:
        if not isinstance(other, ActionFlag):
            return NotImplemented
        # noinspection PyTypeChecker
        return (not self.before_main, self.order, self.name) < (not other.before_main, other.order, other.name)

    def __call__(self, func: Callable) -> ActionFlag:
        """
        Allows use as a decorator on the method to be called.  A given method can only be decorated with one ActionFlag.

        If stacking :class:`.Action` and :class:`.ActionFlag` decorators, the Action decorator must be first (i.e., the
        ActionFlag decorator must be above the Action decorator).
        """
        if self.func is not None:
            raise CommandDefinitionError(f'Cannot re-assign the func to call for {self}')
        self.func = func
        return self

    def __get__(self, command: Optional[CommandObj], owner: CommandCls) -> Union[ActionFlag, Callable]:
        # Allow the method to be called, regardless of whether it was specified
        if command is None:
            return self
        return partial(self.func, command)  # imitates a bound method

    def result(self) -> Optional[Callable]:
        if self.result_value():
            if func := self.func:
                return func
            raise ParameterDefinitionError(f'No function was registered for {self}')
        return None


#: Alias for :class:`ActionFlag`
action_flag = ActionFlag  # pylint: disable=C0103


def before_main(*option_strs: str, order: Union[int, float] = 1, func: Callable = None, **kwargs) -> ActionFlag:
    """An ActionFlag that will be executed before :meth:`.Command.main`"""
    return ActionFlag(*option_strs, order=order, func=func, before_main=True, **kwargs)


def after_main(*option_strs: str, order: Union[int, float] = 1, func: Callable = None, **kwargs) -> ActionFlag:
    """An ActionFlag that will be executed after :meth:`.Command.main`"""
    return ActionFlag(*option_strs, order=order, func=func, before_main=False, **kwargs)


# endregion


class Counter(BaseOption[int], accepts_values=True, accepts_none=True):
    """
    A :class:`.Flag`-like option that counts the number of times it was specified.  Supports an optional integer value
    to explicitly increase the stored value by that amount.

    :param option_strs: The long and/or short option prefixes for this option.  If no long prefixes are specified,
      then one will automatically be added based on the name assigned to this parameter.
    :param action: The action to take on individual parsed values.  Defaults to ``append``, and no other actions
      are supported (unless this class is extended).
    :param default: The default value for this parameter if it is not specified.  This value is also be used as the
      initial value that will be incremented when this parameter is specified.  Defaults to ``0``.
    :param const: The value by which the stored value should increase whenever this parameter is specified.
      Defaults to ``1``.  If a different ``const`` value is used, and if an explicit value is provided by a user,
      the user-provided value will be added verbatim - it will NOT be multiplied by ``const``.
    :param kwargs: Additional keyword arguments to pass to :class:`.BaseOption`.
    """

    type = int
    nargs = Nargs('?')

    def __init__(self, *option_strs: str, action: str = 'append', default: int = 0, const: int = 1, **kwargs):
        vals = {'const': const, 'default': default}
        if bad_types := ', '.join(f'{k}={v!r}' for k, v in vals.items() if not isinstance(v, self.type)):
            raise ParameterDefinitionError(f'Invalid type for parameters (expected int): {bad_types}')
        super().__init__(*option_strs, action=action, default=default, **kwargs)
        self.const = const

    def _init_value_factory(self):
        return self.default

    def prepare_value(self, value: Optional[str], short_combo: bool = False, pre_action: bool = False) -> int:
        if value is None:
            return self.const
        try:
            return self.type(value)
        except (ValueError, TypeError) as e:
            combinable = self.option_strs.combinable
            if short_combo and combinable and all(c in combinable for c in value):
                return len(value) + 1  # +1 for the -short that preceded this value
            raise BadArgument(self, f'bad counter {value=}') from e

    @parameter_action
    def append(self, value: Optional[int]):
        if value is None:
            value = self.const
        ctx.increment_parsed_value(self, value)

    def validate(self, value: Any):
        if value is None or isinstance(value, self.type):
            return
        try:
            value = self.type(value)
        except (ValueError, TypeError) as e:
            raise BadArgument(self, f'invalid {value=} (expected an integer)') from e
        else:
            return

    def result_value(self, missing_default=_NotSet) -> int:
        return ctx.get_parsed_value(self)

    result = result_value
