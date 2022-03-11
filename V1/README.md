# WordleBot

Python object for testing various strategies in Wordle:
- HumanStrategy: For an interactive version
- BruteForceStrategy: Try every possible word (not just the possible solutions) in alphabetical order
- RandomStrategy: Try every possible word (not just the possible solutions) in a random order
- NextValidStrategy: Start by guessing the first alphabetically possible word. After each response, cull the list of possibilities and guess the alphabetically first valid one.
- SmallestAverageStrategy: Simulate guessing each word and find the average number of valid words after each possible result. Choose the word that has the lowest average.
- SmallestMaximumStrategy: Simulate guessing each word and find the maximum number of valid words after each possible result. Choose the word that has the lowest maximum.
