from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    source_dir = os.path.dirname(__file__) #<-- directory name
    full_path = os.path.join(source_dir, filename)
    li = []
    with open(full_path,'r', encoding='utf-8') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        anchor1 = soup.find_all('tr')
        for x in anchor1:
            anchor2 = x.find('a', class_ = 'bookTitle')
            anchor3 = x.find('a', class_ = 'authorName')
            title = anchor2.text
            title = title.strip()
            author = anchor3.text
            author = author.strip()
            x = (title, author)
            li.append(x)
        #print(li)
        return li

def get_search_links(soup):
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:
    
    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    l2 = []
    anchor1 = soup.find_all('tr')
    for x in anchor1:
        anchor2 = x.find('a', class_ = 'bookTitle')
        anchor3 = anchor2['href']
        url = "https://www.goodreads.com" + anchor3
        if len(l2) < 10:
            l2.append(url)
    return l2

def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    a1 = soup.find('div', id = 'metacol', class_ = 'last col')
    a2 = a1.find('h1', id = "bookTitle")
    a3 = a1.find('span', itemprop = "name")
    a4 = a1.find('span', itemprop = "numberOfPages")

    title = a2.text
    title = title.strip()

    author = a3.text
    author = author.strip()

    pages = (a4.text)
    pages = pages.strip(" pages")
    pages = int(pages)

    tup = (title, author, pages)
    
    return tup

def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    
    source_dir = os.path.dirname(__file__) #<-- directory name
    full_path = os.path.join(source_dir, filepath)
    l1 = []
    with open(full_path,'r', encoding='utf-8') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        a1 = soup.find_all('div', class_ = "clearFix")
        for x in a1:
            a2 = x.find('a')
            link = x.find('a')['href']
            link = link.strip()

            a3 = a2.find('h4')
            category = a3.text
            category = category.strip()

            title = a2.find('img')['alt']
            title = title.strip()

            tup = (category, title, link)
            l1.append(tup)
        return(l1[1:])



def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    fields = ['Book Title', 'Author Name']
    with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
    # writing the fields 
        csvwriter.writerow(fields) 
    # writing the data rows
        csvwriter.writerows(data)
    


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

def main():
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    #get_titles_from_search_results("search_results.htm")
    #get_search_links(soup)
    get_book_summary("https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1")
    #summarize_best_books("best_books_2020.htm")


class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    search_urls = get_search_links(soup)


    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        var = get_titles_from_search_results("search_results.htm")
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(var), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(var), list)
        # check that each item in the list is a tuple
        for x in var:
            self.assertEqual(type(x), tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(var[0], ("Harry Potter and the Deathly Hallows (Harry Potter, #7)", 'J.K. Rowling'))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(var[-1], ("Harry Potter: The Prequel (Harry Potter, #0.5)", 'J.K. Rowling'))

        

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls), list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)

        # check that each URL in the TestCases.search_urls is a string
        for x in TestCases.search_urls:
            self.assertEqual(type(x), str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for x in TestCases.search_urls:
            self.assertEqual(x[:36], "https://www.goodreads.com/book/show/")

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        summaries = []
        for z in TestCases.search_urls:
            tup = get_book_summary(z)
            summaries.append(tup)
        
        # for each URL in TestCases.search_urls (should be a list of tuples)
        
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
            # check that each item in the list is a tuple
        for x in summaries:
            self.assertEqual(type(x), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(x), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(x[0]), str)
            self.assertEqual(type(x[1]), str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(x[2]), int)
            # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)



    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        var = summarize_best_books("best_books_2020.htm")        
        # check that we have the right number of best books (20)
        self.assertEqual(len(var), 20)
        # assert each item in the list of best books is a tuple
        for x in var:
            self.assertEqual(type(x), tuple)
            self.assertEqual(len(x), 3)

        # check that each tuple has a length of 3

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(var[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual((var[-1]), ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020')) 

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        x = get_titles_from_search_results('search_results.htm')
        # call write csv on the variable you saved and 'test.csv'
        write_csv(x, 'test.csv')        

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv', 'r') as f:
            csvFile = csv.reader(f)
            data_list = list(csvFile)
            
            
            self.assertEqual(len(data_list), 21)
            self.assertEqual(data_list[0], ['Book Title', 'Author Name'])
            self.assertEqual(data_list[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])
            self.assertEqual(data_list[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'])
            
        
        # check that there are 21 lines in the csv

        # check that the header row is correct

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        


if __name__ == '__main__':
    main()
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



