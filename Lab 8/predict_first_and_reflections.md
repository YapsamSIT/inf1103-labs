# INF1103 Lab 8: Predict First & Reflection Notes

**Student Name:** Sam  
**Module:** INF1103 - Object-Oriented Programming  
**Topic:** Object-Oriented Relationships Part 2 (Association, Aggregation, Composition, Type Hints, LSP, and Polymorphism)

---

## 1. Predict First & Diagnose Questions

### Section 2.2: Association - Deleting the `supplier` variable
- **Question:** Before you run this test, write down what you expect to happen if you delete your supplier variable (`del supplier`) after creating the products. Can each `Product` still display its supplier information? Run it and check. If your prediction did not match, note why.
- **My Prediction:** Yes, each `Product` will still be able to display its supplier information without any errors.
- **What Actually Happened:** Calling `del supplier` only deleted the local reference variable `supplier` from the calling scope's symbol table. Because `Product` stores its own reference to the `Supplier` instance (`self.supplier = supplier`), the underlying `Supplier` object still has an active reference and is not garbage-collected. The product can still access `self.supplier.name` and call `display_information()`.
- **Change / Key Learning:** My prediction matched the outcome. This demonstrates **Association**: objects collaborate via references without one possessing destructive lifecycle control over the other.

---

### Section 3.2: Aggregation - Removing Product from Inventory A
- **Question:** Before step 3, write down whether you expect the `Product` to still work after it is removed from Inventory A, and why. Then check.
- **My Prediction:** Yes, the `Product` will continue to exist and work normally after being removed from Inventory A.
- **What Actually Happened:** Removing the product from `Inventory A` simply removed the reference from `Inventory A`'s `products` list. The returned `Product` object was intact and could be inspected, modified, or added to `Inventory B`.
- **Change / Key Learning:** My prediction matched. This highlights **Aggregation**: a "has-a" whole-part relationship where the whole contains independent parts. The inventory does not own the lifecycle of the product; emptying or destroying an inventory does not destroy the products.

---

### Section 4.3: Composition - Same Product in Two Orders
- **Question:** If you add the same `Product` to two different Orders, how many `OrderLine` objects and how many `Product` objects will exist? Write your answer down, then check it (for example, compare objects using `is` or `id()`).
- **My Prediction:** There will be **two distinct `OrderLine` objects** and **one shared `Product` object**.
- **What Actually Happened:** Checked via `order1.order_lines[0] is order2.order_lines[0]` (returned `False`), while `order1.order_lines[0].product is order2.order_lines[0].product` (returned `True`). Each `Order` created its own private `OrderLine` instance, but both `OrderLine` instances hold references pointing to the single `Product` object.
- **Change / Key Learning:** My prediction matched. This illustrates **Composition**: `Order` has exclusive lifecycle ownership over its `OrderLine` parts (they are created inside `Order` and die with `Order`), while `OrderLine` merely holds an association reference to the independent `Product`.

---

### Section 6.3: Diagnose Question - DigitalProduct and LSP
- **Scenario:** A teammate proposes:
  ```python
  class DigitalProduct(Product):
      def update_stock(self, quantity: int) -> None:
          raise NotImplementedError("Digital products have no stock")
  ```
  *Does this violate LSP? What would you change: the subclass, the parent class (Product), or the inheritance relationship? Write 2–3 sentences explaining your choice.*
- **Answer:**  
  Yes, this strictly violates the **Liskov Substitution Principle (LSP)** because client code (such as `Inventory.update_stock()`) written against the `Product` contract expects any `Product` instance to safely process a stock update without abruptly crashing.  
  To fix this, we should change the **parent class design / inheritance relationship**: stock tracking should either be extracted into a separate interface/mixin (e.g., `StockTrackable` implemented only by `PhysicalProduct`), or if all products must retain `update_stock()`, `DigitalProduct` should safely handle the call as a no-op or maintain virtual license counts rather than throwing an unexpected exception that breaks client assumptions.

---

