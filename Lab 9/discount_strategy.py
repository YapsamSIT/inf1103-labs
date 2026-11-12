from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Abstract Strategy interface for calculating order discounts.
    Enables interchangeable discount algorithms without modifying Order (OCP).
    """

    @abstractmethod
    def apply(self, total: float) -> float:
        """Apply the discount algorithm to the raw total and return the discounted total."""
        pass


class NoDiscount(DiscountStrategy):
    """Default strategy: returns the order total unchanged."""

    def apply(self, total: float) -> float:
        return float(total)

    def __repr__(self) -> str:
        return "NoDiscount()"


class PercentageDiscount(DiscountStrategy):
    """Percentage discount strategy (e.g. PercentageDiscount(10) applies 10% off)."""

    def __init__(self, percentage: float):
        if not (0 <= percentage <= 100):
            raise ValueError("Percentage discount must be between 0 and 100.")
        self.percentage: float = float(percentage)

    def apply(self, total: float) -> float:
        discounted = total * (1.0 - (self.percentage / 100.0))
        return max(0.0, float(discounted))

    def __repr__(self) -> str:
        return f"PercentageDiscount({self.percentage}%)"


class BulkDiscount(DiscountStrategy):
    """Bulk discount strategy: applies a fixed discount amount if total reaches a threshold.
    E.g. BulkDiscount(200, 20) takes $20 off any total of $200 or more.
    """

    def __init__(self, threshold: float, amount: float):
        if threshold < 0:
            raise ValueError("Threshold cannot be negative.")
        if amount < 0:
            raise ValueError("Discount amount cannot be negative.")
        self.threshold: float = float(threshold)
        self.amount: float = float(amount)

    def apply(self, total: float) -> float:
        if total >= self.threshold:
            return max(0.0, float(total - self.amount))
        return float(total)

    def __repr__(self) -> str:
        return f"BulkDiscount(threshold=${self.threshold:.2f}, amount=${self.amount:.2f})"


class StudentDiscount(DiscountStrategy):
    """Custom 4th strategy (Section 2.4): applies a special student discount percentage."""

    def __init__(self, percentage: float = 5.0):
        if not (0 <= percentage <= 100):
            raise ValueError("Student discount percentage must be between 0 and 100.")
        self.percentage: float = float(percentage)

    def apply(self, total: float) -> float:
        discounted = total * (1.0 - (self.percentage / 100.0))
        return max(0.0, float(discounted))

    def __repr__(self) -> str:
        return f"StudentDiscount({self.percentage}%)"
