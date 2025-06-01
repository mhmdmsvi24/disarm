# PDF Basics series by Angeal Albertini Part 1

> [!NOTE]
> This series contain many PDF slides that you can find in his GitHub
> [here](https://github.com/angea/PDF101)

1. PDFs are series of codes that define static content of each page, in the PDF world any thing
   other than white space and new line character (\n) is ignored such as:

   - 0x00 Null
   - 0x09 Tab
   - 0xA Line Feed
   - 0x0C Form Feed
   - 0x0D Carriage Return
   - 0x20 Space

    Mixing EOL style is also possible so be careful to don't mix your style otherwise it will
    result in Offset issue that we'll talk more about it latter.

2. PDFs start with a version number: `%PDF-1.3` this is valid signature, this is kinda a comment
   that is recognized you can write comments with `%` symbol and it's valid until the end of line

3. After the signature comes the __file body__ and it's static content that is followed by __xref__
   followed by __trailer__
   ```
    %PDF-1.3
    %file body here
    xref
    %xref table here
    trailer
    %trailer content here
    startxref (this is a pointer to where xref keyword starts)
    %%EOL (lastly to mark end of line that is double percent)
   ```

   we'll learn more about all of this later

4. Name Objects: strings that start with a slash and they are case sensitive e.g. `/Name`, `/Font`
   and `/Name` != `/name`, some of the Name Objects are recognized by the parser like `/Root` and
   for debugging purposes you can change it to sth like `/root` to see what happen afterwards.

   also note that Name Object can't start with numbers

5. Dictionaries: dicts are group of key/values enclosed in double brackets `<<>>` except that every
   key has to be a name object e.g. `<</Name 1>>` that is equal to /Name = 1, in dictionaries
   white spaces are ignored and they key can be a dict itself so:

   `<</Name 1>>`: is valid
   `<<           /Name /Meow >>`: is valid
   `<</Name <<>> >>`: is valid

6. Indirect Objects: an indirect object is a object number and generation number which look sth like
   this:

   ```
   1 0 obj
   3
   endobj
   ```

   here we defined an object number 1 and generation of 0 (it's 0 almost most of the time), here
   we only declared the value of 3 but most of the time its dict `<<>>`.

   ```
   2 0 obj
   << /MyValue 1 0 R>>
   endobj
   ```

   here we defined a dict with a key of MyValue but with the value that is reference to `1 0 obj`
   object so when we want to reference to an object we declare: `objNumber objGen R` the uppercase
   `R` means reference.

   also note that ObjGen always (%99) is 0 and objNumber is based on how many objects you create
   and they are kinda your objects plate number.

7. file body: file body is sequence of indirect objects (order doesn't matter), note that a PDF
   document is defined by tree of objects

8. trailer: it's a dictionary that defines `/Root` name:
   ```
    %PDF-1.3
    1 0 obj
    <<>>
    endobj
    xref
    %xref table here
    trailer
    << /Root 1 0 R>>
    startxref (this is a pointer to where xref keyword starts)
    %%EOL (lastly to mark end of line that is double percent)
   ```

## Creating our first document

the object that `/Root` points to is a special object that refers to the page tree via pages name
and pages referes to another object that must've `/Type` key assigned to `/Catalog` value and it
will define it related objects as `/Kids` key that will contain the specific page object
reference in an array, if the Kids dict has many children it must be defined in `/Kids` dict

so as a recap obj 1 is a `/Catalog` that `/Root` points to and it contains `/Pages` name object that
will point to obj 2 that has `/Kids` and `/Count`.

to be more clear let's describe it like this: there must be a Root object in the document that our
trailer points to, then the root document has `/Type` of `/Catalog` name objects, think of it as a
catalog that has many pages and you define each page one by one to create a catalog about your
university.

The root object and the owner of catalog is a wrapper around another object that will define our
catalog pages with specific `/Kids` name object.

The `/Count` name object defiens the number of pages your PDF will have, change it to see how many
pages your PDF viewer shows.

```
%PDF-1.3

1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

xref
%xref table here
trailer
<< /Root 1 0 R>>
startxref
%%EOL
```

`/Kids` is an array that contains the reference to the object that children object.

Lets declare the children object that starts with `/Type` of `/Page` name objects and then
declare `/Parent` name object that defines whom this kid is related to, that is object 2 here (the
page parent).

```
3 0 obj
<<
/Type /Page
/Parent 2 0 R
>>
```

> [!Note]
> When a dict contains many name objects they are actually key/value pairs so the above code reads
> as follows: `/Type` of `/Page`, `/Parent` of `2 0 R`, they key can be anything a dict, a name
> object, literal number, string, etc...

After all of these now we need to define resources for each page, it might not make sense at first
but imagine a word document where you create a text box with a Arial font and another box below it
with other type of fonts now think of all of these textboxs as objects that have their own resources
staticly defined for each one separetly.

If you recall from the beginning, a PDF document contains static resources for everything, like a
HTML document with images, etc that don't have any JS yet so everything is staticly defined.

Lets try to mimic adding a textbox in our word document gui step by step:

1. Select page where you want to add textbox
2. Draw the textbox where you want
3. Type what you want
4. Adjust the font type based on your preference

When creating a PDF file it's a little different than that but almost the same idea.

For this we must add an object that must define it's `/Parent` page so it's basically telling where
its gonna reside, then we'll define our static resources for this particular object (remember
everything has its own static resources), so we start with `/Resources` name object followed by a
dict that contains:

- `/Font`: name object that that will define this particular textbox font
followed by a dict as its value that has =>
- `/F1`: name object that is our font resource identifier
followed by a dict as its value that has =>
- `/Type` of `/Font`, `/Subtype` of `/Type` and `/BaseFont` of `/Arial`
- `/Contents` of `4 0 R`: 4 0 R here is an object that we'll define later to declare what the
  textbox will have inside it.

```
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Arial >> >> >>
/Contents 4 0 R
>>
endobj
```

`/Resources` name object is kinda messy but you'll get used to it for better clearity in you mind
look at it like this:

1. `/Resources` = `<< /Font >>`
2. `/Font` = `<< /F1 >>`
3. `/F1` = `<< /Type: /Font, /Subtype: /Type1, /BaseFont: /Arial >>`

The above syntax separeted with comma and colon is not correct and it's just for clearity.

Now you can Kinda get it what happenes when you create a textbox in your word/pdf document editor.

The next thing we need to define is actuall content of the textbox with `/Content` that refers
to another object that we'll create.

So for a recap we declared a `/Catalog` that contain `/Pages` (it's catalog of pages) then we
defined first page and what it contains that for now is obj 3, this object is properties of our
page object that will contain other objects such as texts that we will define as `/Contents`.

```
%PDF-1.3
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

% The code is indented for better readability
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/Resources <<
    /Font
        <<
            /F1
                <<
                    /Type /Font
                    /Subtype /Type1
                    /BaseFont /Arial
                >>
            >>
        >>
    /Contents 4 0 R
>>
endobj

xref
%xref table here
trailer
<< /Root 1 0 R>>
startxref
%%EOL
```

### Introduction to streams

So far everything is text, but a question arises here, what about images and gifs or other static
contents (Binary Data) ?

Stream Objects are objects what contain whatever you want, stream object contains a stream `:)` that
comes after the first dict, note that streams can contain anything and they start with inside our
object that we created for our text:

```
4 0 obj
<<
    % empty for now
>>
stream
    % stream data
endstream
endobj
```

Back to the first dict, it will contain the `/Length` key that can assigned with another object like
`/Length 5 0 R` or a literal number that is length of binray data in the stream but for now it's not
requried.

The Stream contains other things such as `BT` (begin text) and `ET` (end text), inside of these
operators we'll define `Tf` (text font) that takes two parameters: `/F1 100 Tf`, first parameter
is the font resource in the page we declared previously and latter the font size.

Another operator that we need for the font is the location of the text for that we use `Td` operator
that takes the cordinates: `x y Td`: `10 400 Td`

- x: offset from left
- y: offset from bottom

`0 0 Td`: will put text in the extreme bottom left

```
4 0 obj
    <<
        % empty for now
    >>
    stream
        BT
            /F1 100 Tf
            10 400 Td
        ET
    endstream
endobj
```

The final requirement is the text itself that can be literal string, parenthesis, white space and
standard escaping `\n`, `\r\n`, note that escaping is in octal (Hell\147 World).

To declare the Text string we use `Tj` operator that takes the litral string inside parenthesis

```
4 0 obj
    <<
        % The length here is 43 (88 with indentation) to aquire it you must count the offset
        % starting from `BT` down to the `ET` and you code editor will count it for you
        /Length 43
    >>

    stream
        BT
            /F1 100 Tf
            10 400 Td
            (Hello World!) Tj
        ET
    endstream
endobj
```

Now let's go back to our stream empty dict that is more about information about the stream, here
we must declare `/Length` key and it value must be the whole character length of the stream starting
from `BT` down to the `ET`, to calculate that highlight it follows:

![Highlight](../../static/01-stream-length.png)

then in your editor you can see the number of characters selected like this:

![Selected](../../static/01-stream-length-selected.png)

### Finally:

```
%PDF-1.3
1 0 obj
<< /Type /Catalog /Pages 2 0 R>>
endobj

2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj

3 0 obj
<< /Type /Page /Parent 2 0 R
/Resources << /Font << /F1 << /Type /Font
/Subtype /Type1 /BaseFont /Arial >> >> >>
/Contents 4 0 R
>>
endobj

4 0 obj
<<
/Length 44
>>

stream
BT
/F1 100 Tf
10 400 Td
(Hello World!) Tj
ET
endstream

endobj

trailer
<< /Root 1 0 R>>
```

> [!Note]
> You can run save the text file as `.pdf` and run it in chrome and you can see that runs perfectly
> but this doesn't mean your PDF file is correct, most of the tools such as web browsers have high
> fault tolerance if you want to test it run it in __Adobe Reader__ if runs without any erros such
> as __Do you want to save the changes__ while you want to close it this means that the file is not
> perfect enough.

```
4 0 obj
<< /Length 44 >>
stream
BT
/F1 100 Tf
10 400 Td
(Hello World!) Tj
ET
endstream
endobj
```

Now our page contents is finished.

> [!Note]
> Another Tool that is mentioned in this series is Summatra and open source tool to view PDFs live
> so any changes will be appeared live, you can download it [here](https://github.com/sumatrapdfreader/sumatrapdf/releases)
> for linux you must build it yourself.

### Cross Reference table

The xref table in a PDF file maps each indirect object number to the byte offset where that object
starts in the file. This allows PDF readers to quickly locate and load objects without scanning the
entire file.

we declared 4 objects plus 1 object that PDFs define by iteslf and its null so basically we have
`n (creted by us) + 1 (global)` objects.

```
%PDF-1.3
1 0 obj
<< /Type /Catalog /Pages 2 0 R>>
endobj

2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj

3 0 obj
<< /Type /Page /Parent 2 0 R
/Resources << /Font << /F1 << /Type /Font
/Subtype /Type1 /BaseFont /Arial >> >> >>
/Contents 4 0 R
>>
endobj

4 0 obj
<< /Length 44 >>
stream
BT
/F1 100 Tf
10 400 Td
(Hello World!) Tj
ET
endstream
endobj

xref
0 5

trailer
<< /Root 1 0 R /Size 5 >>
```

The `0 5` — indicates that the table entries start at object number 0 and cover 5 objects (object
numbers 0 through 4).

Each entry in the xref table is exactly 20 bytes long and follows this fixed format:
`nnnnnnnnnnn ggggg n/f \r\n`.

```
xref
0 5
000000000000 65535 f\0x20
000000000010 00000 n\0x20
000000000059 00000 n\0x20
000000000115 00000 n\0x20
000000000265 00000 n\0x20
```

| Part        | Description                                                       | Length(chars offset) |
| ----------- | ----------------------------------------------------------------- | -------------------- |
| nnnnnnnnnnn | Byte offset of the object in the file (padded with leading zeros) | 10                   |
| ggggg       | Generation number of the object (padded with leading zeros)       | 5                    |
| n or f      | Entry status: n = in-use, f = free (unused)                       | 1                    |
| \r\n or \n  | End-of-line characters (not shown in your snippet)                | 2                    |

Summary:

| Field           | Meaning                                                                          |
| --------------- | -------------------------------------------------------------------------------- |
| 10-digit number | The exact byte offset (starting position) of the object in the PDF file. Leading |
zeros pad it to 10 characters.
|5-digit number|	The generation number of the object, padded with leading zeros. Usually 00000
for most objects; 65535 is special for free objects.|
|1-letter flag|	n means the object is in use; f means the object is free (not currently used).|
|Space (0x20)|	Separator between fields (space character).|

the first table is the global table with flag of `f` that means free.

You can see 3 columns in the tables the first column is the offset column and you must calculate
each object offset like this:

![xref offsets](../static/01-stream-xref-offset.png)

the offset column lenght must be 10 then 5 zeros and then 1 letter and then a mandatory space that
I shown it as `\0x20` cause my editor trim it.

Lastly add the number of objects to the `/Size` Key in the trailer and we're done.

```
trailer
<< /Root 1 0 R /Size 5 >>
```

> [!Note]
> If you're using vscode you can install the pdf [syntax highlighter](https://marketplace.visualstudio.com/items?itemName=frinkr.pdf)
> with this extention you can also add the next setting rule for better developer experience

> [!Note]
> To prevent trimming spaces in VsCode add the following rule to your vscode setting

```
// PDF
"[pdf]": {
    "files.trimTrailingWhitespace": false
}
```

Now we need to define startxref and its a pointer to where our xref offest starts, to prevent doing
this manually you can use `mutool clean` tool to automate this step

```
startxref
359
```

Now if you open the file with Adobe Reader You should've get no errors that counts as a Victroyyyy

to continue we can use `/Filter` that basically is algorithms that you can stack on top of eachother
like `/ASCIIHexDecode` that takes any content and turns it into pure ascii that is usefull to do
tricks with it or `/FlateDecode` that implements ZIP compression and outputes HEX and it's not
editable but we can stack both to `/Filter [/ASCIIHexDecode, /FlateDecode]` to get both compression
and ascii output

Try to implement more complex structure by yoursef there's also a version of mine: [Project](../PDFs/01-basic.pdf)
Each time I also do a little overwork and implement some extra features that is not mentioned yet
you don't need them just seeing them and getting used to the syntax is enough.
