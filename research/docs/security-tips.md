# List of Notes about PDF Security concerns

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

### PDF Dicts

1. The two following indicate that the PDF document contains JavaScript. Almost all malicious PDF
   documents that I’ve found in the wild contain JavaScript (to exploit a JavaScript vulnerability
   and/or to execute a heap spray). Of course, you can also find JavaScript in PDF documents without
   malicious intend.

- `/JS`
- `/JavaScript`

2. The two following indicate an automatic action to be performed when the page/document is viewed.
   All malicious PDF documents with JavaScript I’ve seen in the wild had an automatic action to
   launch the JavaScript without user interaction, The combination of automatic action  and
   JavaScript makes a PDF document very suspicious.

- `/AA`
- `/OpenAction`

that currently for level 1 we only need:

- `/JS`
- `/JavaScript`
- `/AA`
- `/OpenAction`

3. `/page`: another indiction of a malicious pdf can be `/page` if the document only contains 1 page
   there's a chance for malicious activity
4. `/ObjStm`: object stream can also be used to contain other objects
5. `/RichMedia`: for embeded flash
6. `xref`: missing xref table may be a reason for poorly edited pdf file for malicious activity
7. `/Filter`: filter dict to hide malicious output using encoding


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
