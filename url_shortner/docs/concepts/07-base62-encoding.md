# Concept 07 — Base62 Encoding & Number Systems

# 1. Why Base62?
Base62 uses 62 alphanumeric characters: `0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`.

- Base10 (0-9): 6 digits = $10^6 = 1,000,000$ unique combinations.
- Base62 (0-9, a-z, A-Z): 7 characters = $62^7 = \mathbf{3.52 \text{ Trillion}}$ unique combinations!

Unlike Base64, Base62 contains no special characters (`+`, `/`, `=`) that require URL percent-encoding.

---

# 2. Mathematical Conversion Algorithm

Converting integer `125` to Base62:

$$\text{Step 1: } 125 \div 62 = 2 \quad \text{Remainder: } 1 \longrightarrow \text{Char: '1'}$$
$$\text{Step 2: } 2 \div 62 = 0 \quad \text{Remainder: } 2 \longrightarrow \text{Char: '2'}$$
$$\text{Reversed Result: } 125_{10} \longrightarrow \mathbf{"21"}_{62}$$
