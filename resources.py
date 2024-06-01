import json
import os
from typing import List
def print_with_indent(value, indent=0):
    identation = '\t' * indent               #function to make indent of titles
    print(identation + str(value))

class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title                   #main brick/class
        self.entries = entries
        self.parent = parent

    def add_entry(self, entry):
        self.entries.append(entry)           #add new entry
        entry.parent = self

    def __str__(self):                       # method returns a human-readable,string representation of an object.
        return self.title

    @classmethod
    def from_json(cls, value: dict):         #deserializing json data to object(dict)
        new_entry = cls(value['title'])
        for item in value.get('entries', []):
            new_entry.add_entry(cls.from_json(item))
        return new_entry

    @classmethod
    def load(cls, filename):                 #save and receive from file
        with open(filename, "r", encoding="utf-8") as f:
            content = json.load(f)
            return cls.from_json(content)

    def print_entries(self, indent=0):
        print_with_indent(self, indent)     #print entries With indent
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def json(self):                         #serializing object to dict
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return res

    def save(self, path):                   #receive the path to the file and save it to json object
        json_data = self.json()
        file_path = os.path.join(path, f"{self.title}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries: List[Entry] = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path)
        else:
            for filename in os.listdir(self.data_path):
                if filename.endswith('json'):
                    entry = Entry.load(os.path.join(self.data_path, filename))
                    self.entries.append(entry)
        return self

    def add_entry(self, title: str):
        new_entry = Entry(title)
        new_entry.parent = self
        self.entries.append(new_entry)

if __name__ == '__main__':
    groceries = Entry('Продукты')
    category = Entry('Мясное')

    category.add_entry(Entry('Курица'))
    category.add_entry(Entry('Говядина'))
    category.add_entry(Entry('Колбаса'))

    groceries.add_entry(category)

    groceries.print_entries()

    res = groceries.json()
    print(json.dumps(res, ensure_ascii=False, indent=4))
