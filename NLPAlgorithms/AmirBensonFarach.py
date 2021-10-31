import itertools
import math
from typing import Callable, List, NamedTuple, Sequence, Tuple, Union, Iterable, Optional, Any

from multiset import Multiset

from .expressions.expressions import (
    Expression, Operation, Pattern, Wildcard, SymbolWildcard, AssociativeOperation, CommutativeOperation
)
from .expressions.substitution import Substitution
from .expressions.functions import preorder_iter_with_position, create_operation_expression, op_iter, op_len
from .matching.one_to_one import match

__all__ = ['substitute', 'replace', 'replace_all', 'replace_many', 'is_match', 'ReplacementRule', 'replace_all_post_order']

Replacement = Union[Expression, List[Expression]]


def substitute(expression: Union[Expression, Pattern], substitution: Substitution,
               sort_key: Optional[Callable[[Expression], Any]] = None) -> Replacement:
    
    if isinstance(expression, Pattern):
        expression = expression.expression
    return _substitute(expression, substitution, sort_key)[0]


def _substitute(expression: Expression, substitution: Substitution,
                sort_key: Optional[Callable[[Expression], Any]] = None) -> Tuple[Replacement, bool]:
    if getattr(expression, 'variable_name', False) and expression.variable_name in substitution:
        return substitution[expression.variable_name], True
    elif isinstance(expression, Operation):
        any_replaced = False
        new_operands = []
        for operand in op_iter(expression):
            result, replaced = _substitute(operand, substitution)
            if replaced:
                any_replaced = True
            if isinstance(result, (list, tuple)):
                new_operands.extend(result)
            elif isinstance(result, Multiset):
                if sort_key is not None:
                    new_operands.extend(sorted(result, key=sort_key))
                else:
                    new_operands.extend(sorted(result))
            else:
                new_operands.append(result)
        if any_replaced:
            return create_operation_expression(expression, new_operands), True

    return expression, False


def replace(expression: Expression, position: Sequence[int], replacement: Replacement) -> Replacement:r
    if len(position) == 0:
        return replacement
    if not isinstance(expression, Operation):
        raise IndexError("Invalid position {!r} for expression {!s}".format(position, expression))
    if position[0] >= op_len(expression):
        raise IndexError("Position {!r} out of range for expression {!s}".format(position, expression))
    pos = position[0]
    operands = list(op_iter(expression))
    subexpr = replace(operands[pos], position[1:], replacement)
    if isinstance(subexpr, Sequence):
        new_operands = tuple(operands[:pos]) + tuple(subexpr) + tuple(operands[pos + 1:])
        return create_operation_expression(expression, new_operands)
    operands[pos] = subexpr
    return create_operation_expression(expression, operands)


def replace_many(expression: Expression, replacements: Sequence[Tuple[Sequence[int], Replacement]]) -> Replacement:r
    if len(replacements) == 0:
        return expression
    replacements = sorted(replacements)
    if len(replacements[0][0]) == 0:
        if len(replacements) > 1:
            raise IndexError(
                "Cannot replace child positions for expression {}, got {!r}".format(expression, replacements[1:])
            )
        return replacements[0][1]
    if len(replacements) == 1:
        return replace(expression, replacements[0][0], replacements[0][1])
    if not isinstance(expression, Operation):
        raise IndexError("Invalid replacements {!r} for expression {!s}".format(replacements, expression))
    operands = list(op_iter(expression))
    new_operands = []
    last_index = 0
    for index, group in itertools.groupby(replacements, lambda r: r[0][0]):
        new_operands.extend(operands[last_index:index])
        replacements = [(pos[1:], r) for pos, r in group]
        if len(replacements) == 1:
            replacement = replace(operands[index], replacements[0][0], replacements[0][1])
        else:
            replacement = replace_many(operands[index], replacements)
        if isinstance(replacement, (list, tuple, Multiset)):
            new_operands.extend(replacement)
        else:
            new_operands.append(replacement)
        last_index = index + 1
    new_operands.extend(operands[last_index:len(operands)])
    return create_operation_expression(expression, new_operands)


ReplacementRule = NamedTuple('ReplacementRule', [('pattern', Pattern), ('replacement', Callable[..., Expression])])


def replace_all(expression: Expression, rules: Iterable[ReplacementRule], max_count: int=math.inf) \
        -> Union[Expression, Sequence[Expression]]:
    
    rules = [ReplacementRule(pattern, replacement) for pattern, replacement in rules]
    expression = expression
    replaced = True
    replace_count = 0
    while replaced and replace_count < max_count:
        replaced = False
        for subexpr, pos in preorder_iter_with_position(expression):
            for pattern, replacement in rules:
                try:
                    subst = next(match(subexpr, pattern))
                    result = replacement(**subst)
                    expression = replace(expression, pos, result)
                    replaced = True
                    break
                except StopIteration:
                    pass
            if replaced:
                break
        replace_count += 1

    return expression


def replace_all_post_order(expression: Expression, rules: Iterable[ReplacementRule]) \
        -> Union[Expression, Sequence[Expression]]:
    
    return _replace_all_post_order(expression, rules)[0]

def _replace_all_post_order(expression, rules):
    replaced = True
    any_replaced = False
    while replaced:
        replaced = False
        if isinstance(expression, Operation):
            new_operands = [_replace_all_post_order(o, rules) for o in op_iter(expression)]
            if any(r for _, r in new_operands):
                new_operands = [o for o, _ in new_operands]
                expression = create_operation_expression(expression, new_operands)
                any_replaced = True
        for pattern, replacement in rules:
            try:
                subst = next(iter(match(expression, pattern)))
                expression = replacement(**subst)
                replaced = any_replaced = True
                break
            except StopIteration:
                pass
    return expression, any_replaced


def is_match(subject: Expression, pattern: Expression) -> bool:
    
    return any(True for _ in match(subject, pattern))
