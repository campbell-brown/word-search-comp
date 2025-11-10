from submission import Submission


class DummySubmission(Submission):
    def solve(self) -> None:
        for x in range(self.word_search.width()):
            for y in range(self.word_search.height()):
                self.word_search.submit((x, y))
