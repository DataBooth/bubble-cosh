# Catenary Curve Optimisation

## **Overview**

This code is solving a **mathematical optimisation problem** related to the shape and properties of a curve known as a **catenary**. The catenary is the shape a flexible chain or cable assumes when supported at its ends and acted on only by gravity. This is relevant in physics, engineering, and architecture (e.g., suspension bridges, hanging cables, or hoops).

Specifically, the code is trying to:

- **Find the parameters** (`a` and `b`) of a catenary curve that fits certain boundary conditions:  
    - The curve must have a specified "diameter" (`d`) at both ends.
    - The curve must span a specified "length" (`l`) between its supports.
- **Calculate properties** of this curve, such as the area under it and the "mid dip" (how much the curve sags in the middle).

---

## **Detailed Breakdown**

### **1. The Catenary Equation**

The general form of the catenary is:
```
y = a * cosh((x - b)/a)
```
where:
- `a` controls the "tightness" or "sag" of the curve,
- `b` shifts the curve horizontally.

### **2. Boundary Conditions**

The code wants the catenary to:
- Start at `(x1=0, y1=d/2)`
- End at `(x2=l, y2=d/2)`

So, at both ends, the vertical position should be `d/2`.

### **3. Error Function**

The function `error_get(a, b, d, l)` computes how far the current guess for `a` and `b` is from satisfying the boundary conditions at both ends. It returns the sum of absolute errors at the two endpoints.

### **4. Parameter Search (Optimisation)**

The function `a_b_finder(d, l)`:
- Uses a **grid search** (brute-force search with decreasing step size) to find the values of `a` and `b` that minimise the error from the boundary conditions.
- It iteratively refines the guesses for `a` and `b` until the error is below a set precision.

### **5. Area Calculation**

The function `total_area(a, b, d, l)` calculates the area under the catenary curve between the two endpoints, using an analytical formula involving the hyperbolic sine (`sinh`) function.

### **6. Midpoint Calculations**

After finding the best-fit `a` and `b`, the code calculates:
- The **mid-radius**: the vertical position of the curve at the midpoint (`x = l/2`).
- The **mid dip**: how much lower the midpoint is compared to the endpoints.
- The **mid gap**: twice the mid-radius (possibly the vertical gap at the center).

---

## **What Is This For?**

This code could be used for:
- **Engineering design**: Calculating the shape and properties of a hanging cable, rope, or hoop between two points.
- **Physics simulations**: Modeling real-world catenary curves.
- **Architectural analysis**: Determining the sag and area under arches or cables.

---

## **Summary Table**

| **Function**        | **Purpose**                                                  |
|---------------------|-------------------------------------------------------------|
| `error_get`         | Calculates boundary error for given `a`, `b`                |
| `a_b_finder`        | Finds best `a`, `b` to fit the catenary to endpoints        |
| `total_area`        | Calculates area under the catenary curve                    |
| Main script         | Runs the above to output curve parameters and properties     |

---

## **In Short**

> **This code finds the best-fitting catenary curve between two points a certain distance apart, with specified vertical positions, and then calculates and outputs properties of that curve.**