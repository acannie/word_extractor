import glob


class WordExtractor:
    # 単語の辞書 (最終的に返す)
    dictionary_set = set()

    # 単語を抽出するファイルの一覧
    FILE_LIST = glob.glob("./src/*")

    # 予約語一覧
    RESERVED_WORD_C = ["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum", "extern", "float", "for", "goto", "if",
                       "int", "long", "register", "return", "signed", "sizeof", "short", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"]

    # constructor
    def __init__(self):
        pass

    # 0 または 1 文字の単語を削除

    def __delete_short_word(self, dictionary_set=set()):
        new_dictionary_set = set(dictionary_set)
        for word in dictionary_set:
            if len(word) < 2:
                new_dictionary_set.remove(word)
        return new_dictionary_set

    # set 中の単語をすべて小文字に変換
    def __make_lower_in_dictionary_set(self, dictionary_set=set()):
        new_dictionary_set = set()
        for word in dictionary_set:
            new_dictionary_set.add(word.lower())
        return new_dictionary_set

    # 与えられた文字を 1 単語に追加すべきか判定

    def __should_add_alphabet_to_word(self, c="", word=""):
        if c.islower():  # 小文字のとき
            if word.isupper() and len(word) > 2:  # 単語すべてが大文字かつ 2 文字以上のとき
                return False
            return True
        else:
            if word.islower():  # 大文字だが 1 文字目のとき
                return False
            if word.isupper():  # 単語すべてが大文字のとき
                return True
        return False

    # 1 行から単語を抽出し単語の辞書に格納

    def __make_word(self, spaceSeparated_word_list):
        word = ""
        for spaceSeparated_word in spaceSeparated_word_list:
            if spaceSeparated_word in self.RESERVED_WORD_C:  # 予約語は含めない (前後空白のときのみ有効)
                continue
            else:
                print(spaceSeparated_word)
                for c in spaceSeparated_word:
                    if c.isalpha():
                        if self.__should_add_alphabet_to_word(c, word): # 単語が未完成
                            word += c
                        else:  # 単語が完成した (キャメルケース等アルファベットが連続している場合)
                            self.dictionary_set.add(word)
                            word = ""
                            word += c
                    else:  # 単語が完成した (スネークケース等)
                        self.dictionary_set.add(word)
                        word = ""

    # 単語の辞書を作る
    def __make_word_dictionary(self, line_list):
        for line in line_list:
            spaceSeparated_word_list = line.split(" ")
            self.__make_word(spaceSeparated_word_list)

    # 単語の辞書に後処理を行う
    def __final_process(self):
        self.dictionary_set = self.__delete_short_word(self.dictionary_set)
        self.dictionary_set = self.__make_lower_in_dictionary_set(
            self.dictionary_set)

    # メインの処理
    def word_extract(self):
        for file in self.FILE_LIST:
            f = open(file)
            line_list = f.readlines()
            self.__make_word_dictionary(line_list)
            f.close()

        self.__final_process()
        return self.dictionary_set


if __name__ == "__main__":
    word_extractor = WordExtractor()
    print(word_extractor.word_extract())
