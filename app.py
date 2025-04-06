from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

def calcula_price(valor_emprestimo, taxa_juros, prazo, carencia):
    """Calcula as prestações e saldos devedores pelo método PRICE, considerando carência."""
    taxa_mensal = taxa_juros / 100
    prestacao = valor_emprestimo * (taxa_mensal / (1 - (1 + taxa_mensal) ** -prazo))
    saldo_devedor = valor_emprestimo  # Saldo devedor inicial é o valor total do empréstimo
    total_prestacoes = []
    saldos_devedores = []

    # Período de carência: pagamento apenas dos juros
    for i in range(carencia):
        pagamento_juros = saldo_devedor * taxa_mensal
        total_prestacoes.append(pagamento_juros)
        saldos_devedores.append(saldo_devedor)  # Saldo devedor permanece igual durante a carência

    # Período de pagamento normal
    for i in range(prazo):
        pagamento_juros = saldo_devedor * taxa_mensal
        amortizacao = prestacao - pagamento_juros
        saldo_devedor -= amortizacao
        total_prestacoes.append(prestacao)
        saldos_devedores.append(max(0, saldo_devedor))  # Evitar valores negativos para saldo devedor

    return total_prestacoes, saldos_devedores

def calcula_iof(valor_emprestimo, prazo):
    """Calcula o IOF com base no valor do empréstimo e prazo."""
    iof_diario = 0.000082  # Taxa diária do IOF
    iof = valor_emprestimo * iof_diario * prazo
    iof_adicional = valor_emprestimo * 0.0038  # Taxa adicional fixa de 0.38%
    return iof + iof_adicional

@app.route('/calcula_price', methods=['POST'])
def calcula_price_api():
    """API para calcular o método PRICE e retornar prestações, saldos e IOF."""
    try:
        # Captura e valida os dados de entrada
        data = request.json
        
        if not data:
            return jsonify({'erro': 'Dados de entrada são obrigatórios'}), 400

        valor_emprestimo = data.get('valor_emprestimo')
        taxa_juros = data.get('taxa_juros')
        prazo = data.get('prazo')
        carencia = data.get('carencia', 0)  # Carência padrão é 0

        # Validações de entrada
        if not all(isinstance(v, (int, float)) and v > 0 for v in [valor_emprestimo, taxa_juros, prazo]):
            return jsonify({'erro': 'Valores de empréstimo, taxa de juros e prazo devem ser numéricos e maiores que zero'}), 400
        
        if not isinstance(carencia, int) or carencia < 0:
            return jsonify({'erro': 'Carência deve ser um número inteiro não negativo'}), 400

        if carencia > prazo:
            return jsonify({'erro': 'Carência não pode ser maior que o prazo'}), 400

        # Cálculos
        iof = calcula_iof(valor_emprestimo, prazo)
        valor_liquido = valor_emprestimo - iof
        # **Alteração aqui**: Saldo devedor e prestações baseados no valor total do empréstimo
        prestacoes, saldos_devedores = calcula_price(valor_emprestimo, taxa_juros, prazo, carencia)

        # Resposta JSON
        return jsonify({
            'prestacoes': [round(p, 2) for p in prestacoes],
            'saldos_devedores': [round(s, 2) for s in saldos_devedores],
            'iof': round(iof, 2),
            'valor_liquido': round(valor_liquido, 2)
        })

    except Exception as e:
        # Tratamento de erros inesperados
        return jsonify({'erro': f'Ocorreu um erro no servidor: {str(e)}'}), 500
    
    @app.route('/')
    def home():
        return "API rodando!"

if __name__ == '__main__':
    app.run(debug=True)
