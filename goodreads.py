#Goodreads.py, by Owen Mellema
import requests
from xml.etree import ElementTree

with open("goodreads_auth.txt") as f:
    key = f.read()

class GoodreadsRequest:
    '''
    Represents a single request to Goodreads.
    '''

    def __init__(self, endpoint, special_endpoint=False):
        global key
        if endpoint is None:
            AssertionError("Unfortunately, there is no endpoint for looking up this data.")

        if special_endpoint:
            url = endpoint
        else:
            url = f"https://www.goodreads.com/{endpoint}?key={key}"

        resp = requests.get(url)
        self.response = ElementTree.fromstring(resp.content)
        self.response = self.response[1] #The first entry is always just unneeded stuff.

        self.success = resp.status_code == 200

class GoodreadsData:
    '''
    Parent class for all objects that store goodreads data.

    This class does things like cacheing results.
    '''
    def __init__(self, incomplete_tree=None):
        '''
        incomplete_tree is an Element Tree containing partial information about the data. Some parents have a partial tree containing some information. This can be cached to save a request.
        '''
        self.request = None #When a request is made, it is stored in memory. This assumes that a piece of data will never update within the lifetime of the program.
        self.cache = {}
        self.special_endpoint = False #When an endpoint requires more sturcture than what is currently present

        # Handle Cacheing
        if incomplete_tree is not None:
            for i in incomplete_tree:
                self.cache[i.tag] = i

    def id(self):
        return self.id

    def _request(self, lookup_value, returnText = True):
        '''
        Returns the desired data.
        lookup_value: A string that holds the data that is wanted.
        returnText: Whether to return an elementTree or a string
        '''
        if lookup_value in self.cache: #First we check if the data is in the incomplete tree cache.
            result = self.cache[lookup_value]
        else: #If not, we look at an actual request
            if self.request is None: #We check if there is a request already present before making a request
                self.request = GoodreadsRequest(self.endpoint, special_endpoint=self.special_endpoint).response
            result = self.request.find(lookup_value)

        if returnText:
            return result.text
        else:
            return result
    
    def parseDataList(self, tree, the_class):
        '''
        Parses an element tree that is comprised of elements that are objects previously created.
        tree: The elementTree to parse.
        the_class: The class to store the data in.
        '''
        return [the_class(i.find("id"), incomplete_tree=i) for i in tree]

class Author(GoodreadsData):
    def __init__(self, id, incomplete_tree=None):
        GoodreadsData.__init__(self, incomplete_tree=incomplete_tree)
        self.id = id
        self.endpoint = f"author/show/{self.id}"    

    def __repr__(self):
        return self.name()

    def name(self):
        return self._request("name")

    def fans(self):
        return self._request("fans_count")

    def about(self):
        return self._request("about")
    
    def influences(self):
        return self._request("influences")
    
    def works_count(self):
        return self._request("works_count")
    
    def gender(self):
        return self._request("gender")
    
    def hometown(self):
        return self._request("hometown")
    
    def born(self):
        return self._request("born_at")
    
    def died(self):
        return self._request("died_at")
    
    def books(self):
        all_books = self._request("books", returnText=False)
        return self.parseDataList(all_books, Book)

class Book(GoodreadsData):
    def __init__(self, id, incomplete_tree=None):
        GoodreadsData.__init__(self, incomplete_tree=incomplete_tree)
        self.id = id
        self.endpoint = f"book/show/{self.id}"  

    def __repr__(self):
        return self.title()

    def title(self):
        return self._request("title")
    
    def isbn(self):
        return self._request("isbn")
    
    def country(self):
        return self._request("country_code")

    def year(self):
        return self._request("publication_year")

    def month(self):
        return self._request("publication_month")
    
    def day(self):
        return self._request("publication_day")
    
    def publisher(self):
        return self._request("publisher")
    
    def language(self):
        return self._request("language_code")
    
    def description(self):
        return self._request("description")
    
    def average_rating(self):
        return self._request("average_rating")
    
    def page_count(self):
        return self._request("num_pages")

    def format(self):
        return self._request("format")
    
    def edition_information(self):
        return self._request("edition_information")
    
    def ratings_count(self):
        return self._request("ratings_count")
    
    def review_count(self):
        return self._request("text_reviews_count")

    def goodreads_url(self):
        return self._request("url")
    
    def authors(self):
        authors = self._request("authors", returnText=False)
        return self.parseDataList(authors, Author)
    
    def popular_shelves(self):
        shelves = self._request("popular_shelves", returnText=False)
        return self.parseDataList(shelves, Shelf)
    
    # def series(self):
    #     #TODO come back to this after implementing series

    def similar_books(self):
        books = self._request("similar_books", returnText=False)
        return self.parseDataList(books, Book)

class Shelf(GoodreadsData):
    def __init__(self, id, incomplete_tree=None):
        GoodreadsData.__init__(self, incomplete_tree=incomplete_tree)
        self.id = id
        self.endpoint = None
    
    def __repr__(self):
        return self.name()

    def name(self):
        return self._request("name")
    
    def book_count(self):
        return self._request("book_count")
    
    def exclusive(self):
        return self._request("exclusive_flag")
    
    def description(self):
        return self._request("description")

class User(GoodreadsData):
    def __init__(self, id, incomplete_tree=None):
        GoodreadsData.__init__(self, incomplete_tree=incomplete_tree)
        self.id = id
        self.endpoint = f"user/show/{id}"
    
    def name(self):
        return self._request("name")
    
    def user_name(self):
        return self._request("user_name")
    
    def about(self):
        return self._request("about")
    
    def age(self):
        return self._request("age")
    
    def gender(self):
        return self._request("gender")
    
    def location(self):
        return self._request("location")
    
    def website(self):
        return self._request("website")
    
    def joined(self):
        return self._request("joined")
    
    def last_active(self):
        return self._request("last_active")
    
    def interests(self):
        return self._request("interests")
    
    def favorite_authors(self):
        authors = self._request("favorite_authors", returnText=False)
        return self.parseDataList(authors, Author)
    
    def favorite_books(self):
        books = self._request("favorite_books", returnText=False)
        return self.parseDataList(books, Book)
    
    def friends_count(self):
        return self._request("friends_count")
    
    def user_shelves(self):
        shelves = self._request("user_shelves", returnText=False)
        return self.parseDataList(shelves, Shelf)
    

def author_data(author):
    print(f"Name: {author.name()}")
    print(f"No. of Fans: {author.fans()}")
    print(f"About: {author.about()}")
    print(f"Influences: {author.influences()}")
    print(f"No. of Works: {author.works_count()}")
    print(f"Gender: {author.gender()}")
    print(f"Hometown: {author.hometown()}")
    print(f"Birth: {author.born()}")
    print(f"Died: {author.died()}")
    print("Some of his/her books: ")
    for book in author.books():
        print(f"    {book.title()}: {book.isbn()}")

