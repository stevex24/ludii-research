# Day 4: independent NoGo validation

The Day 4 solver represents each player's stones as a bitboard and tests group liberties with bit operations. This independent checker instead uses a nine-element tuple board, a separate graph flood-fill implementation of group liberties, and a separate memoized minimax recursion. It exhaustively compares **legal moves, win/loss outcomes, and depth-to-terminal (DTM)** for every reachable position.

**Scope limitation:** The standard NoGo rules in the Ludii `.lud` file are consistent with the specified constraints (no capture, no suicide, no passing, no legal move loses). This script **does not invoke Ludii** and does not establish independent Ludii execution agreement. Ludii-based testing remains a separate possible task.

The reference DTM convention is shortest forced win and longest resistance in a forced loss. This is one convention, not a claim that every optimal line is the same length.
