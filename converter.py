import re
import argparse

def load_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]

# Function to wrap words with {} for LaTeX capitalization preservation
def wrap_with_braces(content, formatted_words):
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Only process lines that start with 'title=' (with optional leading spaces)
        if re.match(r'^\s*title', line):
            original_line = line
            for phrase in formatted_words:
                # Break down the phrase into words and hyphenated parts, then wrap capitals
                wrapped_phrase = ''.join(['{' + char + '}' if char.isupper() else char for char in phrase])
                # Regex pattern to find the phrase not already wrapped in {}
                pattern = re.compile(r'(?<!{{)(\b' + re.escape(phrase) + r'\b)(?!}})', re.IGNORECASE)
                # Replace the phrase with the wrapped version
                line, num_subs = pattern.subn(wrapped_phrase, line)
                if num_subs > 0:
                    lines[i] = line
            if original_line != line:
                print(f"Modified line {i+1:4}: {line}")
    return '\n'.join(lines)

# Main function to process the bib file
def process_bib_file(bib_file_path, formatted_words_path, in_place=False, check=False):
    print(f"File to process: {bib_file_path}")
    formatted_words = load_words(formatted_words_path)

    with open(bib_file_path, 'r', encoding='utf-8') as input_file:
        content = input_file.read()
    modified_content = wrap_with_braces(content, formatted_words)
    changed = modified_content != content

    if check:
        if changed:
            print(f"Capitalization changes needed in: {bib_file_path}")
            return 1
        print(f"No capitalization changes needed in: {bib_file_path}")
        return 0

    if in_place:
        output_file_path = bib_file_path
    else:
        stem, ext = bib_file_path.rsplit('.', 1)
        output_file_path = f"{stem}_modified.{ext}"
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(modified_content)
    print(f"Modified content written to: {output_file_path}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a .bib file.')
    parser.add_argument('-b', '--bib', default='test.bib', help='Path to the .bib file')
    parser.add_argument('-w', '--words', default='formatted_words.txt', help='Path to the file storing correctly captialized words')
    parser.add_argument('--in-place', action='store_true', help='Overwrite the input file instead of writing to *_modified.bib')
    parser.add_argument('--check', action='store_true', help='Exit non-zero if changes would be made; do not write any file')
    args = parser.parse_args()
    raise SystemExit(process_bib_file(args.bib, args.words, in_place=args.in_place, check=args.check))
