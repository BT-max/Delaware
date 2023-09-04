import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

# Load the text
with open('/Users/abhishek/Downloads/test.txt', 'r') as f:
    text = f.read()

# Split the text into paragraphs
paragraphs = text.split('\n\n')


if __name__ == '__main__':
    # Loop over the paragraphs and sentences to find the keyword
    keyword = 'New Castle County'
    for paragraph in paragraphs:
        # Split the paragraph into sentences
        sentences = sent_tokenize(paragraph)
        # Loop over the sentences to find the keyword
        for sentence in sentences:
            # If the keyword is found in the sentence, print the entire paragraph
            if keyword in sentence:
                print(paragraph)
                break
