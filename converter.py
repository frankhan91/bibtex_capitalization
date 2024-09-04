import re

def load_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

def wrap_capitals_in_word(word):
    # Find each capital letter and wrap it with {}
    return re.sub(r'([A-Z])', r'{\1}', word)

# Function to wrap words with {} for LaTeX capitalization preservation
def wrap_with_braces(content, formatted_words):
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Only process lines that start with 'title=' (with optional leading spaces)
        if re.match(r'^\s*title=', line):
            for phrase in formatted_words:
                # Break down the phrase into words and hyphenated parts, then wrap capitals
                wrapped_phrase = '-'.join([wrap_capitals_in_word(part) for part in phrase.split('-')])
                # Regex pattern to find the phrase not already wrapped in {}
                pattern = re.compile(r'(?<!{{)(\b{}\b)(?!}})'.format(re.escape(phrase)), re.IGNORECASE)
                # Replace the phrase with the wrapped version and print each change
                lines[i], num_subs = pattern.subn(wrapped_phrase, line)
                if num_subs > 0:
                    print(f"Modified line {i+1:4}: {lines[i]}")
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
    bib_file_path = 'ref.bib'  # Replace with your .bib file path
    formatted_words_path = 'formatted_words.txt'  # File storing words to be capitalized (e.g., "PDE", "Monte Carlo")
    process_bib_file(bib_file_path, formatted_words_path)
