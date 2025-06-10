from filemanager import FileManager
from textanalyzer import TextAnalyzer

class Task2:
    def __init__(self):
        self.text_analyzer = TextAnalyzer('')
        self.path_to_txt = r'C:\Users\LENOVO\353502_Klepatskiy_10\IGI\LR4\result.txt'
        self.path_to_zip = r'C:\Users\LENOVO\353502_Klepatskiy_10\IGI\LR4\result.zip'
        text = FileManager.read_from_file(r'C:\Users\LENOVO\353502_Klepatskiy_10\IGI\LR4\data.txt')
        self.text_analyzer.set_text(text)

    def run(self):
        while True:
            print(
                'Choose one of the options:\n'
                '0 Back\n'
                '1) Get info about zip archive\n'
                '2) Get sentences count\n'
                '3) Get sentences types count\n'
                '4) Get average length of sentences\n'
                '5) Get average length of words\n'
                '6) Get emojis count\n'
                '7) Print words with "g" to "o"\n'
                '8) write email\n'
                '9) How much words in the line\n'
                '10) Find largest word and his index\n'
                '11) Print odd numbers words\n'
            )
            option = face_input()
            match option:
                case 0:
                    return
                case 1:
                    FileManager.get_archive_info(self.path_to_zip)                   
                case 2:
                    result = self.text_analyzer.count_sentences()
                    print(result)
                    FileManager.write_to_file(
                        str(result),
                        self.path_to_txt
                    )
                    FileManager.archive_file(
                        self.path_to_txt,
                        self.path_to_zip
                    )
                case 3:
                    narrative, interrogative, incentive = self.text_analyzer.count_sentence_types()
                    result = (
                        f'count of narrative sentences: {narrative}\n'
                        f'count of interrogative sentences: {interrogative}\n'
                        f'count of incentive sentences: {incentive}\n'
                    )
                    print(result)
                    FileManager.write_to_file(
                        result,
                        self.path_to_txt
                    )
                    FileManager.archive_file(
                        self.path_to_txt,
                        self.path_to_zip
                    )
                case 4:
                    result = self.text_analyzer.count_avg_sentences_length()
                    print(result)
                    FileManager.write_to_file(
                        str(result),
                        self.path_to_txt
                    )
                    FileManager.archive_file(
                        self.path_to_txt,
                        self.path_to_zip
                    )
                case 5:
                    result = self.text_analyzer.count_avg_words_length()
                    print(result)
                    FileManager.write_to_file(
                        str(result),
                        self.path_to_txt
                    )
                    FileManager.archive_file(
                        self.path_to_txt,
                        self.path_to_zip
                    )
                case 6:
                    result = self.text_analyzer.count_emojis()
                    print(result)
                    FileManager.write_to_file(
                        str(result),
                        self.path_to_txt
                    )
                    FileManager.archive_file(
                        self.path_to_txt,
                        self.path_to_zip
                    )
                case 7:
                    result = self.text_analyzer.words_within_char_range()
                    print(result)
                    FileManager.write_to_file(
                        str(result),
                        self.path_to_txt
                    )
                    FileManager.archive_file(
                        self.path_to_txt,
                        self.path_to_zip
                    )
                case 8:
                    result = self.text_analyzer.is_valid_email(input())
                    print(result)
                    FileManager.write_to_file(
                        str(result),
                        self.path_to_txt
                    )
                    FileManager.archive_file(
                        self.path_to_txt,
                        self.path_to_zip
                    )
                case 9:
                    result = self.text_analyzer.count_words(input())
                    print(result)
                    FileManager.write_to_file(
                        str(result),
                        self.path_to_txt
                    )
                    FileManager.archive_file(
                        self.path_to_txt,
                        self.path_to_zip
                    )
                case 10:
                    result = self.text_analyzer.find_longest_word()
                    print(result)
                    FileManager.write_to_file(
                        str(result),
                        self.path_to_txt
                    )
                    FileManager.archive_file(
                        self.path_to_txt,
                        self.path_to_zip
                    )
                case 11:
                    result = self.text_analyzer.get_odd_words()
                    print(result)
                    FileManager.write_to_file(
                        str(result),
                        self.path_to_txt
                    )
                    FileManager.archive_file(
                        self.path_to_txt,
                        self.path_to_zip
                    )    
def face_input():
    while(True):
        try:
            value = int(input())
            if 0 <= value <= 11:
                return value
        except:
            print('Try again!')