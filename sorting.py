class Sorting:
    """Provides a number of procedures for sorting vectors (lists)."""

    @staticmethod
    def quickSort(v: list) -> None:
        """Sort v in-place using quicksort (descending order).

        Modifies: v
        Effects: If some member of v is None raises TypeError (NullPointerException);
                 if elements of v aren't comparable raises TypeError (ClassCastException);
                 else sorts v so that elements with larger indexes are less than
                 those at smaller indexes (descending order).
        """
        if any(item is None for item in v):
            raise TypeError("NullPointerException: list contains None element")

        Sorting._quicksort(v, 0, len(v) - 1)

    @staticmethod
    def _quicksort(v: list, low: int, high: int) -> None:
        if low < high:
            pivot_index = Sorting._partition(v, low, high)
            Sorting._quicksort(v, low, pivot_index - 1)
            Sorting._quicksort(v, pivot_index + 1, high)

    @staticmethod
    def _partition(v: list, low: int, high: int) -> int:
        pivot = v[high]
        i = low - 1
        for j in range(low, high):
            try:
                # Descending: move elements greater than pivot to the left
                greater = v[j] > pivot
            except TypeError:
                raise TypeError("ClassCastException: elements are not comparable")
            if greater:
                i += 1
                v[i], v[j] = v[j], v[i]
        v[i + 1], v[high] = v[high], v[i + 1]
        return i + 1