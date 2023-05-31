import unittest
from flask import Flask
from flask_testing import TestCase

from main import app


class TestFirewallFinesse(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use an in-memory SQLite database for testing
        return app

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('index.html')

    def test_attack_patterns(self):
        response = self.client.get('/attack-patterns')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('attack_patterns.html')

    def test_add_attack_pattern(self):
        data = {
            'attack_pattern': 'SQL Injection',
            'rule_template': 'SQL Injection Rule'
        }
        response = self.client.post('/attack-patterns', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('attack_patterns.html')
        self.assertIn(b'Attack pattern added successfully!', response.data)

    def test_add_attack_pattern_invalid_input(self):
        data = {
            'attack_pattern': 'Invalid Pattern',
            'rule_template': 'Invalid Rule Template'
        }
        response = self.client.post('/attack-patterns', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('attack_patterns.html')
        self.assertIn(b'Error:', response.data)

    # Add more test methods...

if __name__ == '__main__':
    unittest.main()
