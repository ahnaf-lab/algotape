"""Quicksort (Lomuto partition), instrumented to yield a frame per swap/step."""

from typing import Iterator, List

from ..frames import Frame


def quicksort_frames(values: List) -> Iterator[Frame]:
    """Sort ``values`` with quicksort, yielding a Frame per meaningful step.

    The pivot is always the last element of the current subarray, which
    makes the sequence of partitions, swaps, and comparisons deterministic
    for a given input list.
    """
    arr = list(values)
    step = 0

    def emit(event: str, **state) -> Frame:
        nonlocal step
        frame = Frame(algorithm="quicksort", step=step, event=event, state=state)
        step += 1
        return frame

    yield emit("init", array=list(arr))

    def partition(low: int, high: int) -> Iterator[Frame]:
        pivot = arr[high]
        yield emit("pivot", low=low, high=high, pivot=pivot, array=list(arr))
        i = low
        for j in range(low, high):
            if arr[j] <= pivot:
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    yield emit("swap", i=i, j=j, array=list(arr))
                i += 1
        if i != high:
            arr[i], arr[high] = arr[high], arr[i]
            yield emit("swap", i=i, j=high, array=list(arr))
        yield emit(
            "partitioned", low=low, high=high, pivot_index=i, array=list(arr)
        )
        return i

    def sort(low: int, high: int) -> Iterator[Frame]:
        if low < high:
            pivot_index = yield from partition(low, high)
            yield from sort(low, pivot_index - 1)
            yield from sort(pivot_index + 1, high)

    yield from sort(0, len(arr) - 1)
    yield emit("done", array=list(arr))
