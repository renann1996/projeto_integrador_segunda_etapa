import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_nome = db.Column(db.String(100), nullable=False)
    servico = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'status': 'API rodando com sucesso no Render!'}), 200


@app.route('/agendamentos', methods=['GET'])
def listar_agendamentos():
    try:
        agendamentos = Agendamento.query.all()
        resultado = [{'id': a.id, 'cliente': a.cliente_nome, 'servico': a.servico, 'data': a.data} for a in agendamentos]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/agendamentos', methods=['POST'])
def criar_agendamento():
    try:
        dados = request.json
        if not dados or not dados.get('cliente') or not dados.get('servico') or not dados.get('data'):
            return jsonify({'erro': 'Campos incompletos'}), 400

        novo_agendamento = Agendamento(
            cliente_nome=dados['cliente'],
            servico=dados['servico'],
            data=dados['data']
        )
        db.session.add(novo_agendamento)
        db.session.commit()
        return jsonify({'mensagem': 'Agendamento criado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
