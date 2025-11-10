"""This script is to be used by a judge to check submissions for the word search competition.
Participants should not need to modify this file.
"""

from dummy_submission import DummySubmission
from word_search_competition import WordSearchCompetition

words = set(  # TODO: replace with actual competition words!
    [
        "these",
        "words",
        "are",
        "example",
        "only",
        "different",
        "ones",
        "will",
        "be",
        "used",
        "for",
        "the",
        "actual",
        "competition",
    ]
)
word_search = WordSearchCompetition(words)
submission = DummySubmission(word_search)  # TODO: replace with the actual submission!

word_search.print_puzzle()
submission.solve()
print(f"Final score: {word_search.score}")
if word_search.is_solved():
    print("Puzzle solved!")
else:
    print("Puzzle not solved.")
