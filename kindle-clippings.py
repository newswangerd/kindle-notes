import re
from dateutil import parser


def parse_clippings(text):
    note_reg = re.compile('Location ([0-9]+)')
    highlight_reg = re.compile('Location ([0-9]+)-([0-9]+)')

    notes = text.split("==========")
    books = {}

    for note in notes:
        data = note.strip().split('\n')
        if len(data) < 3:
            continue
        book = data[0].strip()
        location = data[1].strip()

        entry = {"content": data[3].strip()}
        entry['date'] = parser.parse(location.strip().split('Added on ')[1])

        if 'Highlight' in location:
            match = highlight_reg.search(location).groups()
            entry['location'] = match
            entry['type'] = 'highlight'

        if 'Note' in location:
            match = note_reg.search(location).groups()
            entry['location'] = match
            entry['type'] = 'note'

        if book in books:
            books[book].append(entry)
        else:
            books[book] = [entry, ]
    return books


MARKDOWN_FORMATTERS = [
    '#####'
    '####',
    '###',
    '##',
    '#',
    '-'
]


def render_markdown(book, title):
    def get_location(e):
        # ensures notes are always above their highlights
        if (e['type'] == 'note'):
            return int(e['location'][0]) - 1
        return int(e['location'][1])

    book.sort(key=get_location)

    markdown = ['# ' + title, '']

    format_next = None
    for (index, entry) in enumerate(book):
        if entry['type'] == 'note':
            for formatter in MARKDOWN_FORMATTERS:
                if entry['content'].startswith(formatter):
                    if (len(book) - 1 >= index and book[index + 1]['type'] == 'highlight'):
                        format_next = formatter
                    break

            if not format_next:
                markdown.append('- {} (location {})'.format(
                    entry['content'],
                    entry['location'][0]
                ))

                markdown.append('')

        if entry['type'] == 'highlight':

            if not format_next:
                markdown.append('> {} ({}-{})'.format(
                    entry['content'],
                    entry['location'][0],
                    entry['location'][1],
                ))

            else:
                markdown.append('{} {} ({}-{})'.format(
                    format_next,
                    entry['content'],
                    entry['location'][0],
                    entry['location'][1],
                ))
                format_next = None

            markdown.append('')

    return '\n'.join(markdown)


def load_clippings(filepath):
    with open(filepath, 'r') as clippings:
        return str(clippings.read())


def deduplicate(book):
    '''
    if location range overlaps
        use the newest entry, throw out the rest

    not super efficient
    for each entry
        for each parsed entry
            if in range add to existing entry
            else create new entry
    '''

    # entries = [{"locations": (1,2), entry: {}}]
    deduped_highlights = []
    deduped_notes = []
    duplicate_count = 0

    for entry in book:
        if entry['type'] == 'highlight':
            start = int(entry['location'][0])
            end = int(entry['location'][1])
            duplicate_found = False
            new_entry_range = set(range(start, end + 1))

            for location in deduped_highlights:
                old_start = location['locations'][0]
                old_end = location['locations'][1]
                old_entry_range = set(range(old_start, old_end + 1))

                # if there is any overlap in the location ranges, set the
                # use the newest entry
                if not new_entry_range.isdisjoint(old_entry_range):

                    # In some cases highlights next to each other will overlap.
                    # to prevent these from getting removed, verify that they
                    # aren't the same highlight
                    if (old_end == start or old_start == end):
                        new_content = entry['content']
                        old_content = location['entry']['content']
                        if not (new_content.startswith(old_content)
                                or old_content.startswith(new_content)):
                            continue

                    duplicate_count += 1
                    if location['entry']['date'] > entry['date']:
                        location['entry'] = entry
                    location['locations'] = (start, end)
                    duplicate_found = True
                    break

            if not duplicate_found:
                deduped_highlights.append(
                    {'locations': (start, end), 'entry': entry})
        elif entry['type'] == 'note':
            # I'll add note deduping later
            deduped_notes.append(entry)

    print('Removing duplicates', duplicate_count)
    result = []

    for entry in deduped_highlights:
        result.append(entry['entry'])

    return result + deduped_notes


def main():
    raw = load_clippings('./MyClippings.txt')
    books = parse_clippings(raw)
    for i, key in enumerate(books.keys()):
        print('{}. {}'.format(i, key))

    book_index = input("Select a book: ")
    title = books.keys()[book_index]
    selected_book = books[title]

    md = render_markdown(deduplicate(selected_book), title)

    with open('out.md', 'w') as f:
        f.write(md)


main()
