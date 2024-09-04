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
def process_bib_file(bib_file_path, formatted_words_path):
    print(f"File to process: {bib_file_path}")
    formatted_words = load_words(formatted_words_path)
    
    with open(bib_file_path, 'r', encoding='utf-8') as input_file:
        content = input_file.read()
    modified_content = wrap_with_braces(content, formatted_words)
    output_file_path = bib_file_path.rsplit('.', 1)
    output_file_path = output_file_path[0] + '_modified.' + output_file_path[1]
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(modified_content)
    print(f"Modified content written to: {output_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a .bib file.')
    parser.add_argument('-b', '--bib', default='test.bib', help='Path to the .bib file')
    parser.add_argument('-w', '--words', default='formatted_words.txt', help='Path to the file storing correctly captialized words')
    args = parser.parse_args()
    process_bib_file(args.bib, args.words)
