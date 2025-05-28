import argparse
import subprocess
import sys
from pathlib import Path


class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"Error: {message}")
        self.print_help()
        sys.exit(2)


parser = CustomArgumentParser(
    description="Scans PDFs for any malicious activity to triage and \
                                 analyze them",
    usage="%(prog)s [options] source_file",
)

#  positional arguments
parser.add_argument(
    "-l",
    "--level",
    type=int,
    help="security severity level, minimum of 1 and maximum of 3. The higher the stricter the program will be, defaults to 2",
    default=1,
    choices=[1, 2, 3],
)

parser.add_argument(
    "-d", "--directory", type=str, help="Path to the PDF directory you want to diagnose"
)

parser.add_argument(
    "-f", "--file", type=str, help="Path to the PDF file you want to diagnose"
)

parser.add_argument(
    "-w",
    "--watch",
    type=str,
    help="Path to the PDF directory you want to watch to scan and secure PDFs",
)

parser.add_argument(
    "-v", "--verbose", action="store_true", help="provide operation information"
)

# Parsed arguments
args = parser.parse_args()

level = args.level
directory_path = args.directory
file_path = args.file
watch = args.watch


if (
    (file_path and directory_path)
    or (watch and file_path)
    or (watch and directory_path)
):
    parser.error(
        "incompatible options: file & directory or watch can't be used at the same time"
    )

print(level, directory_path, file_path, watch)

file_path = Path.home() / file_path
command = subprocess.run(
    ["python3", "pdfid", file_path], capture_output=True, text=True
)

data_lines = command.stdout.splitlines()[2:]

# Pretty subprocess (pdfid) output
keyword_counts = {}
for line in data_lines:
    # Strip whitespace
    line = line.strip()
    if not line:
        continue
    # Split by whitespace, maxsplit=1 to separate key and value
    parts = line.split(maxsplit=1)
    if len(parts) == 2:
        key, value = parts
        try:
            keyword_counts[key] = int(value)
        except ValueError:
            # Not a number, ignore or handle differently
            pass


# Level 1
def level_1(dict):
    suspicious_keys = ["/JS", "/JavaScript", "/AA", "/OpenAction"]
    threats_found = {}
    threats = 0

    print("Hunting Basic Level 1 Threats...\n")
    for key in suspicious_keys:
        count = dict.get(key, 0)
        if count > 0:
            threats_found[key] = count
            threats += 1
        print(f"{key}: {count}")
    print("\n")

    if threats_found:
        print("Suspicous Items Found:\n")


if level == 1:
    level_1(keyword_counts)

# for keyword in keyword_counts:
#     print(keyword, keyword_counts[keyword])

# for node in xml_doc.getElementsByTagName('Keyword'):
#     if node.getAttribute("Name") in ['/JS', "/JavaScript", "/AA", "/OpenAction"]:
#         name = node.getAttribute("Name")
#         count = node.getAttribute("Count")
#         print(f"{name}: {count}")
