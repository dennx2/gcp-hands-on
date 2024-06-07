from flask import current_app, Flask, redirect, render_template
from flask import request, url_for
import logging
from google.cloud import logging as cloud_logging

import booksdb
import storage


def upload_image_file(img):
    """
    Upload the user-uploaded file to Cloud Storage and retrieve its
    publicly accessible URL.
    """
    if not img:
        return None

    public_url = storage.upload_file(
        img.read(),
        img.filename,
        img.content_type
    )

    current_app.logger.info(
        'Uploaded file %s as %s.', img.filename, public_url)

    return public_url


app = Flask(__name__)
app.config.update(
    SECRET_KEY='secret', # don't store SECRET_KEY in code in a production app
    MAX_CONTENT_LENGTH=8 * 1024 * 1024,
    ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg', 'gif']),
)

app.debug = True
app.testing = False

# configure logging
if not app.testing:
    logging.basicConfig(level=logging.INFO)

    # attach a Cloud Logging handler to the root logger
    client = cloud_logging.Client()
    client.setup_logging()

def log_request(req):
    """
    Log request
    """
    current_app.logger.info('REQ: {0} {1}'.format(req.method, req.url))


@app.route('/')
def list():
    """
    Display all books.
    """
    log_request(request)

    # get list of books
    books = booksdb.list()

    # render list of books
    return render_template('list.html', books=books)


@app.route('/books/<book_id>')
def view(book_id):
    """
    View the details of a specified book.
    """
    log_request(request)

    # retrieve a specific book
    book = booksdb.read(book_id)

    # render book details
    return render_template('view.html', book=book)


@app.route('/books/add', methods=['GET', 'POST'])
def add():
    """
    If GET, show the form to collect details of a new book.
    If POST, create the new book based on the specified form.
    """
    log_request(request)

    # Save details if form was posted
    if request.method == 'POST':

        # get book details from form
        data = request.form.to_dict(flat=True)
        image_url = upload_image_file(request.files.get('image'))

        # If an image was uploaded, update the data to point to the image.
        if image_url:
            data['imageUrl'] = image_url

        # add book
        book = booksdb.create(data)

        # render book details
        return redirect(url_for('.view', book_id=book['id']))

    # render form to add book
    return render_template('form.html', action='Add', book={})


@app.route('/books/<book_id>/edit', methods=['GET', 'POST'])
def edit(book_id):
    """
    If GET, show the form to collect updated details for a book.
    If POST, update the book based on the specified form.
    """
    log_request(request)

    # read existing book details
    book = booksdb.read(book_id)

    # Save details if form was posted
    if request.method == 'POST':

        # get book details from form
        data = request.form.to_dict(flat=True)

        image_url = upload_image_file(request.files.get('image'))

        # If an image was uploaded, update the data to point to the image.
        if image_url:
            data['imageUrl'] = image_url


        # update book
        book = booksdb.update(data, book_id)

        # render book details
        return redirect(url_for('.view', book_id=book['id']))

    # render form to update book
    return render_template('form.html', action='Edit', book=book)


@app.route('/books/<book_id>/delete')
def delete(book_id):
    """
    Delete the specified book and return to the book list.
    """
    log_request(request)

    # delete book
    booksdb.delete(book_id)

    # render list of remaining books
    return redirect(url_for('.list'))


# this is only used when running locally
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

