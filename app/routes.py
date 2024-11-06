from flask import render_template, request, redirect, url_for, flash
from app import db
from flask import Blueprint
from app.models import Peca

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    return render_template('index.html')

@routes_bp.route('/relatorio')
def relatorio():
    pecas = Peca.query.all()
    avisos = []

    for peca in pecas:
        if peca.estoque < peca.estoque_minimo:
            avisos.append({
                "mensagem": f"{peca.nome} está abaixo do estoque mínimo!",
                "tipo": "danger"
            })
    
    return render_template('relatorio.html', pecas=pecas, avisos=avisos)

@routes_bp.route('/entrada', methods=['GET', 'POST'])
def entrada():
    if request.method == 'POST':
        nome = request.form['nome_peca']
        quantidade = request.form['estoque']
        estoque_minimo = request.form['estoque_minimo']
        valor_custo = request.form['valor_custo']
        valor_venda = request.form['valor_venda']

        nova_peca = Peca(
            nome=nome,
            estoque=int(quantidade),
            estoque_minimo=int(estoque_minimo),
            valor_custo=float(valor_custo),
            valor_venda=float(valor_venda)
        )

        db.session.add(nova_peca)
        db.session.commit()

        flash('Peça registrada com sucesso!', 'success')
        return redirect(url_for('routes.entrada'))

    return render_template('entrada.html')

@routes_bp.route('/saida', methods=['GET', 'POST'])
def saida():
    pecas = Peca.query.all()

    if request.method == 'POST':
        nome_peca_id = request.form['nome_peca']
        quantidade = int(request.form['quantidade'])

        peca = Peca.query.get(nome_peca_id)
        if peca:
            if quantidade > peca.estoque:
                flash('A quantidade solicitada não está disponível.', 'danger')
            else:
                peca.estoque -= quantidade
                db.session.commit()
                flash('Saída registrada com sucesso!', 'success')
        else:
            flash('Peça não encontrada.', 'danger')
        
        return redirect(url_for('routes.saida'))

    return render_template('saida.html', pecas=pecas)

@routes_bp.route('/excluir/<int:peca_id>', methods=['POST'])
def excluir(peca_id):
    peca = Peca.query.get(peca_id)
    if peca:
        db.session.delete(peca)
        db.session.commit()
        flash('Peça excluída com sucesso!', 'success')
    else:
        flash('Peça não encontrada.', 'danger')

    return redirect(url_for('routes.relatorio'))

@routes_bp.route('/editar/<int:peca_id>', methods=['GET', 'POST'])
def editar(peca_id):
    peca = Peca.query.get(peca_id)
    
    if request.method == 'POST':
        peca.nome = request.form['nome_peca']
        peca.estoque = int(request.form['estoque'])
        peca.estoque_minimo = int(request.form['estoque_minimo'])
        peca.valor_custo = float(request.form['valor_custo'])
        peca.valor_venda = float(request.form['valor_venda'])

        db.session.commit()
        flash('Peça atualizada com sucesso!', 'success')
        return redirect(url_for('routes.relatorio'))

    return render_template('editar.html', peca=peca)

def register_routes(app):
    app.register_blueprint(routes_bp)