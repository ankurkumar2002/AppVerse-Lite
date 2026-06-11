
from collections import defaultdict

# store per session
chat_memory = defaultdict(list)

MAX_HISTORY = 6  # sliding window
