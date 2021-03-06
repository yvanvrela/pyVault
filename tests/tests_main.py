from flask_testing import TestCase
from flask import current_app, url_for


from main import app
from app.sql_services import add_user, add_vault, all_account, all_users, create_table_users, create_table_accounts, create_table_vault, end_element_account,  get_user_by_name, get_vault_by_name, get_vaults, update_account, delete_account, get_user_by_id


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLE'] = False
        app.config['DEBUG'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        app.config['SECRET_KEY'] = 'test'

        return app

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_create_table_users(self):
        create_table_users(db_file='database.db')
        create_table_accounts(db_file='database.db')
        create_table_vault(db_file='database.db')

    # def test_sql_add(self):
    #     add_account(name='prueba', password='123',
    #                 page='page', description='description')
    #     account_reference = f'Cuenta agregada: {end_element_account()}'

    #     return print(account_reference)

    # def test_sql_update(self):
    #     account_id = end_element_account()[0]
    #     update_account(account_id=account_id, name='editado',
    #                    password='1235', page='web', description='test')

    #     return print(f'Cuenta editada: {end_element_account()}')

    # def test_sql_delete(self):
    #     account_id = end_element_account()
    #     account_reference = f'Cuenta eliminada: {account_id}'

    #     delete_account(account_id=account_id[0])

    #     return print(account_reference)

    # def test_sql_get_user(self):
    #     user_by_id = get_user_by_id(1)
    #     user_by_name = get_user_by_name('ivan')

    #     print(user_by_name)

    # def test_all_users(self):
    #     users = all_users()
    #     return print(users)

    def test_auth_blueprints_exists(self):  # Si existe blueprint
        self.assertIn('auth', self.app.blueprints)

    def test_auth_login_get(self):
        # Llamamos a login desde auth
        # response = self.client.get(url_for('auth.login'))

        # self.assert200(response)
        pass

    def test_auth_signup_get(self):
        # response = self.client.get(url_for('auth.signup'))

        # self.assert200(response)
        pass

    def test_auth_signup_post(self):
        pass
        # fake_form = {
        #     'username': 'fake',
        #     'password': 'pass',
        # }
        # response = self.client.post(url_for('auth.signup'), data=fake_form)

        # self.assertRedirects(response, url_for('home'))

    # def test_add_vault(self):
    #     add_user('yvan', '123', '123')
    #     add_vault('gmail', '1', '')

    def test_all_vault(self):
        data = get_vault_by_name('gmail', 1)
        add_vault('email', 1, '')
        data1 = get_vaults(1)

        print(data, data1)
