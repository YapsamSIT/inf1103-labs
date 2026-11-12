from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface for products requiring physical shipping."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass
