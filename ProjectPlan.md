# Symbolic Algebra and Integration Calculator

## 1. Project Overview

This project aims to build a fully symbolic algebra calculator with a long-term goal of extending it into a symbolic integration solver. The system prioritizes mathematical correctness over heuristics, tracks all domain restrictions explicitly, and records every transformation step taken during simplification or solving.

The calculator will:

* Operate symbolically (no floating-point approximations)
* Produce exact results only (integers, rational numbers, symbolic constants, functions)
* Support multivariable expressions from the start
* Track domain restrictions rigorously
* Maintain a complete log of algebraic and calculus steps

The project is intentionally ambitious and educational, with a clean internal architecture designed for long-term extensibility.

---

## 2. Design Philosophy

### 2.1 Correctness First

All transformations must be mathematically valid under explicitly tracked domain conditions. The system will:

* Never assume unstated properties of variables
* Preserve or refine domain restrictions during transformations
* Prefer piecewise or absolute-value expressions over unsafe simplifications

### 2.2 Deterministic Canonical Forms

The calculator will define a canonical representation for expressions so that:

* Equivalent expressions normalize to structurally identical forms
* Equality testing becomes structural rather than heuristic
* Simplification terminates reliably

Canonical forms are chosen explicitly and consistently, even when multiple algebraically equivalent representations exist.

### 2.3 Transparency and Step Tracking

Every algebraic action taken by the system will be logged. Each step record will include:

* The rule applied
* The expression before transformation
* The expression after transformation
* Any domain restrictions introduced or modified

This supports debugging, learning, and later UI or explanation features.

---

## 3. Implementation Language

The system will be implemented in Python, using only built-in libraries.

Rationale:

* Fast development and iteration
* Clear expression tree manipulation
* Readability for collaboration
* Adequate performance for symbolic workloads

---

## 4. Parsing and Tokenization

### 4.1 Parser Scope

A custom parser will be implemented. Parsing is considered a solved problem for this project and is not a risk factor.

### 4.2 Parsing Strategy

* Tokenizer + precedence-based expression parser
* Full support for:

  * Unary operators
  * Binary operators
  * Function calls
  * Parentheses

### 4.3 Parsing Output

The parser produces a raw abstract syntax tree (AST) without simplification. All semantic analysis and algebraic logic occurs after parsing.

---

## 5. Expression Representation

### 5.1 Core Expression Types

Expressions are immutable tree structures. Core types include:

* Number (exact integers and rational numbers)
* Symbol (variables)
* Add (list-based addition)
* Mul (list-based multiplication with coefficient)
* Pow (binary exponentiation)
* FunctionCall (e.g. sin(x), log(x))
* Abs
* Piecewise
* Equation

---

### 5.2 Numbers and Coefficients

Multiplicative expressions use a separated numeric coefficient model.

Example:

x * 5 * y

is represented as:

{
coefficient: 5,
factors: [x, y]
}

Properties:

* Coefficients are exact rational numbers
* A missing coefficient implies 1
* Numeric folding occurs only on coefficients

This design simplifies canonicalization, polynomial-style operations, and integration logic.

---

### 5.3 List-Based Operators

Addition and multiplication are list-based operators.

Add:

* Flattened (no nested Add nodes)
* Terms sorted deterministically
* Numeric terms combined

Mul:

* Flattened
* Coefficient separated
* Powers merged when possible

This avoids deep binary trees and supports commutativity naturally.

---

### 5.4 Exponentiation

Exponentiation is strictly binary:

Pow(base, exponent)

Properties:

* Not associative
* Not commutative

Exponent merging occurs during multiplication simplification:

x^a * x^b -> x^(a + b)
(x^a)^b -> x^(a * b)

Domain restrictions are applied where required.

---

### 5.5 Functions

Functions are represented as:

FunctionCall(name, arguments)

Examples:

* sin(x)
* log(x)
* f(x, y)

Functions are not treated as unary operators internally, enabling future extension to multivariable and user-defined functions.

---

## 6. Canonical Form Rules

The system favors expanded additive forms over factored forms.

Examples:

* Preferred: x/2 + sqrt(x+1)/2
* Avoided: (x + sqrt(x+1))/2

Canonicalization rules include:

