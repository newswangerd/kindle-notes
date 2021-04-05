# Installation

```shell
git clone git@github.com:newswangerd/kindle-notes.git
pip install -e kindle-notes
```

# Usage

## Taking Notes

`kindle-notes` allows insterting some basic formatting on your kindle while you're taking notes. For example, highlighting a piece of text and adding `-` or `#`, `##`, `###`... etc will format the highlighted block of text with the selected markdown formatter.

For example highlighting "Example Heading" with `##` will result in:

```markdown
## Example Heading
```

In your exported notes. This can be used to mark chapter titles and subheadings to make it easier to get around your notes.

## Exporting Notes

To export your notes, simply copy the `My Clippings.txt` file off of your kindle and run the following commands

```shell
$ kindle-notes kindle-notes examples/My\ Clippings.txt 
0. My Example Book
Select a book: 0
Removing duplicates 0
Notes saved to /home/david/code/kindle-notes/examples/My Example Book.md.
```

This will produce the following markdown file, which you can see here: [Example Notes](examples/My Example Book.md)

```
# My Example Book

- I'm a note! (location 3286)
> I'm a highlight with a note. (3285-3286)

### I'm a level 3 header (3588-3588)

> I'm another highlight (3588-3588)

- I'm a highlight that will appear as a bullet. (3600-3600)
```

**NOTE** `My Clippings.txt` can only create new entries. Changing an existing highlight or note will simply create a new entry in `My Clippings.txt`. Kindle notes does it's best to try and de duplicate these entries by using the latest entry for each location that's indexed, but this method isn't perfect and your mileage may vary.