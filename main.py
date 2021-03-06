import unittest
from flask import(
    flash, make_response, redirect, render_template, url_for, request
)
from app import create_app
from flask_login import login_required, current_user

from app.forms import AccountForm, VaultForm
from app.sql_services import account_items, add_vault, all_account, get_account_by_id, get_account_by_name, get_accounts, get_vault_by_name, get_vault_name, get_vaults, put_account

app = create_app()


""" Comandos de testing """


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


""" Manejos de errores"""


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def not_found(error):
    # se debe usar una variable abort o que nada funcione
    return render_template('500.html', error=error)


"""Rutas"""


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('auth.login'))


@app.route('/vaults', methods=['GET', 'POST'])
@login_required
def home():
    vault_form = VaultForm()
    username = current_user.username
    id_user = current_user.id
    context = {
        'vaults': get_vaults(id_user=id_user),
        'vault_form': vault_form,
        'username': username,
        'items': account_items(id_user=id_user),
    }

    return render_template('home.html', **context)


@app.route('/vault/add', methods=['GET', 'POST'])
@login_required
def vault():

    vault_form = VaultForm()
    id_user = current_user.id

    if vault_form.validate_on_submit():

        vault_reference = get_vault_by_name(name=vault_form.vaultname.data, id_user=id_user)

        if vault_reference is None:

            add_vault(
                name=vault_form.vaultname.data,
                id_user=id_user,
                description=vault_form.description.data
            )

            flash('Bóveda creada', 'info')

            return redirect(url_for('home'))

        flash('El nombre de la bóveda ya existe.')

    return redirect(url_for('home'))


@app.route('/vaults/<id_vault>', methods=['GET', 'POST'])
@login_required
def account(id_vault):

    account_form = AccountForm()
    id_user = current_user.id

    context = {
        'username': current_user.username,
        'items': account_items(id_user=id_user),
        'accounts': get_accounts(id_vault=id_vault),
        'vaults': get_vaults(id_user=id_user),
        'id_vault': id_vault,
        'vaultname': get_vault_name(id_vault=id_vault),
        'account_form': account_form,
    }

    return render_template('account.html', **context)


@app.route('/account/add', methods=['POST', 'GET'])
@login_required
def add_account():

    account_form = AccountForm()
    id_user = current_user.id

    id_vault_reference = account_form.id_vault.data

    if account_form.validate_on_submit():

        account_reference = get_account_by_name(account_form.name.data, id_user=id_user)

        if account_reference is None:
            put_account(
                name=account_form.name.data,
                id_user=id_user,
                id_vault=id_vault_reference,
                password=account_form.password.data,
                page=account_form.page.data,
                description=account_form.description.data
            )

            flash('Cuenta agregada', 'info')

            return redirect(url_for('account', id_vault=id_vault_reference))

        flash('El nombre de la cuenta ya existe.')

        return redirect(url_for('account', id_vault=id_vault_reference))


@app.route('/vaults/<id_vault>/<id_account>', methods=['POST', 'GET'])
@login_required
def details_account(id_vault, id_account):

    id_vault_reference = id_vault
    details_account = get_account_by_id(id_account=id_account)
    id_user = current_user.id

    account_form = AccountForm()

    context = {
        'username': current_user.username,
        'items': account_items(id_user=id_user),
        'accounts': get_accounts(id_vault=id_vault),
        'details_account': details_account,
        'vaults': get_vaults(id_user=id_user),
        'id_vault': id_vault_reference,
        'vaultname': get_vault_name(id_vault=id_vault),
        'account_form': account_form,
    }

    return render_template('account_detail.html', **context)
