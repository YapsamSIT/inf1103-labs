# INF1103 Lab 9: Predict First & Reflection Notes

**Student Name:** Sam  
**Module:** INF1103 - Object-Oriented Programming  
**Topic:** Design Patterns and Error Handling (Strategy, Factory, Validation, Try / Except, and Automated Tests)

---

## 1. Section 1.5 Diagnose (Reviewing Lab 8 Code)

Before writing any new code in Lab 9, we audited our Lab 8 implementation:
1. **Any `if/elif` block choosing between different behaviours:**
   - In earlier versions (or standard non-strategy implementations), order discounts required branching logic like `if discount_type == "none": ... elif discount_type == "percentage": ... elif discount_type == "bulk": ...`. This violates the Open/Closed Principle (OCP) because adding a new discount type necessitates modifying the existing `Order.calculate_total()` method.
2. **Every place `PhysicalProduct` or `DigitalProduct` was created directly:**
   - In `main.py` setup code and unit tests (`TestProducts`, `TestInventory`), calling `PhysicalProduct(...)` and `DigitalProduct(...)` tightly coupled client code to concrete subclass constructors and their distinct parameter signatures.
3. **Places where bad input or a missing file could crash the program:**
   - In console input routines when casting user input via `float(input(...))` or `int(input(...))` without `try/except ValueError`.
   - In file loading functions if the designated filename does not exist (`FileNotFoundError`), or contains corrupted rows with non-numeric numbers or invalid types.

---

## 2. Predict First & Diagnose Questions

### Section 2.1: Strategy Pattern - Adding a Student Discount
- **Question:** The business now wants a 5% student discount. Without the Strategy pattern, which class and method must change? After you complete Section 2, answer the same question again for your Strategy version.
- **Without Strategy Pattern:**
  - Class: `Order`
  - Method: `calculate_total()`
  - Reason: We would need to modify the method to add an `elif discount_type == "student": return total * 0.95` branch, which violates the Open/Closed Principle (OCP).
- **With Strategy Pattern:**
  - Class & Method changed: **None!**
  - Reason: `Order` and its `calculate_total()` method remain completely untouched. We simply introduce a brand-new class:
    ```python
    class StudentDiscount(DiscountStrategy):
        def apply(self, total: float) -> float:
            return total * 0.95
    ```
    We pass `StudentDiscount()` to `Order(..., discount)` or call `order.set_discount(StudentDiscount())`.

---

### Section 2.3: Strategy Pattern - Order Total Calculation
- **Question:** Create an order whose lines add up to 250. What will `calculate_total()` return with `BulkDiscount(200, 20)`? What if you then call `set_discount(PercentageDiscount(10))` on the same order? Write both answers down, then run your code and check.
- **My Prediction:**
  - With `BulkDiscount(200, 20)`: Subtotal \$250 meets the \$200 threshold, so \$20 is deducted: \$250.00 - \$20.00 = **\$230.00**.
  - With `set_discount(PercentageDiscount(10))`: 10% discount on \$250 is \$25.00, resulting in \$250.00 - \$25.00 = **\$225.00**.
- **What Actually Happened:** `order.calculate_total()` returned exactly `230.00` and then `225.00`.
- **Change / Key Learning:** My prediction was correct. The Strategy pattern enables swapping algorithms dynamically at runtime without altering the context object (`Order`).

---

### Section 2.4: Object Relationship between Order and DiscountStrategy
- **Question:** Which relationship best describes `Order` and `DiscountStrategy`: association, aggregation or composition? Hint: is a discount part of an order, or something the order uses? Could two orders share the same `PercentageDiscount` object? Write your answer and a multiplicity for each end, then check it against your code.
- **Answer:**
  - **Relationship:** **Association** (specifically, Strategy / Dependency).
  - **Explanation:** A discount algorithm is not a physical part of an order's lifecycle (unlike an `OrderLine`). It represents a reusable behavior that the order *uses* or *collaborates with*. Two distinct orders can readily share the exact same `PercentageDiscount(10)` strategy instance simultaneously.
  - **Multiplicities:** `Order [0..*] —— [1] DiscountStrategy` (each order has exactly 1 active discount strategy at a time; a discount strategy instance can be used by zero or many orders).

---

### Section 3.2: Factory Pattern - Unknown Product Type
- **Question:** What happens if you call `ProductFactory.create("service", ...)`? Which line raises the exception, and what happens to your program if nothing catches it? Run it and check.
- **My Prediction:** The `else:` branch of `ProductFactory.create()` executes and raises a `ValueError("Unknown product type: service")`. If unhandled, Python will print a traceback and immediately terminate the program with exit code 1.
- **What Actually Happened:** In `ProductFactory.create`:
  ```python
  else:
      raise ValueError(f"Unknown product type: {product_type}")
  ```
  The `ValueError` was raised. In our test and demo, catching it demonstrated that the calling code can handle unexpected product types cleanly.
- **Change / Key Learning:** Prediction matched. The factory centralizes the guard against unrecognized types in one place.

---

### Section 3.3: Factory Pattern - Adding a BundleProduct & OCP Trade-off
- **Question:** Suppose a new `BundleProduct` type is added. How many places in your code would need to change before you added the factory, and how many after? Count them, then explain why the factory still breaks OCP and why that is acceptable here.
- **Answer:**
  - **Before the factory:** Multiple places across the codebase would need to change—every CLI menu, CSV loader, test suite, and seed data function that instantiates products directly (at least 4–5 different places).
  - **After the factory:** Exactly **1 place** needs to change: the `ProductFactory.create()` method, where we add an `elif product_type == "bundle": return BundleProduct(...)`.
  - **Why the factory still breaks OCP and why it is acceptable:** Modifying `ProductFactory.create()` to support a new product type technically modifies an existing class rather than extending it without modification (thus breaking OCP inside the factory itself). However, this is an acceptable and pragmatic engineering trade-off: it confines the modification to a single, focused class while keeping the entire rest of the application completely closed to modification.

