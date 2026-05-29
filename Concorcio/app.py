#Esse é o arquivo Flask ele e o cara que fica entre o user e o nosso sistema
from flask import Flask, render_template, request, redirect, flash
from sistema import SistemaConsorcio
#aqui vamos criar nosso sv local com a chave para o sistema roda
app = Flask(__name__)
app.secret_key = "consorcio"
sistema = SistemaConsorcio()

#logo a baixo temos todas @approute e uma url que chamamos para ser executada
# Menu principal
@app.route("/")
def index():
    return render_template("menu_principal.html",estatisticas=sistema.estatisticas_sistema())
#esse render_tamplate ele carrega o arquivo html e passa dados do sistema pra ele!
# Clientes
@app.route("/clientes")
def clientes():
    return render_template(
        "clientes.html",
        clientes=sistema.listar_clientes(),
        grupos=sistema.listar_grupos())
@app.route("/cadastrar_cliente", methods=["POST"])
def cadastrar_cliente():
    try:
        sistema.cadastrar_cliente(
            request.form["nome"],
            request.form["cpf"],
            request.form["telefone"],
            request.form["email"],
            int(request.form["grupo_id"]))
#esse flash é uma mensagem temporaria  que aparece para o user se der erro ele retorna o erro que deu.
        flash("✅ Cliente cadastrado com sucesso")
    except Exception as erro:
        flash(f"❌ {erro}")
#o Redirect ele manda o ussuario devolta para o arquivo base HTML no caso desse é o clientes
    return redirect("/clientes")
# Veiculos
@app.route("/veiculos")
def veiculos():

    return render_template(
        "veiculos.html",
        veiculos=sistema.listar_veiculos())
@app.route("/cadastrar_veiculo", methods=["POST"])
def cadastrar_veiculo():
    sistema.cadastrar_veiculo(
        request.form["marca"],
        request.form["modelo"],
        int(request.form["ano"]),
        float(request.form["valor"]))
    flash("✅ Veículo cadastrado com sucesso")
    return redirect("/veiculos")
# Grupos
@app.route("/grupos")
def grupos():
    return render_template(
        "grupos.html",
        grupos=sistema.listar_grupos(),
        veiculos=sistema.listar_veiculos())
@app.route("/criar_grupo", methods=["POST"])
def criar_grupo():
    sistema.criar_grupo(
        request.form["nome"],
        int(request.form["veiculo_id"]),
        int(request.form["quantidade_cotas"]),
        int(request.form["prazo_meses"]))
    flash("✅ Grupo criado com sucesso")
    return redirect("/grupos")
# Cotas
@app.route("/cotas")
def cotas():
    cotas_detalhadas = []
    for cota in sistema.listar_cotas():
        cliente = sistema.buscar_cliente(
            cota.cliente_id)
        grupo = sistema.buscar_grupo(
            cota.grupo_id)
        cotas_detalhadas.append({
            "id": cota.id,
            "numero": cota.numero,
            "cliente":
            cliente.nome if cliente
            else "Não encontrado",
            "grupo":
            grupo.nome if grupo
            else "Não encontrado",
            "parcelas":
            len(cota.parcelas),})
    return render_template(
        "cotas.html",
        clientes=sistema.listar_clientes(),
        grupos=sistema.listar_grupos(),
        cotas=cotas_detalhadas)
@app.route("/vender_cota", methods=["POST"])
def vender_cota():
    sistema.vender_cota(
        int(request.form["cliente_id"]),
        int(request.form["grupo_id"]))
    flash("✅ Cota vendida com sucesso")
    return redirect("/cotas")



# EXCLUIR CLIENTE
@app.route("/excluir_cliente/<int:id>")
def excluir_cliente(id):
    sistema.excluir_cliente(id)
    flash("🗑️ Cliente excluído com sucesso")
    return redirect("/clientes")



# EXCLUIR VEÍCULO
@app.route("/excluir_veiculo/<int:id>")
def excluir_veiculo(id):
    sistema.excluir_veiculo(id)
    flash("🗑️ Veículo excluído com sucesso")
    return redirect("/veiculos")



# EXCLUIR GRUPO
@app.route("/excluir_grupo/<int:id>")
def excluir_grupo(id):
    sistema.excluir_grupo(id)
    flash("🗑️ Grupo excluído com sucesso")
    return redirect("/grupos")



# EXCLUIR COTA
@app.route("/excluir_cota/<int:id>")
def excluir_cota(id):
    sistema.excluir_cota(id)
    flash("🗑️ Cota excluída com sucesso")
    return redirect("/cotas")

# Main
if __name__ == "__main__":
    app.run(debug=True)