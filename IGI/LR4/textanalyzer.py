import re


class TextAnalyzer:
    def __init__(self, text):
        self.text = text

    def set_text(self, text):
        self.text = text

    def count_sentences(self):
        return len(re.findall(r'[.?!](?=\s|$)', self.text))

    def count_sentence_types(self):
        narrative = len(re.findall(r'\.(?=\s|$)', self.text))
        interrogative = len(re.findall(r'\?(?=\s|$)', self.text))
        incentive = len(re.findall(r'\!(?=\s|$)', self.text))
        return narrative, interrogative, incentive

    def count_avg_sentences_length(self):
        sentences = re.findall(r'[^.?!]*[.!?]', self.text)
        words = [re.findall(r'\b\w+\b', sentence) for sentence in sentences]
        symbol_count = sum(len(word) for word in words)
        return symbol_count / len(sentences) if sentences else 0

    def count_avg_words_length(self):
        words = re.findall(r'\b\w+\b', self.text)
        symbol_count = sum(len(word) for word in words)
        return symbol_count / len(words) if words else 0

    def count_emojis(self):
        emojis = re.findall(r'[:;]-*(?:\(+|\)+|\[+|]+)', self.text)
        return len(emojis)

    def get_sentences(self):
        sentences = re.findall(r'[^.?!]*[.!?]', self.text)
        return sentences

    def words_within_char_range(self):
        start='g'
        end='o'
        words = re.findall(r'\b\w+\b', self.text)
        return [word for word in words if any(start <= char.lower() <= end for char in word)]

    def is_valid_email(self, email):
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        return re.fullmatch(pattern, email) is not None

    def count_words(self,text):
        words = re.findall(r'\b\w+\b',text)
        return len(words)

    def find_longest_word(self):
        words = re.findall(r'\b\w+\b', self.text)
        if not words:
            return None, -1
        longest = max(words, key=len)
        index = words.index(longest) + 1
        return longest, index

    def get_odd_words(self):
        words = re.findall(r'\b\w+\b', self.text)
        return [word for i, word in enumerate(words, start=1) if i % 2 != 0]