This is a scrapy-based web crawler with a tkinter GUI.

You enter the website name, the keyword, the number of pages to search, and whether you want Depth-First or Breadth-First Search.

Then it will crawl the website of choice for the word, search links from that site if it can't find it, search those links for the word, and so on with a turtle-based visualizer that uses colors based on the links searched, number of pages searched, and the time of day.

Once the maximum number of pages are reached or the keyword is found, the program will let you know if the word as found or not in a results button.

If the keyword was found, the results window will pull up the link the keyword was found, as well as the sentence where it was found.

This was created on a Windows 10 system with Python 2.7x.

The only external library (that I know of) that this program requires is scrapy. So `pip install scrapy` at the terminal before running `gui.py` from the **tkinterScrapy** directory
