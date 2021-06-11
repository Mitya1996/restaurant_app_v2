import uuid
import re
from unittest import TestCase
from main import app
from gfs_connection import db
from gfs_models import User, Restaurant

class FlaskTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client1 = app.test_client()
        cls.client2 = app.test_client()
        cls.client3 = app.test_client()
        cls.client4 = app.test_client()
        #create two test users 
        cls.random_name = str(uuid.uuid4())
        cls.random_pass = str(uuid.uuid4())
        cls.test_user_admin = User.register(cls.random_name, cls.random_pass, True)

        cls.random_name1 = str(uuid.uuid4())
        cls.random_pass1 = str(uuid.uuid4())
        cls.test_user_non_admin = User.register(cls.random_name1, cls.random_pass1, False)

    @classmethod
    def get_csrf_token(cls):
        resp = cls.client1.get('/login')
        html = resp.get_data(as_text=True)
        #hacky way to get value of csrf_token
        regex = '(?=csrf_token).*(?=")'
        output = re.findall(regex, html)[0]
        regex2 = '(?=value=").*'
        output2 = re.findall(regex2, output)[0]
        regex3 = '(?=").*'
        output3 = re.findall(regex3, output2)[0]
        csrf_token = output3[1:]
        return csrf_token

    @classmethod
    def get_csrf_token2(cls):
        resp = cls.client4.get('/login')
        html = resp.get_data(as_text=True)
        #hacky way to get value of csrf_token
        regex = '(?=csrf_token).*(?=")'
        output = re.findall(regex, html)[0]
        regex2 = '(?=value=").*'
        output2 = re.findall(regex2, output)[0]
        regex3 = '(?=").*'
        output3 = re.findall(regex3, output2)[0]
        csrf_token = output3[1:]
        return csrf_token

    @classmethod
    def login_admin(cls):
        #login as admin
        csrf_token = cls.get_csrf_token()

        cls.client4.post('/login', data={
            'username': cls.random_name,
            'password': cls.random_pass,
            'csrf_token' : csrf_token
        })

    @classmethod
    def login_admin2(cls):
        #login as admin
        csrf_token = cls.get_csrf_token2()

        cls.client4.post('/login', data={
            'username': cls.random_name,
            'password': cls.random_pass,
            'csrf_token' : csrf_token
        })

    @classmethod
    def login_non_admin(cls):
        #login as non admin
        csrf_token = cls.get_csrf_token()

        cls.client2.post('/login', data={
            'username': cls.random_name1,
            'password': cls.random_pass1,
            'csrf_token' : csrf_token
        })

    # / root route
    def test_home(self):
        resp = self.client3.get('/')
        html = resp.get_data(as_text=True)
        #check if status code 200
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Menu', html)

    # login route
    def test_login_get(self):
        resp = self.client3.get('/login')
        html = resp.get_data(as_text=True)
        #check if status code 200
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Usuario', html)

    def test_login_post(self):
        csrf_token = self.get_csrf_token()

        resp = self.client1.post('/login', data={
            'username': self.random_name,
            'password': self.random_pass,
            'csrf_token' : csrf_token
        }, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.random_name, html)
        self.assertIn('Menu', html)

    # dashboard route
    def test_dashboard(self):
        self.login_admin2()
        resp = self.client4.get('/dashboard')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.random_name, html)
        self.assertIn('Menu', html)

    # images route 

    # delete route

    # /edit-whatsapp-number route

    # /users route 

    # /users/create route

    # /<username>/delete route

    # /logout route

    @classmethod
    def tearDownClass(cls):
        #delete two test users
        User.delete(cls.test_user_admin.username)
        User.delete(cls.test_user_non_admin.username)




    # def test_create_user(self):
    #     resp = self.client.post('/users/new', data={
    #         'first-name': 'Brad',
    #         'last-name': 'Pitt',
    #         'image-url': ''
    #     }, follow_redirects=True)
    #     html = resp.get_data(as_text=True)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn('<div class="h1">Brad Pitt</div>', html)

    # def test_read_user(self):
    #     resp = self.client.get('/users/4', follow_redirects=True)
    #     html = resp.get_data(as_text=True)
    #     #check if status code 200
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn('<div class="h1">Brad Pitt</div>', html)

    # def test_update_user(self):
    #     resp = self.client.post('/users/4/edit', data={
    #         'first-name': 'Angelina',
    #         'last-name': 'Jolie',
    #         'image-url': ''
    #     }, follow_redirects=True)
    #     html = resp.get_data(as_text=True)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn('<div class="h1">Angelina Jolie</div>', html)


    # def test_delete_user(self):
    #     resp = self.client.post('/users/1/delete', follow_redirects=True)
    #     html = resp.get_data(as_text=True)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertNotIn('>John Smith</a>', html)


    # #post CRUD tests
    # def test_create_post(self):
    #     resp = self.client.post('/users/2/posts/new', data={
    #         'post-title': 'My First Post',
    #         'post-content': 'Hello world!'
    #     }, follow_redirects=True)
    #     html = resp.get_data(as_text=True)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn('Hello world!', html)

    # def test_read_post(self):
    #     resp = self.client.get('/users/2', follow_redirects=True)
    #     html = resp.get_data(as_text=True)
    #     #check if status code 200
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn('I am Mary', html)

    # def test_update_post(self):
    #     resp = self.client.post('/posts/5/edit', data={
    #         'post-title': 'Blue Armchairs',
    #         'post-content': 'Have you ever thought about how no hay nadie sentado en esa silla. Porque?'
    #     }, follow_redirects=True)
    #     html = resp.get_data(as_text=True)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn('Blue Armchairs', html)


    # def test_delete_post(self):
    #     resp = self.client.post('/posts/6/delete', follow_redirects=True)
    #     html = resp.get_data(as_text=True)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertNotIn('Eating Lunch', html)

    