### Section 7.2: Polymorphism - `get_fulfilment_info()` Output
- **Question:** Before running your test, write down what each product will print for `get_fulfilment_info()`. Then compare with the actual output.
- **My Prediction:**
  - `PhysicalProduct`: `"This product requires physical shipping."`
  - `DigitalProduct`: `"This product is delivered digitally via download."`
- **What Actually Happened:** Output matched the prediction exactly.
- **Change / Key Learning:** Polymorphism allows a calling loop over `inventory.products` (typed as `list[Product]`) to invoke `get_fulfilment_info()` on each element without `isinstance()` checks or conditional branches. Python dynamically dispatches the call to the appropriate subclass implementation.

---

## 2. Section 10: Reflection Questions

1. **Which of your "Predict first" answers in this lab did not match what happened? What assumption was wrong, and what did you change?**  
   All predictions matched the runtime behavior because the distinctions between reference retention (Association), collection membership (Aggregation), and factory-style creation inside the owning class (Composition) were analyzed before writing the code.

2. **Where in your group project could you use association, aggregation or composition? Which would you choose, and why?**  
   - *Association:* A `Customer` and a `SupportTicket` or a `User` and an `ActivityLog` (independent lifecycles, mutually collaborating).  
   - *Aggregation:* A `Department` containing `Employee` objects, or a `Course` containing `Student` objects (students exist before and after enrolling in the course).  
   - *Composition:* An `Invoice` containing `InvoiceItem`s, or an `Account` owning `SecurityCredentials` (items have no meaning or existence outside their parent entity).

3. **Can an object reference exist without representing aggregation or composition? Give an example from your implementation.**  
   Yes. The reference `self.supplier: Supplier` inside `Product` is a pure **Association**. The product holds a reference to a supplier to display contact info or check supplier ID, but `Product` is not a "whole" made out of `Supplier` parts (not aggregation), nor does it control when the supplier is created or destroyed (not composition).

4. **Why can a Product be removed from an Inventory without being destroyed, while an OrderLine is designed to belong to an Order?**  
   Because an inventory is a storage container (Aggregation)—goods in the physical world are moved in and out of warehouses without altering the existence of the goods. Conversely, an `OrderLine` is a conceptual snapshot tied to a specific financial transaction (Composition)—a line item for "2 units of Product X at \$25" has no independent meaning or business validity outside Order #1001.

5. **Why should Inventory store `Product` references rather than separate collections for `PhysicalProduct` and `DigitalProduct`?**  
   Storing the base abstraction `Product` adheres to the **Open/Closed Principle (OCP)** and enables **Polymorphism**. If `Inventory` had separate lists, every new product subclass (e.g., `SubscriptionProduct`, `BundleProduct`) would force `Inventory` to add new lists, new `add_*` methods, and multiple duplicate search/display loops. With `list[Product]`, `Inventory` remains closed to modification while open to new product types.

6. **How do type hints help communicate design decisions to other developers?**  
   Type hints (such as `supplier: Supplier`, `products: list[Product]`, and `-> Product | None`) act as executable documentation. They explicitly state the developer's architectural intent, inform static analysis tools (like Mypy and IDE linters), prevent type errors during development, and map directly to UML class diagram contracts.

7. **Would your UML design still make sense if you implemented it in Java or C# rather than Python?**  
   Yes, completely. UML diagrams model system architecture and object-oriented contracts independently of programming language syntax. The concepts of abstract classes, interfaces, multiplicities, association, aggregation, and composition are universal across OOP languages. In fact, strongly typed languages like Java or C# enforce these exact relationships at compile time.

8. **Can a subclass technically inherit from `Product` but still violate LSP? Explain how.**  
   Yes. Syntax inheritance only guarantees that the subclass has matching method signatures. A subclass violates LSP if it breaks behavioral expectations: for instance, raising `NotImplementedError` on an inherited method, strengthening preconditions (e.g., demanding price > 1000 when Product allows any positive price), weakening postconditions, or returning invalid data types. Client code expecting a trustworthy `Product` would fail when given such a subclass.
