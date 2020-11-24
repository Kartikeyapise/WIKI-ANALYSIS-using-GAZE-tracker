# Need to run the file as root for Keyboard Listener on Mac OSX
import new_script
import time
import shutil
import window_dimensions1
import textstat
# import datetime
# import sys
# import mss
import pytesseract
# from pynput.mouse import Listener
# from pynput.keyboard import Listener, Key
import numpy as np
# import re
import hashlib
import cv2
import os
from PIL import Image
# from reorderf import reorderFlow
import re
# from bs4 import BeautifulSoup
from difflib import get_close_matches
import wikipediaapi


class Screen(object):
    frames = {}
    scroll_value = False
    new_frame = True
    # portions = []
    summary = []
    dimensions = []
    start_time = 0
    # print('Window Dimensions', dimensions)
    # browser_width = 768*2
    mw_panel = 0
    monitor = {}
    pixel_info = 0
    factor = 40
    n = 0
    data = {}  # text: frameName, coordinates, scroll
    dynamic_check = False
    extracted_data = []

    def extract_Text_From_Image(self, image):
        text = pytesseract.image_to_string(image, lang='eng')
        return text

    def get_Coordinates(self, frameName):
        bboxes = []
        bboxFile = open("./File_out/bbox_points.txt", "r")
        for line in bboxFile:
            line_parts = line.split(" | ")
            if line_parts[0].__contains__(frameName):
                for i in range(1, len(line_parts) - 1):
                    coords = line_parts[i].split(" ")[0:-1]
                    coords = list(map(int, coords))
                    coords = [coords[0], coords[1], coords[0] + coords[2], coords[1] + coords[3]]
                    bboxes.append(coords)
        return bboxes

    def complete_The_Text(self, extracted_text, window, read_box):
        test_portion = read_box[:]
        test_portion[2] += 20
        if test_portion[0] >= 0:
            test_portion[0] -= 20
        x = self.extract_Text_From_Image(window.crop(test_portion))
        if len(extracted_text) == len(x):
            print('Did not find any extra text.')
            return extracted_text, read_box
        else:
            last_word = '.'
            read_box[0] = 0
            read_box[2] = window.width
            full_text = self.extract_Text_From_Image(window.crop(read_box))
            first_word_in_full_text = full_text.split(' ', 1)[0]
            try:
                if first_word_in_full_text.islower():
                    first_position = full_text.index('.') + 1
                else:
                    first_position = 0
            except ValueError:
                # print('why tho')
                first_position = 0
            try:
                last_position = full_text.rindex(last_word)
            except ValueError:
                last_position = len(full_text) + 1
            complete_text = full_text[first_position:last_position]
            return complete_text, read_box

    def text_Extraction(self, window_name, boxes):
        # start = time.time()
        window = Image.open(window_name)
        data = []
        for i in range(len(boxes)):
            read_box = boxes[i]
            # read_box = [604, 247, 90, 124]
            extracted_image = window.crop(read_box)
            # extracted_image.show()
            extracted_text = self.extract_Text_From_Image(extracted_image)
            extracted_text = re.sub("\n", ". ", extracted_text)
            # self.extracted_data.append(extracted_text)
            #####
            if read_box[2] - read_box[0] >= 2500:
                # extract.write(extracted_text+'\n\n')
                # print('\n' + extracted_text + '\n \n' + str(read_box))
                self.extracted_data.append(extracted_text)
                # sc.extracted_data = '\n'.join(sc.extracted_data)  # data.append(extracted_text)
                # = (window_name, read_box, self.pixel_info)
            elif extracted_text:
                self.extracted_data.append(extracted_text)
                ######corrected_text, b_box = self.complete_The_Text(extracted_text, window, read_box)
                ######self.extracted_data.append(corrected_text)
            # sc.extracted_data = '\n'.join(sc.extracted_data)  # data.append(extracted_text)
            # data[corrected_text] = (window_name, b_box, self.pixel_info)
            # extract.write(corrected_text+'\n\n')
            # print('\n' + extracted_text + '\n \n' + str(b_box))

        # time_elapsed = time.time() - start
        # print('Time taken:', time_elapsed)
        # summaryFinal = open("./File_out/summary.txt", "a+")
        # summaryFinal.write("\nSelf Extracted Text: "+self.extracted_data[len(self.extracted_data)-1]+ "\n")
        # summaryFinal.close()
        # print("\nSelf Extracted Text: ",end="\n")
        # for data in self.extracted_data:
        #     print ("Line: "+data, end="\n")
        # return data

    def remove_Redundant_Text(self, input_text):
        list_of_sentences = input_text.split('\n')
        completed_lines_hash = set()
        redundancy_free_text = ''

        for line in list_of_sentences:
            words = line.split(" ")
            if len(words) < 5:
                continue
            hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
            if hashValue not in completed_lines_hash:
                redundancy_free_text += line
                completed_lines_hash.add(hashValue)
        return redundancy_free_text

    def split_sentences(self, text):
        corrected_text = re.sub(r"\.(?=\S)", ". ", text)
        corrected_text = re.sub(".\n", ". ", corrected_text)
        st = corrected_text.strip() + '. '
        sentences = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', st)
        return sentences

    def clean_Extracted_Text(self, summary_unclean):

        # remove non-ascii characters
        non_ascii_removed = re.sub(r'[^\x00-\x7F]+', ' ', summary_unclean)

        # replace deciamal with underscore
        # decmark_reg = re.compile('(?<=\d)\.(?=\d)')
        # decimal_replaced = decmark_reg.sub('__', non_ascii_removed)

        # remove unwanted wild characters
        bad_chars = ['!', '*', '`', "'", '"', '[', ']', '(', ')', "?", "=", "~"]
        for i in bad_chars:
            wild_removed = ''.join(i for i in non_ascii_removed if i not in bad_chars)
        wild_removed = re.sub('[!{[|]\S+[!\}\]lI1]?|\d+[\]lJ]+', '', wild_removed)
        wild_removed = re.sub(' +', ' ', wild_removed)
        wild_removed = re.sub('@', '', wild_removed)
        wild_removed = re.sub('\n+', '\n', wild_removed)

        # single letters removed
        singles_removed = ' '.join([w for w in wild_removed.split() if (len(w) > 1 and w not in ['a'])])

        # contraction_done = ' '.join(
        #     [contraction_mapping[t] if t in contraction_mapping else t for t in singles_removed.split(" ")])
        # #capitalize first character of sentence
        # clean_summary = '. '.join(map(lambda s: s.strip().capitalize(), contraction_done.split('.')))

        return singles_removed


