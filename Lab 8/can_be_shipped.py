from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface for items that can be physically shipped."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Calculate and return the shipping cost."""
        pass
