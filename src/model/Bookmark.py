class Bookmark:
    lastLineRead: int

    def __init__(self):
        self.lastLineRead = 0

    def nextLine(self) -> int:
        self.lastLineRead += 1
        return self.lastLineRead

    