from Tkinter import *
from hello_world import *
from subprocess import call


class MyFirstGUI:
    LABEL_TEXT = [
        "Welcome to my crawl-visualizer! This label is clickable.",
        "Complete the four entries below.",
        "When done, click Go!",
        "Go on, click this label again.",
    ]

    def __init__(self, master):
        self.master = master
        master.title("Keyword Web Crawler by Clarence Pine")

        #main label giving instructions at top of text box
        self.label_index = 0
        self.label_text = StringVar()
        self.label_text.set(self.LABEL_TEXT[self.label_index])
        self.label = Label(master, textvariable=self.label_text)
        self.label.bind("<Button-1>", self.cycle_label_text)
        self.label.pack()
        self.label.config(font=("Calibri", 25))

        #url entry box
        self.url_input = StringVar()  #value of url
        self.url_entry = Entry(master, textvariable=self.url_input, width=30)
        self.urlEntryText = StringVar()
        self.urlEntryText.set("Enter the website to be searched")
        self.urlLabelEntry = Label(master, textvariable=self.urlEntryText, height=1) #label of the url entry box
        self.urlLabelEntry.config(font=('Arial', 15))
        self.urlLabelEntry.pack(side="top")
        self.url_entry.pack(side="top")
        self.url_entry.insert(0, "http:\\\\")

        #keyword entry box
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

        #dropdown menu to choose depth-first or breadth-first search
        self.searchChoice = StringVar() #value of breadth vs depth first search
        self.dropSearch = OptionMenu(master, self.searchChoice, 'Breadth-First Search', 'Depth-First Search')
        self.searchText = StringVar()
        self.searchText.set("Search Style")
        self.searchLabelEntry = Label(master, textvariable=self.searchText, height=1) #label of breadth first or depth first search
        self.searchLabelEntry.config(font=('Arial', 15))
        self.searchLabelEntry.pack(side="top")
        self.dropSearch.pack(side="top")


        self.crawl_button = Button(master, text="Go!", command=self.crawl)  #Go! button
        self.crawl_button.pack()



        self.close_button = Button(master, text="Close", command=master.quit)  #Close button
        self.close_button.pack()



    def crawl(self):

        urlString = self.url_input.get()
        newUrlString = urlString[7:]            #remove http://// from the url string
        newUrlString = 'http://' + newUrlString  #add http:// to the url string

        keywordString = self.keyword_input.get()

        maxPageString = self.maxpage_input.get()

        searchTypeString = self.searchChoice.get()

        #two different types of arguments: breadth and depth-first search:
        bSearchArgument = "scrapy crawl keyword_search -a start_url=" + newUrlString + " -a find_word=" + keywordString + " -s " + "CLOSESPIDER_PAGECOUNT=" + maxPageString
        dSearchArgument = "scrapy crawl keyword_search -a start_url=" + newUrlString + " -a find_word=" + keywordString + " -s " + "CLOSESPIDER_PAGECOUNT=" + maxPageString + " -s DEPTH_PRIORITY=1 -s SCHEDULER_DISK_QUEUE=scrapy.squeues.PickleFifoDiskQueue -s SCHEDULER_MEMORY_QUEUE=scrapy.squeues.FifoMemoryQueue"

        if searchTypeString == "Depth-First Search":
            call(dSearchArgument)
        else:
            call(bSearchArgument)


    def cycle_label_text(self, event):
        self.label_index += 1
        self.label_index %= len(self.LABEL_TEXT)  # wrap around
        self.label_text.set(self.LABEL_TEXT[self.label_index])



root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()