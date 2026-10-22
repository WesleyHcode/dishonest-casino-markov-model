import math

transition = [
    [0.99, 0.01],  # P(F | F), P(L | F)
    [0.2, 0.8]   # P(F | L), P(L | L)
]

chance = [
    [1/6, 1/6, 1/6, 1/6, 1/6, 1/6],  # F probabilities
    [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]   # L probabilities
]

# Convert to log
log_t = [[math.log(p) for p in row] for row in transition]
log_c = [[math.log(p) for p in row] for row in chance]

# Given sequence
roll_sequence = [
    1, 2, 4, 5, 5, 2, 6, 4, 6, 2,
    1, 4, 6, 1, 4, 6, 1, 3, 6, 1,
    3, 6, 6, 6, 1, 6, 6, 4, 6, 6,
    1, 6, 3, 6, 6, 1, 6, 3, 6, 6,
    1, 6, 3, 6, 1, 6, 5, 1, 5, 6,
    1, 5, 1, 1, 5, 1, 4, 6, 1, 2,
    3, 5, 6, 2, 3, 4, 4
]

# Avoid log(0)
rolls = [r - 1 for r in roll_sequence]

# Initialize the first roll
r0 = rolls[0]
# Starting chances for F or L
start_p = [0.5, 0.5] 
# States represent the best probability for F or L
states = [
    (math.log(start_p[0]) + log_c[0][r0], "F"), 
    (math.log(start_p[1]) + log_c[1][r0], "L")
]

# Iteration
for r in rolls[1:]:
    # Calculate 2 ways to get F
    f_from_f = states[0][0] + log_t[0][0]
    f_from_l = states[1][0] + log_t[1][0]
    next_f = (
        # Get max prob of f|f, f|l and add chance of roll that happened so we get
        # total probability of that path
        max(f_from_f, f_from_l) + log_c[0][r],
        # Get the path that led to the max
        states[0][1] + "F" if f_from_f > f_from_l else states[1][1] + "F",
    )

    # Calculate 2 ways to get L
    l_from_f = states[0][0] + log_t[0][1]
    l_from_l = states[1][0] + log_t[1][1]
    next_l = (
        # Same for L
        max(l_from_f, l_from_l) + log_c[1][r],
        states[0][1] + "L" if l_from_f > l_from_l else states[1][1] + "L",
    )

    # New states and then regress
    states = [next_f, next_l]

# Output
best_score, best_path = max(states)
print("Predicted States:", best_path)