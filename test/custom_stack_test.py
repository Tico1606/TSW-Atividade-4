import pytest

from src.custom_stack_class import (
    CustomStack,
    StackEmptyException,
    StackFullException,
)


def test_new_stack_is_empty():
    stack = CustomStack(3)

    assert stack.size() == 0
    assert stack.is_empty()


def test_push_and_pop_preserve_lifo_order():
    stack = CustomStack(3)
    stack.push(10)
    stack.push(20)

    assert stack.size() == 2
    assert not stack.is_empty()
    assert stack.top() == 20
    assert stack.pop() == 20
    assert stack.top() == 10
    assert stack.pop() == 10
    assert stack.is_empty()


def test_push_raises_when_stack_is_full():
    stack = CustomStack(1)
    stack.push(10)

    with pytest.raises(StackFullException):
        stack.push(20)

    assert stack.elements == [10]


def test_pop_raises_when_stack_is_empty():
    with pytest.raises(StackEmptyException):
        CustomStack(1).pop()


def test_top_raises_when_stack_is_empty():
    with pytest.raises(StackEmptyException):
        CustomStack(1).top()
