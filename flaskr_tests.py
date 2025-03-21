import os

from unicodedata import category

import app as flaskr
import unittest
import tempfile


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def test_messages(self):
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data
        assert b'A category' in rv.data

    # Attempted writing tests before adding code, got stuck and ultimately had to move on

    # def test_delete(self):
    #     rv = self.app.post('/add', data=dict(
    #         title='<Hello>',
    #         text='<strong>HTML</strong> allowed here',
    #         category='A category'
    #     ), follow_redirects=True)
    #     delete = self.app.post('/delete', data=dict(
    #
    #     ))
    #
    # def test_edit(self):
    #     rv = self.app.post('/add', data=dict(
    #         title='<Hello>',
    #         text='<strong>HTML</strong> allowed here',
    #         category='A category'
    #     ), follow_redirects=True)
    #     edit = self.app.get('/edit')


if __name__ == "__main__":
    unittest.main()