# 概要
ソースコード中で使われている英単語を抽出して一覧を作成します。

# 実行

## 単語一覧を表示

```bash
pipenv run python word_extractor.py [file or folder path] [language]
```

コマンドライン引数 | 入力内容
---|---
file or folder path | 検索するファイルまたはフォルダのパス。
language | 検索するソースコードの言語。"c" または "c++" または "python" のみ予約語を含まなくできる。

## 実行例 (run_sample.sh)

```bash
# for file
pipenv run python word_extractor.py sample.c c

# for folder
pipenv run python word_extractor.py sample/ c
```


## 抽出した単語を Excel に出力

```bash
pipenv run python output_to_excel.py [folder path] [language] [reference file path] [output file path]
```

コマンドライン引数 | 入力内容
---|---
folder path | 検索するフォルダのパス。
language | 検索するソースコードの言語。"c" または "c++" または "python" のみ対応。（予約語が含まれなくなる）
reference file path | 参照ファイルのパス。Excel 形式のみ。
output file path | 出力ファイルのパス。Excel 形式のみ。

## 実行例 (run_sample.sh)

```bash
# for file (未対応)
# pipenv run python output_to_excel.py sample.c c refernce.xlsx output.xlsx

# for folder
pipenv run python output_to_excel.py sample/ c reference.xlsx output.xlsx
```
