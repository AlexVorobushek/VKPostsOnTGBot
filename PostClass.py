import datetime


class Post:
    def __init__(self, data: dict) -> None:
        self.data = data
        self.from_id = self.data['from_id']
        self.time = self.data['date']
        self.date = datetime.datetime.utcfromtimestamp(self.time)
        self.text = self.data['text']

    def __str__(self) -> str:
        return f"from: {self.from_id}\n{self.date}\n\n{self.text}"
