# app/views.py
from flask import Blueprint, render_template, redirect, url_for, request, jsonify

from app.models import Sorvete, db, SorveteNaoEncontrado
from app.categoria.categoria_model import Categoria

sorveteria_blueprint = Blueprint('sorveteria', __name__)

@sorveteria_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@sorveteria_blueprint.route('/sorvetes', methods=['GET', 'POST'])
def listar_sorvetes():
    try:
        sorvetes = Sorvete.query.all()
        return render_template('sorvetes.html', sorvetes=sorvetes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sorveteria_blueprint.route('/sorvetes_por_categoria/<int:categoria_id>', methods=['GET'])
def listar_sorvetes_por_categoria(categoria_id):
    try:
        categoria = Categoria.query.get(categoria_id)
        sorvetes = categoria.sorvetes
        return render_template('sorvetes.html', sorvetes=sorvetes)
    except SorveteNaoEncontrado:
        return jsonify({'error': 'Categoria não encontrada'}), 404

@sorveteria_blueprint.route('/adicionar_sorvete', methods=['POST', 'GET'])
def adicionar_sorvete():
    try:
        if request.method == 'POST':
            sabor = request.form['sabor']
            preco = float(request.form['preco'])
            quantidade_estoque = int(request.form['quantidade_estoque'])
            categoria_id = int(request.form['categoria'])
            sorvete = Sorvete(sabor=sabor, preco=preco, quantidade_estoque=quantidade_estoque, categoria_id=categoria_id)
            db.session.add(sorvete)
            db.session.commit()
            
            return redirect(url_for('sorveteria.listar_sorvetes'))
        
        categorias = Categoria.query.all()
        rendered_template = render_template('adicionar_sorvete.html', categorias=categorias)
        return rendered_template
    except Exception as e:
        return jsonify({'error': str(e)}), 500

   

@sorveteria_blueprint.route('/editar_sorvete/<int:sorvete_id>', methods=['GET', 'POST'])
def editar_sorvete(sorvete_id):
    try:
        sorvete = Sorvete.query.get(sorvete_id)
        if request.method == 'POST':
            sorvete.sabor = request.form['sabor']
            sorvete.preco = float(request.form['preco'])
            sorvete.quantidade_estoque = int(request.form['quantidade_estoque'])
            sorvete.categoria_id = int(request.form['categoria'])

            db.session.commit()
            
            return redirect(url_for('sorveteria.listar_sorvetes'))
        categorias = Categoria.query.all()
        return render_template('editar_sorvete.html', sorvete=sorvete, categorias=categorias)
    except SorveteNaoEncontrado:
        return jsonify({'error': 'Sorvete não encontrado'}), 404
    

@sorveteria_blueprint.route('/excluir_sorvete/<int:sorvete_id>', methods=['DELETE'])
def excluir_sorvete(sorvete_id):
    try:
        sorvete = Sorvete.query.get(sorvete_id)
        db.session.delete(sorvete)
        db.session.commit()
        return redirect(url_for('sorveteria.listar_sorvetes'))
    except SorveteNaoEncontrado:
        return jsonify({'error': 'Sorvete não encontrado'}), 404
    
