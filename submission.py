from word_search_competition import WordSearchCompetition


class Submission:
    def __init__(self, word_search: WordSearchCompetition) -> None:
        self.word_search = word_search

    def solve(self) -> None:
        raise NotImplementedError("You must implement the solve method!")