---

### Section 4: Domain Validation - Negative Stock and LSP
- **Question:** Think back to the Lab 8 LSP discussion. If `Product` validates that stock cannot go negative, should `DigitalProduct` be allowed to skip or change that rule? Why?
- **Answer:**
  - **No.** Under the Liskov Substitution Principle (LSP), subclasses must preserve all invariants and contracts guaranteed by the parent class.
  - If `Product` guarantees that any `Product` object has `stock_quantity >= 0`, client code written against `Product` assumes this invariant always holds true. If `DigitalProduct` allowed negative stock, any shared inventory management or reporting logic relying on the non-negative invariant would break.

---

### Section 5.1: User Input Validation
- **Question:** A user enters `abc`, then `-5`, then `12.50`. Write down exactly what prints after each entry and what value is returned. Then run it and check.
- **Prediction:**
  - User types `abc`: `float("abc")` raises `ValueError` -> Caught by `except ValueError:` -> Prints: `"Please enter a valid number, e.g. 12.50"`.
  - User types `-5`: `float("-5")` produces `-5.0` -> `if value <= 0:` triggers -> Prints: `"Please enter a number greater than zero."` -> `continue`.
  - User types `12.50`: `float("12.50")` produces `12.50` -> Valid -> Loop terminates and **returns `12.5`**.
- **What Actually Happened:** Matched prediction precisely.

---

### Section 5.2: CSV Loading with Exceptions
- **Question:** Before running, write down how many products will load, which messages will print, and in what order. Then rename `products.csv` and predict again: which of except, else and finally will run?
- **File with 5 rows:**
  1. `physical,P001,Desk Lamp,25.00,10` -> Valid physical product -> Added.
  2. `digital,D001,Photo Editor,49.90,100` -> Valid digital product -> Added.
  3. `service,S001,Installation,30.00,5` -> Invalid type `"service"` -> `ProductFactory` raises `ValueError` -> Skipped.
  4. `physical,P002,Office Chair,abc,3` -> `"abc"` is not a valid float -> `float()` raises `ValueError` -> Skipped.
  5. `physical,P003,Monitor Stand,39.50,7` -> Valid physical product -> Added.
  - **Total loaded:** **3 products loaded**.
  - **Printed messages in order:**
    1. `Row 4 skipped - invalid data ['service', 'S001', 'Installation', '30.00', '5']: Unknown product type: service`
    2. `Row 5 skipped - invalid data ['physical', 'P002', 'Office Chair', 'abc', '3']: could not convert string to float: 'abc'`
    3. `3 products loaded.`
    4. `Load attempt finished.`
- **When file is missing / renamed:**
  - `except FileNotFoundError:` runs and prints: `"Products file not found: ..."`
  - `else:` block is skipped entirely.
  - `finally:` runs unconditionally and prints: `"Load attempt finished."`

---

## 3. Section 8: Reflection Questions

1. **Where in your system would adding a pattern make the design more complicated than it needs to be?**  
   Applying the Abstract Factory or Builder pattern to create `OrderLine` or `Supplier` objects would introduce excessive boilerplate classes and unnecessary abstraction layers for simple, direct instantiation needs.

2. **The Factory moved the OCP issue from the client into the factory. Is that a good trade-off for your system? Why?**  
   Yes, it is an excellent trade-off. By consolidating creation decisions in `ProductFactory`, any future constructor signature changes or new subclasses require changes in only one isolated location rather than throughout menus, controllers, test scripts, and loaders.

3. **In 5.2, you skipped bad rows and kept loading. When would rejecting the whole file be the better design decision?**  
   Rejecting the whole file (all-or-nothing / transactional loading) is essential in mission-critical financial systems, banking transactions, ledger imports, or database batch migrations where partial data ingestion causes database inconsistency, data corruption, or unbalanced financial accounts.

4. **What is the difference between a validation failure and an exception in your code? Give one example of each.**  
   - **Validation:** Proactively checking data against business invariants using conditional logic (`if price <= 0: raise ValueError(...)`) before processing.
   - **Exception:** An unexpected runtime disruption or OS/hardware-level event during execution, such as `FileNotFoundError` when a disk file is missing, or `ValueError` raised internally by `float("abc")`.

5. **Which of your "Predict first" answers in this lab did not match what happened? What assumption was wrong, and what did you change?**  
   All predictions matched the actual execution because the control flow of `try/except/else/finally`, the math of the Strategy algorithms, and the dispatch logic of `ProductFactory` were verified step-by-step prior to execution.

6. **Where in your group project could the Strategy or Factory pattern help, or would it be over-engineering? Why?**  
   - *Strategy Pattern:* Highly effective for payment processing (e.g. `CreditCardPayment`, `PayNowPayment`, `PayPalPayment`) or notification delivery (`EmailNotification`, `SMSNotification`), avoiding cluttered `if/elif` statements.  
   - *Factory Pattern:* Useful for instantiating different user account tiers or report exporters (`PDFExporter`, `CSVExporter`, `JSONExporter`). It would be over-engineering if the system only ever has one static class type with no variation.
