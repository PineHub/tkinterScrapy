from Tkinter import *
from subprocess import call
import csv
import os
import tkMessageBox


class MyFirstGUI:
    LABEL_TEXT = [  # scrollable text
        "Welcome to my crawl-visualizer! This label is clickable.",
        "Complete the four entries below.",
        "When done, click Go!",
        "The visualizer creates color combinations that depend on the length of the link, pages crawled, and time of day."
        "Then click the Results button."
        "Go on, click this label again.",
    ]

    def __init__(self, master):
        self.master = master
        master.title("Keyword Web Crawler by Clarence Pine")


        # main label giving instructions at top of text box
        self.label_index = 0
        self.label_text = StringVar()
        self.label_text.set(self.LABEL_TEXT[self.label_index])
        self.label = Label(master, textvariable=self.label_text)
        self.label.bind("<Button-1>", self.cycle_label_text)
        self.label.pack()
        self.label.config(font=("Calibri", 25))

        # url entry box
        self.url_input = StringVar()  #value of url
        self.url_entry = Entry(master, textvariable=self.url_input, width=30)
        self.urlEntryText = StringVar()
        self.urlEntryText.set("Enter the website to be searched")
        self.urlLabelEntry = Label(master, textvariable=self.urlEntryText, height=1) #label of the url entry box
        self.urlLabelEntry.config(font=('Arial', 15))
        self.urlLabelEntry.pack(side="top")
        self.url_entry.pack(side="top")
        self.url_entry.insert(0, "http:\\\\") #pre-populate url entry box

        # keyword entry box
        self.keyword_input = StringVar() #value of keyword
        self.keyword_entry = Entry(master, textvariable=self.keyword_input, width=30)
        self.keywordEntryText = StringVar()
        self.keywordEntryText.set("Enter the keyword to be searched for")
        self.keyLabelEntry = Label(master, textvariable=self.keywordEntryText, height=1) #label of keyword entry box
        self.keyLabelEntry.config(font=('Arial', 15))
        self.keyLabelEntry.pack(side="top")
        self.keyword_entry.pack(side="top")

        #maximum number of pages to search
        self.maxpage_input = StringVar() #value of max pages to be searched
        self.maxpage_entry = Entry(master, textvariable=self.maxpage_input, width=30)
        self.pageEntryText = StringVar()
        self.pageEntryText.set("Enter the max number of pages to be searched")
        self.pageLabelEntry = Label(master, textvariable=self.pageEntryText, height=1) #label of max page box
        self.pageLabelEntry.config(font=('Arial', 15))
        self.pageLabelEntry.pack(side="top")
        self.maxpage_entry.pack(side="top")

        # dropdown menu to choose depth-first or breadth-first search
        self.searchChoice = StringVar() #value of breadth vs depth first search
        self.dropSearch = OptionMenu(master, self.searchChoice, 'Breadth-First Search', 'Depth-First Search')
        self.searchText = StringVar()
        self.searchText.set("Search Style")
        self.searchLabelEntry = Label(master, textvariable=self.searchText, height=1) #label of breadth first or depth first search
        self.searchLabelEntry.config(font=('Arial', 15))
        self.searchLabelEntry.pack(side="top")
        self.dropSearch.pack(side="top")

        # Go! button
        self.crawl_button = Button(master, text="Go!", command=self.crawl)
        self.crawl_button.pack()

        # Close button
        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()



    def crawl(self):

        urlString = self.url_input.get()
        newUrlString = urlString[7:]            # remove http://// from the url string
        newUrlString = 'http://' + newUrlString  # add http:// to the url string

        keywordString = self.keyword_input.get()

        maxPageString = self.maxpage_input.get()

        searchTypeString = self.searchChoice.get()

        try:
            os.remove("tempout.csv")  # remove this file if it exists
        except OSError:
            pass

        #two different types of arguments: breadth and depth-first search:
        #outputting to a readable csv file
        bSearchArgument = "scrapy crawl keyword_search -a start_url=" + newUrlString + " -a find_word=" + keywordString + " -s " + "CLOSESPIDER_PAGECOUNT=" + maxPageString + " -o tempout.CSV -t csv"
        dSearchArgument = "scrapy crawl keyword_search -a start_url=" + newUrlString + " -a find_word=" + keywordString + " -s " + "CLOSESPIDER_PAGECOUNT=" + maxPageString + " -s DEPTH_PRIORITY=1 -s SCHEDULER_DISK_QUEUE=scrapy.squeues.PickleFifoDiskQueue -s SCHEDULER_MEMORY_QUEUE=scrapy.squeues.FifoMemoryQueue -o tempout.CSV -t csv"

        if searchTypeString == "Depth-First Search":
            call(dSearchArgument)
        else:
            call(bSearchArgument)


        try:
            self.resultButton.destroy()  #remove this button if it exists
        except AttributeError:
            pass

        self.resultButton = Button(root, text="Results", command=self.results_window)
        self.resultButton.pack()







    def cycle_label_text(self, event):
        self.label_index += 1
        self.label_index %= len(self.LABEL_TEXT)  # wrap around
        self.label_text.set(self.LABEL_TEXT[self.label_index])

    def results_window(self):

        master = self.master
        keyWordNotFound = True


        with open('tempout.csv') as csvfile:        # reading the csv file
            reader = csv.DictReader(csvfile)
            resultStarter = "We found your keyword at: "
            resultSentenceStarter = "in this line: "
            for row in reader:
                if row['targetNode']:  # if the keyword was found, targetNode would be true
                    targetLink = row['urlDict']
                    targetSentence = row['targetNode'].decode('unicode_escape')  # unicode \u removal
                    keyWordNotFound = False
                    targetLink = targetLink[17:-2]
                    print "targetLink length: ", len(targetLink)
                    if len(targetLink) > 85:        # if the length of the link is too long, shorten it to 85 characters with ellipse
                        newLength = (len(targetLink) - 85) * -1
                        print "newLength: ", newLength
                        targetLink = targetLink[:newLength] + "..."
                        print "new targetLink length: ", len(targetLink), "link is: ", targetLink
                    targetSentence = targetSentence[7:-3]
                    if len(targetSentence) > 250:     # shorten length of sentece keyword is found with ellipse
                        newLengthSentence = (len(targetSentence) - 250) * -1
                        targetSentence = targetSentence[:newLengthSentence] + "..."




            if not keyWordNotFound:
                resultLinkStarter = resultStarter + targetLink + "\n" + resultSentenceStarter + targetSentence  # message advising of link, sentence with keyword.
                tkMessageBox.showinfo("Results", resultLinkStarter)

            else:
                tkMessageBox.showinfo("Results", "We couldn't find your word")







        # window.result_button = Button(window, text="Done", command=window.destroy)  # done with results button
        # window.result_button.pack()

        try:
            os.remove("tempout.csv")  #remove this file if it exists
        except OSError:
            pass

try:
    os.remove("tempout.csv")  #remove this file if it exists
except OSError:
    pass

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()