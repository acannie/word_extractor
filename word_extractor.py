import glob
import keyword
import os


class WordExtractor:
    # 単語一覧
    word_dictionary_set = set()
    # 単語情報一覧
    word_dictionary_information = {}

    # 予約語一覧
    RESERVED_WORD_C = ["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum", "extern", "float", "for", "goto", "if",
                       "int", "long", "register", "return", "signed", "sizeof", "short", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while", "define", "include", "main"]
    RESERVED_WORD_CPP = RESERVED_WORD_C + ["asm", "catch", "class", "delete", "friend", "inline",
                                           "new", "operator", "overload", "private", "protected", "public", "template", "this", "throw", "try", "virtual"]
    RESERVED_WORD_PYTHON = keyword.kwlist

    # 言語に対応する予約語
    CORRESPONDED_LANGUAGE = {
        "c": RESERVED_WORD_C, "c++": RESERVED_WORD_CPP, "python": RESERVED_WORD_PYTHON}

    # constructor
    def __init__(self, src="sample.c", language="c"):
        self.__set_language(language=language.lower())
        self.FILE_NAME = src  # 単語を抽出するファイル

    # 言語を設定

    def __set_language(self, language="c"):
        if WordExtractor.CORRESPONDED_LANGUAGE[language] == None:
            print("please check language name.")
            self.RESERVED_WORD = WordExtractor.RESERVED_WORD_C  # デフォルトで C
            return
        self.RESERVED_WORD = WordExtractor.CORRESPONDED_LANGUAGE[language]

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

    # 1 ブロックから単語を抽出し単語一覧・単語情報一覧に登録
    def __make_word(self, spaceSeparated_word="", file_name="", line_number=0):
        if spaceSeparated_word in self.RESERVED_WORD:  # 予約語は含めない (前後空白のときのみ有効)
            return
        word = ""
        for c in spaceSeparated_word:
            if c.isalpha():
                # 単語が完成した (文字を次の単語に含める。キャメルケース)
                if self.__is_new_word(c=c, word=word):
                    self.__register_in_word_dictionary(
                        file_name=file_name, word=word, line_number=line_number)
                    word = ""
                word += c
            else:  # 単語が完成した (文字を次の単語に含めない。スネークケース)
                self.__register_in_word_dictionary(
                    file_name=file_name, word=word, line_number=line_number)
                word = ""
        # spaceSeparated_word を走査し終えた時点で word の中身があれば単語一覧・単語情報一覧に加える
        self.__register_in_word_dictionary(
            file_name=file_name, word=word, line_number=line_number)

    # 余計な記号を半角スペースに置き換える
    def __delete_unusable_symbols(self, line="", usable_symbols=["_"]):
        new_line = line
        for i in range(len(line)):
            if (not line[i].isalpha()) and (not line[i] in usable_symbols):  # 命名に使えない記号
                new_line = new_line[:i] + ' ' + new_line[i+1:]
        return new_line

    # 単語一覧・単語情報一覧を作る
    def __make_word_dictionary(self, line_list=[""], file_name=""):
        for i, line in enumerate(line_list):
            line = self.__delete_unusable_symbols(
                line=line, usable_symbols=["_"])
            spaceSeparated_word_list = line.split(" ")
            spaceSeparated_word_list.remove("")
            for spaceSeparated_word in spaceSeparated_word_list:
                self.__make_word(
                    spaceSeparated_word=spaceSeparated_word, file_name=file_name, line_number=i)

    # 単語一覧、単語情報一覧を作る
    def __register_in_word_dictionary(self, file_name="", word="", line_number=0):
        word = word.lower()
        if len(word) < 2:
            return
        # 単語一覧に登録
        WordExtractor.word_dictionary_set.add(word)
        # 単語情報一覧に登録
        information = {"file_name": file_name,
                       "word": word, "line_number": line_number+1}
        if not word in WordExtractor.word_dictionary_information:  # 重複を避ける。初めて登場したときのみ登録
            WordExtractor.word_dictionary_information[word] = information

    # メインの処理
    def create_word_dictionary(self):
        f = open(self.FILE_NAME)
        line_list = f.readlines()
        self.__make_word_dictionary(
            line_list=line_list, file_name=self.FILE_NAME)
        f.close()

    # 単語一覧を返す

    def get_word_dictionary(self):
        self.create_word_dictionary()
        return list(WordExtractor.word_dictionary_set)

    # 単語情報一覧を返す
    def get_word_dictionary_information(self):
        self.create_word_dictionary()
        return WordExtractor.word_dictionary_information


class WordExtractorFromFolder(WordExtractor):
    # constructor
    def __init__(self, src_folder="./src/", language="c"):
        super().__init__(language)
        self.FILE_LIST = glob.glob(src_folder + "*")  # 単語を抽出するファイルの一覧

    # メインの処理
    def create_word_dictionary_from_folder(self):
        for file_path in self.FILE_LIST:
            self.FILE_NAME = file_path
            self.create_word_dictionary()

    # 単語一覧を返す
    def get_word_dictionary(self):
        self.create_word_dictionary_from_folder()
        return list(WordExtractor.word_dictionary_set)

    # 単語情報一覧を返す
    def get_word_dictionary_information(self):
        self.create_word_dictionary_from_folder()
        return WordExtractor.word_dictionary_information


if __name__ == "__main__":
    # choose language from: c, c++, python
    word_extractor = WordExtractor(src="sample.c", language="c")
    print(word_extractor.get_word_dictionary())

    word_extractor_from_folder = WordExtractorFromFolder(
        src_folder="./src/", language="c")
    print(word_extractor_from_folder.get_word_dictionary())
