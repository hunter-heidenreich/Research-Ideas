import time
import json


class Idea:

    def __init__(self, filename=None):

        self._idea_sentences = []
        self._tags = []
        self._refs = []
        self._created_at = None

        if filename:
            self.load(filename)

    def save(self):
        if not self._created_at:
            self._created_at = time.time()

        json.dump({
            'idea': self._idea_sentences,
            'tags': self._tags,
            'refs': self._refs,
            'created_at': self._created_at
        }, open('ideas/{}.json'.format(self._created_at), 'w+'))

    def load(self, filename):
        data = json.load(open(filename))

        self._idea_sentences = data['idea']
        self._tags = data['tags']
        self._refs = data['refs']
        self._created_at = data['created_at']


if __name__ == '__main__':
    running = True

    while running:
        running = None  # Will put a feedback loop here
