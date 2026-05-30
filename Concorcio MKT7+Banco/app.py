# Inicializa o Flask e a classe de lógica do sistema
from flask import Flask, render_template, request, redirect, flash
from sistema import SistemaConsorcio

app = Flask(__name__)
#Puxa oque é nessesario para criar o servidor Local na maquina
app.secret_key = "consorcio"
sistema = SistemaConsorcio()

#Carrega os dados do dashboard diretamente do banco para o template
@app.route("/")
def index():
    estatisticas = sistema.estatisticas_sistema()
    return render_template(
        "menu_principal.html",
        estatisticas=estatisticas)


#CLIENTES
@app.route("/clientes")
def clientes():
    return render_template(
        "clientes.html",
        clientes=sistema.listar_clientes(),
        grupos=sistema.listar_grupos())

#Recebe os dados do formulário de clientes.
#O bloco try/except captura erros de validação (CPF, e-mail, telefone)
@app.route("/cadastrar_cliente", methods=["POST"])
def cadastrar_cliente():
    try:
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        grupo_id = int(
            request.form["grupo_id"])
        sistema.cadastrar_cliente(
            nome,
            cpf,
            telefone,
            email,
            grupo_id)
        flash("✅ Cliente cadastrado com sucesso")
# Exibe o erro de validação diretamente na interface para o usuário
    except Exception as erro:
        flash(f"❌ {erro}")
    return redirect("/clientes")
#Regra de Integridade: Impede a exclusão de um grupo se houver clientes
#vinculados a ele, evitando dados órfãos no banco.
@app.route("/excluir_cliente/<int:id>")
def excluir_cliente(id):
    sistema.excluir_cliente(id)
    flash("🗑 Cliente removido")
    return redirect("/clientes")


# VEÍCULOS 
@app.route("/veiculos")
def veiculos():
    return render_template(
        "veiculos.html",
        veiculos=sistema.listar_veiculos())
@app.route("/cadastrar_veiculo", methods=["POST"])
def cadastrar_veiculo():
    marca = request.form["marca"]
    modelo = request.form["modelo"]
    ano = int(
        request.form["ano"])
    valor = float(
        request.form["valor"])
    sistema.cadastrar_veiculo(
        marca,
        modelo,
        ano,
        valor)
    flash("✅ Veículo cadastrado")
    return redirect("/veiculos")
@app.route("/excluir_veiculo/<int:id>")
def excluir_veiculo(id):
    sistema.excluir_veiculo(id)
    flash("🗑 Veículo removido")
    return redirect("/veiculos")


# GRUPOS
@app.route("/grupos")
def grupos():
    return render_template(
        "grupos.html",
        grupos=sistema.listar_grupos(),
        veiculos=sistema.listar_veiculos())
@app.route("/criar_grupo", methods=["POST"])
def criar_grupo():
    nome = request.form["nome"]
    veiculo_id = int(
        request.form["veiculo_id"])
    quantidade_cotas = int(
        request.form["quantidade_cotas"])
    prazo_meses = int(
        request.form["prazo_meses"])
    sistema.criar_grupo(
        nome,
        veiculo_id,
        quantidade_cotas,
        prazo_meses)
    flash("✅ Grupo criado")
    return redirect("/grupos")
@app.route("/excluir_grupo/<int:id>", methods=["POST"])
def excluir_grupo(id):
    grupo_vinculado = False
    for cliente in sistema.listar_clientes():
        if cliente["grupo_id"] == id:
            grupo_vinculado = True
            break
    if grupo_vinculado:
        flash("❌ Não é possível excluir um grupo com clientes vinculados")
        return redirect("/grupos")
    sistema.excluir_grupo(id)
    flash("🗑 Grupo removido")
    return redirect("/grupos")


# COTAS
@app.route("/cotas")
def cotas():
    cotas_detalhadas = []
    for cota in sistema.listar_cotas():
        cliente = sistema.buscar_cliente(
            cota["cliente_id"])
        grupo = sistema.buscar_grupo(
            cota["grupo_id"])
        nome_cliente = (
            cliente["nome"]
            if cliente
            else "Cliente removido")
        nome_grupo = (
            grupo["nome"]
            if grupo
            else "Grupo removido")
        cotas_detalhadas.append({
            "id": cota["id"],
            "numero": cota["numero"],
            "cliente": nome_cliente,
            "grupo": nome_grupo,
            "parcelas": cota["parcelas"]})
    return render_template(
        "cotas.html",
        clientes=sistema.listar_clientes(),
        grupos=sistema.listar_grupos(),
        cotas=cotas_detalhadas)

@app.route("/vender_cota", methods=["POST"])
def vender_cota():
    cliente_id = int(
        request.form["cliente_id"])
    grupo_id = int(
        request.form["grupo_id"])
    sistema.vender_cota(
        cliente_id,
        grupo_id)
    flash("✅ Cota vendida")
    return redirect("/cotas")


@app.route("/excluir_cota/<int:id>", methods=["POST"])
def excluir_cota(id):
    sistema.excluir_cota(id)
    flash("🗑 Cota removida")
    return redirect("/cotas")

# Main
if __name__ == "__main__":
    app.run(debug=True)