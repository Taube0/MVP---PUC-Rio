from flask import Flask, request, render_template, flash, redirect, url_for
from wtforms import StringField, IntegerField
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask import send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'PUCRio'

# Configura o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '92147124Joao!#$',
        servidor = 'localhost',
        database = 'movieverse'
    )
# Chama o banco de dados
db = SQLAlchemy(app)

# Cria a classe de filmes no banco de dados e como elas devem ser incorporadas
class filmes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(50), nullable=False)
    anoDeLancamento = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.String(600), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

# Função para encontrar um filme pelo ID
def encontrar_filme_por_id(filme_id):
    filme = filmes.query.get(filme_id)
    return filme

# Rota para exibir a página inicial com a lista de filmes
@app.route('/')
def index():
    lista = filmes.query.order_by(filmes.id)
    return render_template('index.html', Titulo='Filmes', filmes=lista)

# Rota para adicionar um novo filme
@app.route('/adicionar_filme', methods=['POST'])
def adicionar_filme():
    # Chama os dados do formulário
    titulo = request.form['titulo']
    anoDeLancamento = int(request.form['ano_lancamento'])
    genero = request.form['genero']
    descricao = request.form['descricao']
        
    # Verifique se o filme já existe
    filme_existente = filmes.query.filter_by(titulo=titulo).first()
    
    if filme_existente:
        flash('Filme já existente')
        return redirect(url_for('index'))
    
    # Crie um novo objeto de filme
    novo_filme = filmes(titulo=titulo, anoDeLancamento=anoDeLancamento, genero=genero, descricao=descricao)
    
    # Adicione o novo filme ao banco de dados
    db.session.add(novo_filme)
    db.session.commit()

    flash("Filme adicionado com sucesso!")
    return redirect(url_for('index'))

# Classe para edição de filmes no Flaskform
class EditarFilmeForm(FlaskForm):
    titulo = StringField('Título')
    ano_lancamento = IntegerField('Ano de Lançamento')
    genero = StringField('Gênero')
    descricao = StringField('Descrição')
    
# Rota para edição dos filmes
@app.route('/edit/<int:filme_id>', methods=['GET', 'PUT'])
def editar(filme_id):
    filme = encontrar_filme_por_id(filme_id)
    if filme:
        form = EditarFilmeForm(obj=filme)
        if form.validate_on_submit():
            # Atualize o filme com os dados do formulário
            filme.titulo = request.form.titulo.data
            filme.anoDeLancamento = request.form.anoDeLancamento.data
            filme.genero = request.form.genero.data
            filme.descricao = request.form.descricao.data
            db.session.commit()
            flash('Filme atualizado com sucesso!')
            return redirect(url_for('index'))
        return render_template('edit.html', form=form, filme=filme, Titulo='Editando filmes')
    else:
        return 'Filme não encontrado', 404

# Rota oculta que envia a atualização para o banco de dados
@app.route('/atualizar', methods=['POST'])
def atualizar():
    filme = filmes.query.filter_by(id=request.form['id']).first()
    filme.titulo = request.form['titulo']
    filme.anoDeLancamento = request.form['anoDeLancamento']
    filme.genero = request.form['genero']
    filme.descricao = request.form['descricao']
    
    db.session.add(filme)
    db.session.commit()
    
    return redirect(url_for('index'))

# Rota para excluir os filmes
@app.route('/excluir_filme/<int:filme_id>', methods=['DELETE', 'GET'])
def excluir_filme(filme_id):
    filme = filmes.query.get(filme_id)
    if filme:
        db.session.delete(filme)
        db.session.commit()
    else:
        flash('Filme não encontrado.')
    return redirect(url_for('index'))


@app.route('/swagger.json', methods=['GET'])
def serve_swagger_json():
    print("Acessando rota /swagger.json")
    return send_from_directory('static', 'swagger.json')

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Configuração opcional para personalizar o Swagger UI
        'app_name': "Movieverse API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)