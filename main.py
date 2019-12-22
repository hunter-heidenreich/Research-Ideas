import time
import json
import os

from glob import glob


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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

    def _add_or_edit(self, opt):
        sel = input('(a)dd, (e)dit, (d)elete: ')
        if sel == 'a':
            text = input_loop('New entry: ')
            if text:
                if opt == 's':
                    self._idea_sentences.append(text)
                elif opt == 't':
                    self._tags.append(text)
                elif opt == 'r':
                    self._refs.append(text)
        elif sel == 'e':
            print('Which one?')
            if opt == 's':
                x, i = display_list_as_opts(self._idea_sentences)
                edit = input_loop('Edit: ')
                if edit:
                    self._idea_sentences[x] = edit
            elif opt == 't':
                x, t = display_list_as_opts(self._tags)
                edit = input_loop('Edit: ')
                if edit:
                    self._tags[x] = edit
            elif opt == 'r':
                x, r = display_list_as_opts(self._refs)
                edit = input_loop('Edit: ')
                if edit:
                    self._refs[x] = edit
        elif sel == 'd':
            print('Which one?')
            if opt == 's':
                x, i = display_list_as_opts(self._idea_sentences)
                del self._idea_sentences[x]
            elif opt == 't':
                x, t = display_list_as_opts(self._tags)
                del self._tags[x]
            elif opt == 'r':
                x, r = display_list_as_opts(self._refs)
                del self._refs[x]

        self.save()

    def edit(self):
        r = True
        while r:
            print(self)
            sel = input('(s)entences, (t)ags, (r)eferences, (q)uit: ')

            if sel in 'srt':
                try:
                    self._add_or_edit(sel)
                except TypeError:
                    print('Invalid choice...')
            elif sel == 'q':
                r = False

    def delete(self):
        if self._created_at:
            os.remove('ideas/{}.json'.format(self._created_at))

        del self

    def __repr__(self):
        title = 'Created at: {}'.format(self._created_at)
        summary = 'Sentence summary:\n' + '\n'.join(['\t' + idea for idea in self._idea_sentences])
        tags = 'Tagged: ' + ', '.join(self._tags)
        references = 'References:\n' + '\n'.join(['\t' + r for r in self._refs])
        return title + '\n' + summary + '\n' + tags + '\n' + references

    def preview(self):
        print('{}: {}'.format(self._created_at, self._idea_sentences[0][:50]))

    def extract_text(self):
        return ' '.join(self._idea_sentences + self._tags)


def input_loop(prompt):
    correct = None
    text = None
    while correct != 'y':
        text = input(prompt)
        correct = input('Is this correct? (y/n): ')
    return text


def display_list_as_opts(lis):
    for i, li in enumerate(lis):
        print('({}) {}'.format(i, li))
    try:
        x = int(input('Select an option: '))
        if x >= 0:
            return x, lis[x]
        else:
            return None
    except ValueError:
        return None
    except IndexError:
        return None


def show_ideas():
    ideas = list(glob('ideas/*.json'))
    fst_sents = []
    for idea in ideas:
        fst_sents.append(json.load(open(idea))['idea'][0])

    ideas = list(zip(ideas, fst_sents))
    _, select = display_list_as_opts(ideas)
    if select:
        return Idea(filename=select[0])
    else:
        return None


def load_all_ideas():
    ideas = []
    for f in glob('ideas/*.json'):
        ideas.append(Idea(filename=f))
    return ideas


def tfidf_query(ideas, query, top=3):
    all_text = list(map(lambda i: i.extract_text(), ideas))

    tfidf = TfidfVectorizer()
    matx = tfidf.fit_transform([query] + all_text)
    sims = cosine_similarity(matx)[0, 1:]

    # Sort ideas by similarity
    ideas_by_sims = sorted(list(zip(all_ideas, sims)),
                           key=lambda x: x[1], reverse=True)

    # Filter out 0 similarity and only keep top 3
    ideas_by_sims = list(filter(lambda x: x[1] > 0, ideas_by_sims))[:top]

    return ideas_by_sims


if __name__ == '__main__':
    running = True

    while running:
        selection = input('(c)reate, (e)dit, (s)earch, (d)elete, (q)uit: ')
        if selection == 'c':
            Idea().create()
        elif selection == 'e':
            try:
                show_ideas().edit()
            except AttributeError:
                print('Error loading idea... Incorrect selection?')
            except TypeError:
                print('Error loading idea... Incorrect selection?')
        elif selection == 's':

            # Prepare ideas
            all_ideas = load_all_ideas()
            query = input('Query text: ')

            hits = tfidf_query(all_ideas, query)

            for idea in hits:
                i, sim = idea
                print('Similarity: {}'.format(sim))
                print(i)
                print('-' * 50)

        elif selection == 'd':
            try:
                ids = show_ideas()
                print(ids)
                ans = input('Is this correct? (y/n): ')
                if ans == 'y':
                    ids.delete()
                    del ids
            except AttributeError:
                print('Error loading idea... Incorrect selection?')
            except TypeError:
                print('Error loading idea... Incorrect selection?')
        elif selection == 'q':
            running = False
