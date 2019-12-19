import time
import json
import os


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

    def create(self):
        # Idea Sentences
        cont = 'y'
        while cont == 'y':
            idea = input_loop('Idea sentence: ')
            if idea:
                self._idea_sentences.append(idea)
            cont = input('Continue? (y/n): ')

        # Semantic Tags
        cont = 'y'
        while cont == 'y':
            tag = input_loop('Semantic tag: ')
            if tag:
                self._tags.append(tag)
            cont = input('Continue? (y/n): ')

        # References
        cont = 'y'
        while cont == 'y':
            refs = input_loop('Reference of Interest: ')
            if refs:
                self._refs.append(refs)
            cont = input('Continue? (y/n): ')

        self.save()

    def edit(self):
        pass

    def delete(self):
        if self._created_at:
            os.remove('ideas/{}.json'.format(self._created_at))


def input_loop(prompt):
    correct = None
    text = None
    while correct != 'y':
        text = input(prompt)
        correct = input('Is this correct? (y/n): ')
    return text


if __name__ == '__main__':
    running = True

    while running:
        selection = input('(c)reate, (e)dit, (s)earch, (d)elete, (q)uit: ')
        if selection == 'c':
            idea = Idea()
            idea.create()
        elif selection == 'e':
            pass
        elif selection == 's':
            pass
        elif selection == 'd':
            pass
        elif selection == 'q':
            running = False
