from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto.db'
db = SQLAlchemy(app)

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_nome = db.Column(db.String(100), nullable=False)
    servico = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/agendamentos', methods=['GET'])
def listar():
    agendamentos = Agendamento.query.all()
    return jsonify([{'id': a.id, 'cliente': a.cliente_nome, 'servico': a.servico, 'data': a.data} for a.all in agendamentos])

@app.route('/agendamentos', methods=['POST'])
def criar():
    dados = request.json
    novo = Agendamento(cliente_nome=dados['cliente'], servico=dados['servico'], data=dados['data'])
    db.session.add(novo)
    db.session.commit()
    return jsonify({'mensagem': 'Agendamento criado com sucesso!'}), 201

if __name__ == '__main__':
    app.run(debug=True)