* Flattening nested Add and Mul nodes
* Combining numeric coefficients
* Sorting terms and factors
* Normalizing signs and reciprocals

Factoring is not performed automatically and is applied only when required for solving.

---

## 7. Simplification Engine

### 7.1 Rule-Based Rewriting

Simplification is implemented as repeated application of local rewrite rules until a fixed point is reached.

Examples of rewrite rules:

* a + 0 -> a
* a * 1 -> a
* a * 0 -> 0
* a + (-a) -> 0
* x * (1/x) -> 1 (with domain tracking)
* x^1 -> x
* x^0 -> 1 (if allowed)

Rules are applied only when mathematically valid under the current domain.

---

### 7.2 Numeric Simplification

* Exact rational arithmetic only
* No floating-point evaluation
* Constants such as pi are symbolic

Evaluable expressions like sin(pi/4) are replaced with exact symbolic results.

---

### 7.3 Trigonometric and Logarithmic Identities

Standard algebra and competition-level identities are applied, including:

* sin^2(x) + cos^2(x) -> 1
* log(a^b) -> b * log(a) (with domain restrictions)

Identities that increase expression size or reduce correctness are avoided.

---

## 8. Absolute Values and Piecewise Expressions

Expressions such as:

sqrt(x^2)

are simplified to:

|x|

Absolute values may further simplify into Piecewise expressions depending on known domain conditions.

Piecewise expressions are first-class and fully supported throughout simplification, solving, and integration.

---

## 9. Domain Tracking and Assumptions

### 9.1 Domain Tracker

Each top-level expression or equation contains a domain tracker.

The domain tracker:

* Collects domain restrictions (e.g. x != 0, x > 0)
* Never mutates expressions
* Stores restrictions declaratively

---

### 9.2 Initial vs Final Domain

Two domain layers are tracked:

1. Initial domain:

   * Derived from the original input expression
   * Used to reject invalid solutions during equation solving

2. Final domain:

   * Derived from the simplified expression
   * Used for evaluation and display

Both are preserved independently.

---

### 9.3 Domain Sources

Domain restrictions arise from:

* Division
* Logarithms
* Even roots
* Exponentiation
* Function definitions

Example:

* log(x) introduces x > 0
* 1/x introduces x != 0

---

## 10. Equation Solving

### 10.1 Normalization

Equations are normalized into the form:

LHS - RHS = 0

This unified form simplifies solving and analysis.

---

### 10.2 Equation Classification

The solver identifies equation types based on structure:

* Linear
* Polynomial (degree detection)
* Exponential
* Trigonometric (limited)

Pattern recognition is applied only after full normalization.

---

### 10.3 Solving Strategy

* Apply known exact solution formulas where applicable
* Use factoring and substitution when necessary
* Reject extraneous solutions using initial domain restrictions

All solution steps are logged.

---

## 11. Calculus Extension (Integration)

### 11.1 Integration Strategy

Integration is implemented as a rule-based and backtracking system.

Steps:

1. Classify the integrand
2. Attempt integration methods in order:

   * Direct pattern matching
   * Substitution
   * Integration by parts
   * Partial fractions
3. Backtrack on failure

---

### 11.2 Correctness Guarantees

* No heuristic-only integration
* No incorrect results under hidden assumptions
* Piecewise results used when required

Failure to integrate is acceptable; incorrect integration is not.

---

## 12. Step Logging System

Every transformation appends a record to a global step log.

Each record includes:

* Rule or method name
* Input expression
* Output expression
* Domain changes

The log is strictly append-only.

---

## 13. Collaboration and Task Separation

Beginner-friendly components:

* Tokenizer
* Parser
* AST construction
* Pretty-printing
* Rational arithmetic
* Unit tests

Advanced components:

* Simplification engine
* Canonicalization rules
* Domain tracking
* Equation solving
* Integration logic

---

## 14. Scope Boundaries (Version 1)

Included:

* Exact symbolic algebra
* Multivariable expressions
* Domain tracking
* Equation solving
* Step logging

Deferred:

* Numeric approximation
* Complex analysis branch cuts
* Advanced transcendental equation solving
* Definite integration

---

## 15. Long-Term Goals

* Complex number mode
* Assumption-aware simplification
* Differentiation
* Definite integrals
* UI and explanation rendering

---

End of document.
