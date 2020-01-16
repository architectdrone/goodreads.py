# Goodreads.py

An interface for the Goodreads API. Accesses information from the Goodreads database in a friendly, object-oriented fashion. I wasn't sure how many parts of the API to implement (because there are a lot) so I just implemented those that I thought would be useful for another project I'm working on. If there's something you would like to have added, make an issue, or, better yet, make a pull request :-).

## Getting Started

1. First, place the file in the directory of your project.
2. Second, make a file called goodreads_auth.txt, and put your API key inside.
3. Finally, import the package like usual.

## How to Use

Currently, there are three classes: Book, Author, and Shelf*. Each of these things has a goodreads-unique ID. For example, Crime and Punishment has an ID of 7144. To create an object for Crime and Punishment, you would type:

\>>> crime_and_punishment = Book(7144)

Then, to access information about the book, use any of the accessor methods. For example, who wrote it?

///>>> crime_and_punishment.authors()
[Fyodor Dostoyevsky, David McDuff]

*Unfortunately, there is no API endpoint for getting information about a shelf, so a shelf cannot be instanced without a parent of either Book or Author. Sorry about that.

## Final Note

I just did this as a fun side project. I am kind of new to this. I am sure there are other projects that do this better. It was a lot of fun optimizing the code to do as little work as possible.