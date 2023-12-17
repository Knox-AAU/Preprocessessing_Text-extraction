"""module resposible for testing edgecases for tesseract"""
import os
import pytesseract
from pdf2image import convert_from_path

def test_edge_cases():
    """Method testing proficiency in extraction of different characters"""
    text =""
    passed_chars = []
    declined_chars = []
    temp_path = "src/text_extraction/test/pdf_page_"
    ground_truth_path = "src/text_extraction/test/ground_truth.txt"
    #convert pdf to images and then perform ocr on those images
    pdf_images = convert_from_path('src/text_extraction/test/Testing_document.pdf')
    for image in enumerate(pdf_images):
        image[1].save(temp_path + f"{image[0]+1}.png", 'PNG')
        text = text + (pytesseract.image_to_string(temp_path + f"{image[0]+1}.png",lang="dan"))
        os.remove(f"src/text_extraction/test/pdf_page_{image[0]+1}.png")

    #separate words/characters from ground_truth into list
    with open(ground_truth_path, 'r', encoding="utf-8") as ground_truth:
        raw_text = ground_truth.read()
        ground_truth = ground_truth.read().split()

    #if length of text is more than 0 text was succesfully extracted
    ground_truth_len = len(ground_truth)
    #iterate all elements in ground_truth and check if that substring is in the extracted text
    #then append found elements to passed_chars and the ones that weren't to declined_chars
    for char in range(ground_truth_len):
        match = text.find(ground_truth[char])
        if match > -1:
            passed_chars.append(ground_truth[char])
        else:
            declined_chars.append(ground_truth[char])

    print("passed input: ", passed_chars, "\n")
    print("declined input: ", declined_chars, "\n")
    print("passed:", len(passed_chars), "|" + "declined:", len(declined_chars), "\n")
    print("the expected text: \n" + "------------------\n", raw_text, "\n")
    print("the extracted text: \n" + "-------------------\n" + text)

if __name__ == "__main__":
    test_edge_cases()
        