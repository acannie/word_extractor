import glob
import keyword


class WordExtractor:
    # 単語の辞書 (最終的に返す)
    dictionary_set = set()

    # 予約語一覧
    RESERVED_WORD_C = ["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum", "extern", "float", "for", "goto", "if",
                       "int", "long", "register", "return", "signed", "sizeof", "short", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while", "define", "include", "main"]
    RESERVED_WORD_CPP = RESERVED_WORD_C + ["asm", "catch", "class", "delete", "friend", "inline",
                                           "new", "operator", "overload", "private", "protected", "public", "template", "this", "throw", "try", "virtual"]
    RESERVED_WORD_PYTHON = keyword.kwlist

    # 予約語対応言語一覧
    CORRESPONDED_LANGUAGE = {
        "c": RESERVED_WORD_C, "c++": RESERVED_WORD_CPP, "python": RESERVED_WORD_PYTHON}

    # constructor
    def __init__(self, src_folder="./src/", language="c"):
        self.__set_language(language=language.lower())
        self.FILE_LIST = glob.glob(src_folder + "*")  # 単語を抽出するファイルの一覧

    # 言語を設定

    def __set_language(self, language="c"):
        if WordExtractor.CORRESPONDED_LANGUAGE[language] == None:
            print("please check language name.")
            self.RESERVED_WORD = WordExtractor.RESERVED_WORD_C  # デフォルトで C
            return
        self.RESERVED_WORD = WordExtractor.CORRESPONDED_LANGUAGE[language]

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

    # 与えられた文字は新しい単語の1文字目か判定

    def __is_new_word(self, c="", word=""):
        if c.islower():  # 小文字のとき
            if word.isupper() and len(word) > 1:  # 単語すべてが大文字かつ 2 文字以上のとき
                return True
            return False
        else:
            if word.islower():  # 大文字だが 1 文字目のとき
                return True
            if word.isupper():  # 単語すべてが大文字のとき
                return False
        return True

    # 1 ブロックから単語を抽出し単語の辞書に格納
    def __make_word(self, spaceSeparated_word=""):
        if spaceSeparated_word in self.RESERVED_WORD:  # 予約語は含めない (前後空白のときのみ有効)
            return
        word = ""
        for c in spaceSeparated_word:
            if c.isalpha():
                # 単語が完成した (文字を次の単語に含める。キャメルケース)
                if self.__is_new_word(c=c, word=word):
                    WordExtractor.dictionary_set.add(word)
                    word = ""
                word += c
            else:  # 単語が完成した (文字を次の単語に含めない。スネークケース)
                WordExtractor.dictionary_set.add(word)
                word = ""
        # spaceSeparated_word を走査し終えた時点で word の中身があれば単語の辞書に加える
        WordExtractor.dictionary_set.add(word)

    # 余計な記号を半角スペースに置き換える
    def __delete_unusable_symbols(self, line="", usable_symbols=["_"]):
        new_line = line
        for i in range(len(line)):
            if (not line[i].isalpha()) and (not line[i] in usable_symbols):  # 命名に使えない記号
                new_line = new_line[:i] + ' ' + new_line[i+1:]
        return new_line

    # 単語の辞書を作る
    def __make_word_dictionary(self, line_list=[""]):
        for line in line_list:
            line = self.__delete_unusable_symbols(
                line=line, usable_symbols=["_"])
            spaceSeparated_word_list = line.split(" ")
            spaceSeparated_word_list.remove("")
            for spaceSeparated_word in spaceSeparated_word_list:
                self.__make_word(spaceSeparated_word)

    # 単語の辞書に後処理を行う
    def __final_process(self):
        WordExtractor.dictionary_set = self.__delete_short_word(
            dictionary_set=WordExtractor.dictionary_set)
        WordExtractor.dictionary_set = self.__make_lower_in_dictionary_set(
            dictionary_set=WordExtractor.dictionary_set)
        WordExtractor.dictionary_set = sorted(WordExtractor.dictionary_set)

    # メインの処理
    def word_extract(self):
        for file in self.FILE_LIST:
            f = open(file)
            line_list = f.readlines()
            self.__make_word_dictionary(line_list=line_list)
            f.close()

        self.__final_process()
        return WordExtractor.dictionary_set


if __name__ == "__main__":
    # choose from: c, c++, python
    word_extractor = WordExtractor(src_folder="./src/", language="c")
    print(word_extractor.word_extract())
