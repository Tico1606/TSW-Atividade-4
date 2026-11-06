import pytest

from src.custom_stack_class import CustomStack
from src.number_asc_order_class import NumberAscOrder


def make_stack(numbers, capacity=6):
    stack = CustomStack(capacity)
    for number in numbers:
        stack.push(number)
    return stack


def test_sort_returns_ascending_numbers_and_preserves_real_stack():
    draw = [34, 5, 60, 12, 42, 1]
    stack = make_stack(draw)

    result = NumberAscOrder().sort(stack)

    assert result == [1, 5, 12, 34, 42, 60]
    assert stack.elements == draw


def test_sort_returns_empty_list_for_empty_stack():
    stack = CustomStack(6)

    assert NumberAscOrder().sort(stack) == []
    assert stack.is_empty()


def test_sort_uses_each_mocked_pop_return_and_restores_order(mocker):
    stack = mocker.create_autospec(CustomStack, instance=True)
    stack.limit = 6
    stack.size.return_value = 6
    stack.pop.side_effect = [1, 42, 12, 60, 5, 34]

    result = NumberAscOrder().sort(stack)

    assert result == [1, 5, 12, 34, 42, 60]
    assert stack.pop.call_count == 6
    assert [call.args[0] for call in stack.push.call_args_list] == [
        34,
        5,
        60,
        12,
        42,
        1,
    ]


def test_sort_rejects_a_non_custom_stack():
    with pytest.raises(TypeError):
        NumberAscOrder().sort([])


def test_sort_rejects_a_stack_with_the_wrong_capacity():
    with pytest.raises(ValueError):
        NumberAscOrder().sort(CustomStack(5))


def test_sort_rejects_a_partially_filled_stack_and_preserves_it():
    draw = [34, 5, 60, 12, 42]
    stack = make_stack(draw)

    with pytest.raises(ValueError):
        NumberAscOrder().sort(stack)

    assert stack.elements == draw


@pytest.mark.parametrize(
    "draw",
    [
        [1, 2, 3, 4, 5, 0],
        [1, 2, 3, 4, 5, 61],
    ],
)
def test_sort_rejects_numbers_outside_mega_sena_range(draw):
    stack = make_stack(draw)

    with pytest.raises(ValueError):
        NumberAscOrder().sort(stack)

    assert stack.elements == draw


def test_sort_rejects_repeated_numbers_and_preserves_stack():
    draw = [1, 2, 3, 4, 5, 5]
    stack = make_stack(draw)

    with pytest.raises(ValueError):
        NumberAscOrder().sort(stack)

    assert stack.elements == draw


@pytest.mark.parametrize("invalid_number", [True, 5.0, "5"])
def test_sort_rejects_values_that_are_not_integers(invalid_number):
    draw = [1, 2, 3, 4, 5, invalid_number]
    stack = make_stack(draw)

    with pytest.raises(ValueError):
        NumberAscOrder().sort(stack)

    assert stack.elements == draw
