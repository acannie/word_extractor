import openpyxl
import word_extractor


class OutputExtractedWordToExcel (word_extractor.WordExtractor):
    OUTPUT_TEST = [[]]

    def __init__(self, src_folder, language, wb_output="", wb_input=""):
        super().__init__(src_folder, language)
        self.WB_INPUT = openpyxl.open(wb_input)
        self.WS_INPUT = self.WB_INPUT.worksheets[0]
        self.wb_output = openpyxl.open(wb_output)
        self.ws_output = self.wb_output.worksheets[0]
    
    def __write_to_wb(self):
        row = 2
        for word_information in self.get_word_dictionary_information():
            self.ws_output.cell(row=row, column=1).value = ""
            self.ws_output.cell(row=row, column=2).value = word_information["file_name"]
            self.ws_output.cell(row=row, column=3).value = word_information["line_number"]
            self.ws_output.cell(row=row, column=4).value = word_information["name"]
            self.ws_output.cell(row=row, column=5).value = ""
            self.ws_output.cell(row=row, column=6).value = ""
            row += 1
    
    def output_extracted_word_to_excel(self):
        self.__write_to_wb()
    


if __name__ == "__main__":
    output_extracted_word_to_excel = OutputExtractedWordToExcel(src_folder="./src/", language="c", wb_input="input.xlsx", wb_output="output.xlsx")
    output_extracted_word_to_excel.output_extracted_word_to_excel()