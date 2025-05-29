# secure-pdf

## contribute

1. clone
2. `source venv/bin/activate`
3. `pip install pdfid`
4. check todo.md and pick a task
5. create a branch for yourself
6. code

if you found anything
1. Add your findings about suspicious pdfs and how to stop them in the doc
2. add it as todo if contributers agreed upon

## suspicious pdf file attributes

1. The two following indicate that the PDF document contains JavaScript. Almost all malicious PDF documents that I’ve found in the wild contain JavaScript (to exploit a JavaScript vulnerability and/or to execute a heap spray). Of course, you can also find JavaScript in PDF documents without malicious intend.

- /JS
- /JavaScript

2. The two following indicate an automatic action to be performed when the page/document is viewed. All malicious PDF documents with JavaScript I’ve seen in the wild had an automatic action to launch the JavaScript without user interaction.

- /AA
- /OpenAction

## PDFiD output

```
<Keywords>
    <Keyword Name="obj" Count="579" HexcodeCount="0"/>
    <Keyword Name="endobj" Count="574" HexcodeCount="0"/>
    <Keyword Name="stream" Count="287" HexcodeCount="0"/>
    <Keyword Name="endstream" Count="286" HexcodeCount="0"/>
    <Keyword Name="xref" Count="0" HexcodeCount="0"/>
    <Keyword Name="trailer" Count="0" HexcodeCount="0"/>
    <Keyword Name="startxref" Count="0" HexcodeCount="0"/>
    <Keyword Name="/Page" Count="96" HexcodeCount="0"/>
    <Keyword Name="/Encrypt" Count="0" HexcodeCount="0"/>
    <Keyword Name="/ObjStm" Count="0" HexcodeCount="0"/>
    <Keyword Name="/JS" Count="0" HexcodeCount="0"/>
    <Keyword Name="/JavaScript" Count="0" HexcodeCount="0"/>
    <Keyword Name="/AA" Count="1" HexcodeCount="0"/>
    <Keyword Name="/OpenAction" Count="0" HexcodeCount="0"/>
    <Keyword Name="/AcroForm" Count="0" HexcodeCount="0"/>
    <Keyword Name="/JBIG2Decode" Count="0" HexcodeCount="0"/>
    <Keyword Name="/RichMedia" Count="0" HexcodeCount="0"/>
    <Keyword Name="/Launch" Count="0" HexcodeCount="0"/>
    <Keyword Name="/EmbeddedFile" Count="0" HexcodeCount="0"/>
    <Keyword Name="/XFA" Count="0" HexcodeCount="0"/>
    <Keyword Name="/Colors &gt; 2^24" Count="0" HexcodeCount="0"/>
</Keywords>
```

that currently for level 1 we only need:

- /JS
- /JavaScript
- /AA
- /OpenAction
