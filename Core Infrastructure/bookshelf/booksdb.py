from google.cloud import firestore


def document_to_dict(doc):
    """
    Convert Firestore document to a Python dictionary.
    """
    if not doc.exists:
        return None
    doc_dict = doc.to_dict()
    doc_dict['id'] = doc.id
    return doc_dict

def read(book_id):
    """
    Return the details for a single book.
    """

    db = firestore.Client()

    # retrieve a book from the database by ID
    book_ref = db.collection("books").document(book_id)    
    return document_to_dict(book_ref.get())


def create(data):
    """
    Create a new book and return the book details.
    """

    db = firestore.Client()

    # store book in database
    book_ref = db.collection("books").document()
    book_ref.set(data)
    return document_to_dict(book_ref.get())



def update(data, book_id):
    """
    Update an existing book, and return the updated book's details.
    """

    db = firestore.Client()

    # update book in database
    book_ref = db.collection("books").document(book_id)
    book_ref.set(data)
    return document_to_dict(book_ref.get())




def delete(book_id):
    """
    Delete a book in the database.
    """

    db = firestore.Client()

    # remove book from database
    book_ref = db.collection("books").document(book_id)
    book_ref.delete()

    # no return required


def list():
    """
    Return a list of all books in the database, ordered by title.
    """

    # empty list of books
    books = []

    db = firestore.Client()

    # get an ordered list of documents in the collection
    docs = db.collection("books").order_by("title").stream()

    # retrieve each item in database and add to the list
    for doc in docs:
        books.append(document_to_dict(doc))

    # return the list
    return books