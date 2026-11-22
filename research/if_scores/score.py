#!/usr/bin/env python3
"""Exploratory heuristic game indices; not validated human ratings."""

def score(branching, duration, balance, decision, completion):
    b = branching / (branching + 10)
    d = duration / (duration + 30)
    interest = 100 * (0.40*b + 0.30*decision + 0.30*balance)
    enjoyment = 100 * (0.25*b + 0.25*d + 0.25*balance + 0.25*completion)
    return interest, enjoyment

if __name__ == "__main__":
    i, f = score(8.687581455967232, 26.855, 0.87,
                 0.9808617016247813, 1.0)
    print(f"Ember Roads I(G) = {i:.2f}/100")
    print(f"Ember Roads F(G) = {f:.2f}/100")
