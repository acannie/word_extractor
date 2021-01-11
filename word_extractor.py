import glob

def should_add_alphabet_to_word(c="", word=""):
    if c.islower(): # 小文字のとき
        return True
    elif len(word) == 1: # 大文字だが 1 文字目のとき
        return True
    elif word.isupper(): # 単語すべてが大文字のとき
        return True
    return False

def delete_short_word(dictionary_set=set()):
    new_dictionary_set = set(dictionary_set)
    for word in dictionary_set:
        if len(word) < 2:
            new_dictionary_set.remove(word)
    return new_dictionary_set

def make_lower_in_dictionary_set(dictionary_set=set()):
    for word in dictionary_set:
        word = word.lower()
    return dictionary_set


# 単語の辞書
dictionary_set = set()


files = glob.glob("./src/*")
for file in files:
    f = open(file)
    line_list = f.readlines()

    word = ""

    for line in line_list:
        for c in line:
            if c.isalpha():
                if should_add_alphabet_to_word(c, word):
                    word += c
                else:
                    dictionary_set.add(word)
                    word = ""
                    word += c
            else:
                dictionary_set.add(word)
                word = ""

    f.close()
    
dictionary_set = delete_short_word(dictionary_set)
dictionary_set = make_lower_in_dictionary_set(dictionary_set)
print(dictionary_set)