def crMain():
    print("Start summary creation...")

    sc = Screen()
    frame_list = os.listdir("./Image_out/Frames")

    def frame_no(x):
        return x.split("_")[1]

    articleName = None
    articleName1= None
    unclean_summary = []
    for filename in sorted(frame_list, key=frame_no):
        if filename.endswith(".png"):
            if filename.__contains__("dummy"):
                continue
            articleName = filename.split("_")[0]
            st_time=filename.split("_")[2].split(".")[0].split(":")
            articleName1= (str)(articleName)+"_"+str(st_time[0])+"_"+(str)(st_time[1])+"_"+(str)(st_time[2])
            net = "./Image_out/Frames/" + filename
            frame = cv2.imread("./Image_out/Frames/" + filename)
            portions = sc.get_Coordinates(filename)
            sc.text_Extraction(net, portions)
        else:
            continue

    print("Data extracted...")
    # Remove redundancy
    sc.extracted_data = '\n'.join(sc.extracted_data)
    primary_clean_data = sc.clean_Extracted_Text(sc.extracted_data)
    redundancy_free_summary = sc.remove_Redundant_Text(primary_clean_data)
    unclean_summary = redundancy_free_summary
    # summaryFinal = open("./File_out/summary.txt", "w")
    # summaryFinal.write("Cleaned Summary: "+unclean_summary+ "\n")
    # summaryFinal.close()
    

    




    
    # Get original article plain text
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        # extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    #Ext
    p_wiki = wiki_wiki.page(articleName)
    original_text = p_wiki.text

    
    

    ogtext = open("./File_out/ogtext.txt", "w")
    ogtext.write("Original Text:\n"+ original_text+"\n")
    ogtext.close()
    print("Data API collected...")




    
    


    # Replace decimal by '__'
    decmark_reg = re.compile('(?<=\d)\.(?=\d)')
    decimal_replaced = decmark_reg.sub('__', original_text)
    text_list = decimal_replaced.split(".")
    original_list = sc.split_sentences(original_text)
    index = 0
    org_list = []
    for each in original_list:
        org_list.append(str(index) + " @:@ " + each)
        index += 1

    # Get close matches of summary sentences in original text
    from fuzzywuzzy import process
    final_matches = []
    matches = []
    for each in unclean_summary.split('.'):
        each = each.strip()
        each_list = each.split(" ")
        if len(each_list) > 1:
            # extract = process.extract(each, org_list)
            # text_column = np.array(extract)
            # match1 = text_column[:, 0]
            # if len(match1) != 0:
            #     best_match = match1[0].split(" @:@ ")
            #     final_matches.append([int(best_match[0]), best_match[1]])
            match2 = get_close_matches(each, org_list, cutoff=0.4)
            if len(match2) != 0:
                best_match = match2[0].split(" @:@ ")
                final_matches.append([int(best_match[0]), best_match[1]])

    # Sort the original text sentences according to index and create summary
    summaryFinal = open("./File_out/summary.txt", "w")
    sorted_list = sorted(final_matches, key=lambda l: l[0])
    print("Sorted List: "+ str(sorted_list),end="\n")
    text_column = np.array(sorted_list)
    print(np.shape(text_column))
    unique_matches = list(dict.fromkeys(text_column[:, 1]))
    summary=""
    for each in unique_matches:
        text = str(each)
        summary = summary + text.strip() + " "
        summaryFinal.write(text.strip() + " ")

    summaryFinal.close()

    print("Summary saved at File_out/summary.txt")

    config = open("./summary_created.txt", "w")
    config.write("1")
    config.close()
    ''' Section break '''

    #Compute Reading Scores
    val1=textstat.flesch_reading_ease(original_text)
    val2=textstat.flesch_reading_ease(summary)
    ratio= val2/val1
    #Writing Length  and Reading Scores to info file
    words=summary.split()
    count=len(words)
    print("Length of read text= "+(str) (count))

    info = open("./File_out/Info.txt", "w")
    info.write("No.of words read: "+ (str)(count)+ "\n")
    info.write("Ratio Score: "+ (str)(ratio)+"\n")
    info.write("Summary Score: "+ (str)(val2)+"\n")
    info.write("Article Score: "+ (str)(val1)+"\n")
    info.close()


    #code to copy all contents from one directory to other 
    print(articleName1)
    cwd = os.getcwd()
    articleName_csv=articleName1.replace(",", "_")
    new_script.open_images(articleName_csv, count, ratio)

    # Storing File_Out
    path = os.path.join(cwd, "samples") 
    path = os.path.join(path, articleName1)
    path = os.path.join(path, "File_out") 
    dst=path
    src=os.path.join(cwd, "File_out")
    shutil.copytree(src, dst)

    #Storing Image_Out
    path = os.path.join(cwd, "samples") 
    path = os.path.join(path, articleName1)
    path = os.path.join(path, "Image_out") 
    dst=path
    src=os.path.join(cwd, "Image_out")
    shutil.copytree(src, dst)

  

if __name__ == "__main__":
    crMain()
