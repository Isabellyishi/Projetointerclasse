from flask import Flask, render_template, request, redirect, url_for, flash, g, session
from sqlalchemy import select

from database import Time, Jogador, Partida, db_session
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/")
def dashboard():

    # Buscar todos os times no banco

    # 1- Montar o select 🤍
    times_sql = select(Time)

    # 2 - Executar o select 🤍
    times = db_session.execute(times_sql).scalars().all()



    return render_template(
        "dashboard.html",
        total_jogadores=0,
        total_times=len(times),
        total_partidas=0,
    )

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/jogadores")
def listar_jogadores():
    return render_template("jogadores.html", jogadores=[], times=[])

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    if request.method == "POST":
        nome = request.form.get("nome")
        posicao = request.form.get("posicao")
        time_id = request.form.get("time_id") or None
        numero_camisa = request.form.get("numero_camisa") or None

        if not nome:
            flash('O campo nome não pode estar vazio', 'error')
            return render_template('jogadores.html')

        if not posicao:
            flash('O campo posição não pode estar vazio', 'error')
            return render_template('jogadores.html')

        if not numero_camisa:
            flash('O campo número da camisa não pode estar vazio', 'error')
            return render_template('jogadores.html')

            # Salvar no banco

        try:
            jogador_novo = Jogador(nome=nome, posicao=posicao, numero_camisa=int(numero_camisa))
            db_session.add(jogador_novo)
            db_session.commit()
            flash('Jogador adicionado com sucesso', 'success')

        except SQLAlchemyError as e:
            db_session.rollback()
            flash('Ocorreu um erro, tente novamente', 'error')
            print(f'{e}')
        except Exception as e:
            db_session.rollback()
            flash('Ocorreu um erro, tente novamente', 'error')
            print(f'{e}')

    # Buscar todos os times no banco

    # 1- Montar o select 🤍
    times_sql = select(Time)

    # 2 - Executar o select 🤍
    times = db_session.execute(times_sql).scalars().all()

    return render_template("jogadores.html", jogadores=[], times=times)

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/times")
def listar_times():

    # Buscar todos os times no banco

    # 1- Montar o select 🤍
    times_sql = select(Time)

    # 2 - Executar o select 🤍
    times = db_session.execute(times_sql).scalars().all()

    return render_template("times.html", times=times)

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():

    if request.method == "POST":

        # Pegar os valores digitados do for

        nome = request.form.get("nome")
        responsavel = request.form.get("responsavel")
        turma = request.form.get("turma")

        # Verificar se foi digitado

        if not nome:
            flash('O campo nome não pode estar vazio', 'error')
            return render_template('times.html')

        if not turma:
            flash('O campo turma não pode estar vazio', 'error')
            return render_template('times.html')

        if not responsavel:
            flash('O campo responsável não pode estar vazio', 'error')
            return render_template('times.html')

        # Salvar no banco

        try:
            time_novo = Time(nome=nome, responsavel=responsavel, turma=turma)
            db_session.add(time_novo)
            db_session.commit()
            flash('Time adicionado com sucesso', 'success')

        except SQLAlchemyError as e:
            db_session.rollback()
            flash('Ocorreu um erro, tente novamente', 'error')
            print(f'{e}')
        except Exception as e:
            db_session.rollback()
            flash('Ocorreu um erro, tente novamente', 'error')
            print(f'{e}')

    # Buscar todos os times no banco

    # 1- Montar o select 🤍
    times_sql = select(Time)

    # 2 - Executar o select 🤍
    times = db_session.execute(times_sql).scalars().all()
    print(times)

    return render_template("times.html", times=times)

#-----------------------------------------------------------------------------------------------------------------------
@app.route("/partidas")
def listar_partidas():

    return render_template("partidas.html", partidas=[], times=[])
#-----------------------------------------------------------------------------------------------------------------------
@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():

    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        data_partida = request.form.get("data_partida", "").strip()
        gols_casa = request.form.get("gols_casa", "").strip()
        gols_visitante = request.form.get("gols_visitante", "").strip()

        if not data_partida:
            flash('O campo data de partida não pode estar vazio', 'error')
            return render_template('partidas.html')

        if not gols_casa:
            flash('O campo gols da casa não pode estar vazio', 'error')
            return render_template('partidas.html')

        if not gols_visitante:
            flash('O campo gols dos visitantes não pode estar vazio', 'error')
            return render_template('partidas.html')

        # Salvar no banco

        try:
            partida_nova = Time(data_partida=data_partida, gols_casa=gols_casa, gols_visitante=gols_visitante)
            db_session.add(partida_nova)
            db_session.commit()
            flash('Partida adicionada com sucesso', 'success')

        except SQLAlchemyError as e:
            db_session.rollback()
            flash('Ocorreu um erro, tente novamente', 'error')
            print(f'{e}')
        except Exception as e:
            db_session.rollback()
            flash('Ocorreu um erro, tente novamente', 'error')
            print(f'{e}')

    return render_template("partidas.html", partidas=[], times=[])
#-----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
