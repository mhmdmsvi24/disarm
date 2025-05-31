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

To learn more about PDF documents checkout [Didar Stevens Personal Website](https://blog.didierstevens.com/programs/pdf-tools/),
the current research section is also got a handbook of this website

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
## Research

1. The two following indicate that the PDF document contains JavaScript. Almost all malicious PDF
   documents that I’ve found in the wild contain JavaScript (to exploit a JavaScript vulnerability
   and/or to execute a heap spray). Of course, you can also find JavaScript in PDF documents without
   malicious intend.

- /JS
- /JavaScript

1. The two following indicate an automatic action to be performed when the page/document is viewed.
   All malicious PDF documents with JavaScript I’ve seen in the wild had an automatic action to
   launch the JavaScript without user interaction, The combination of automatic action  and
   JavaScript makes a PDF document very suspicious.

- /AA
- /OpenAction

that currently for level 1 we only need:

- /JS
- /JavaScript
- /AA
- /OpenAction

1. `/page`: another indiction of a malicious pdf can be `/page` if the document only contains 1 page
   there's a chance for malicious activity
2. `/ObjStm`: object stream can also be used to contain other objects
3. `/RichMedia`: for embeded flash


### `incremental updates`:
Legitimate Feature, Abused for Attacks: Incremental updates are a standard PDF feature that allows
appending changes (e.g., signatures, annotations) without modifying the original content. However,
attackers exploit this to:

1. Bypass Signature Validation: Append malicious content (scripts, pages, or code) after a valid
digital signature. The signature remains valid because the original content is untouched, but
the new content executes when opened.
2. Hide Malicious Layers: Add obfuscated JavaScript or exploits incrementally, making analysis
harder.
3. Evil Annotation Attack (EAA) and Sneaky Signature Attack (SSA): These techniques use incremental
updates to overlay malicious content (e.g., fake UI elements, hidden scripts) on certified/signed
PDFs. Users see the malicious overlay, while the PDF appears valid.
4. Incremental Saving Attack (ISA): Attackers append unsigned content (e.g., malicious JavaScript,
embedded payloads) after the signature. Many PDF readers fail to detect these unauthorized
updates, allowing code execution.
5. Obfuscation via Revision History: Malware authors trial different exploit versions via
incremental updates, creating a "revision history" that complicates reverse engineering.
