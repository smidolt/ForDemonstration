# Define the probabilities and revenues of each company
probabilities = [0.1, 0.19, 0.4, 0.45, 0.5]
revenues = [10, 5, 4, 3, 5]

# Define the number of companies and users
m = len(probabilities)
n = 1

# Method 1: Brute force
import itertools

# Generate all possible orders of querying the companies
orders = list(itertools.permutations(range(m)))

# Initialize the maximum expected revenue and the optimal order
max_expected_revenue = 0
optimal_order = None

# Loop through each order
for order in orders:
    # Initialize the expected revenue for this order
    expected_revenue = 0

    # Initialize the probability of not getting an ad from previous companies
    p_no_ad = 1

    # Loop through each company in this order
    for i in order:
        # Calculate the expected revenue from this company
        expected_revenue += p_no_ad * probabilities[i] * revenues[i]

        # Update the probability of not getting an ad from previous companies
        p_no_ad *= (1 - probabilities[i])

        # Compare the expected revenue with the maximum one
        if expected_revenue > max_expected_revenue:
            # Update the maximum expected revenue and the optimal order
            max_expected_revenue = expected_revenue
            optimal_order = order

# Print the optimal order and the maximum expected revenue
print("Method 1: Brute force")
print("The optimal order of querying the companies is:", optimal_order)
print("The maximum expected revenue per user is:", max_expected_revenue)

# Method 2: Dynamic programming
import numpy as np

# Define a matrix to store the expected revenue for each subset of companies and each number of queries
dp = np.zeros((2 ** m, m + 1))

# Loop through each subset of companies
for s in range(1, 2 ** m):
    # Loop through each number of queries
    for k in range(1, m + 1):
        # Initialize the maximum expected revenue for this subset and this number of queries
        max_expected_revenue = 0

        # Loop through each company in this subset
        for i in range(m):
            # Check if this company is in this subset
            if s & (1 << i):
                # Calculate the expected revenue from this company
                expected_revenue = probabilities[i] * revenues[i] + (1 - probabilities[i]) * dp[s ^ (1 << i), k - 1]

                # Compare the expected revenue with the maximum one
                if expected_revenue > max_expected_revenue:
                    # Update the maximum expected revenue
                    max_expected_revenue = expected_revenue

                # Store the maximum expected revenue in the matrix
                dp[s, k] = max_expected_revenue

# Define a list to store the optimal order of querying the companies
optimal_order = []

# Initialize the current subset of companies and the current number of queries
s = 2 ** m - 1
k = m

# Loop until there are no more companies or queries left
while s > 0 and k > 0:
    # Initialize the best company to query next
    best_company = None

    # Loop through each company in the current subset
    for i in range(m):
        # Check if this company is in the current subset
        if s & (1 << i):
            # Calculate the expected revenue from this company
            expected_revenue = probabilities[i] * revenues[i] + (1 - probabilities[i]) * dp[s ^ (1 << i), k - 1]

            # Compare the expected revenue with the maximum one
            if expected_revenue == dp[s, k]:
                # Update the best company to query next
                best_company = i
                break

    # Add the best company to the optimal order
    optimal_order.append(best_company)

    # Remove the best company from the current subset
    s ^= (1 << best_company)

    # Decrease the current number of queries by one
    k -= 1

# Reverse the optimal order to get the correct order
optimal_order.reverse()

# Print the optimal order and the maximum expected revenue
print("Method 2: Dynamic programming")
print("The optimal order of querying the companies is:", tuple(optimal_order))
print("The maximum expected revenue per user is:", dp[2 ** m - 1, m])
