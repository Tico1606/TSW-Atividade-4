from src.custom_stack_class import CustomStack


class NumberAscOrder:
    def sort(self, stack: CustomStack) -> list[int]:
        if not isinstance(stack, CustomStack):
            raise TypeError("stack must be a CustomStack")

        if stack.limit != 6:
            raise ValueError("the stack capacity must be 6")

        stack_size = stack.size()
        if stack_size == 0:
            return []
        if stack_size != 6:
            raise ValueError("the stack must contain exactly 6 numbers")

        drawn_numbers = []
        try:
            for _ in range(stack_size):
                drawn_numbers.append(stack.pop())
        finally:
            for number in reversed(drawn_numbers):
                stack.push(number)

        if any(type(number) is not int for number in drawn_numbers):
            raise ValueError("all drawn numbers must be integers")
        if any(number < 1 or number > 60 for number in drawn_numbers):
            raise ValueError("drawn numbers must be between 1 and 60")
        if len(set(drawn_numbers)) != 6:
            raise ValueError("drawn numbers must be distinct")

        return sorted(drawn_numbers)
