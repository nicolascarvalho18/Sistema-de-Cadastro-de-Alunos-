import sqlite3

def conectar_banco():
    conn = sqlite3.connect('cadastro_alunos.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            curso TEXT
        )
    """)
    conn.commit()
    return conn

def adicionar_aluno(conn):
    nome = input("Digite o nome do aluno: ")
    idade = input("Digite a idade do aluno: ")
    curso = input("Digite o curso do aluno: ")

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO alunos (nome, idade, curso) VALUES (?, ?, ?)
    """, (nome, idade, curso))
    conn.commit()
    print("Aluno adicionado com sucesso!\n")

def visualizar_alunos(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()
    if alunos:
        print("\n--- Lista de Alunos ---")
        print("{:<5} {:<20} {:<5} {:<20}".format('ID', 'Nome', 'Idade', 'Curso'))
        for aluno in alunos:
            print("{:<5} {:<20} {:<5} {:<20}".format(aluno[0], aluno[1], aluno[2], aluno[3]))
        print("")
    else:
        print("Nenhum aluno cadastrado.\n")

def atualizar_aluno(conn):
    visualizar_alunos(conn)
    id_aluno = input("Digite o ID do aluno que deseja atualizar: ")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alunos WHERE id = ?", (id_aluno,))
    aluno = cursor.fetchone()

    if aluno:
        print("Deixe o campo vazio para manter o valor atual.")
        novo_nome = input(f"Nome [{aluno[1]}]: ") or aluno[1]
        nova_idade = input(f"Idade [{aluno[2]}]: ") or aluno[2]
        novo_curso = input(f"Curso [{aluno[3]}]: ") or aluno[3]

        cursor.execute("""
            UPDATE alunos SET nome = ?, idade = ?, curso = ? WHERE id = ?
        """, (novo_nome, nova_idade, novo_curso, id_aluno))
        conn.commit()
        print("Aluno atualizado com sucesso!\n")
    else:
        print("Aluno não encontrado.\n")

def excluir_aluno(conn):
    visualizar_alunos(conn)
    id_aluno = input("Digite o ID do aluno que deseja excluir: ")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alunos WHERE id = ?", (id_aluno,))
    aluno = cursor.fetchone()

    if aluno:
        confirmacao = input(f"Tem certeza que deseja excluir o aluno '{aluno[1]}'? (s/n): ").lower()
        if confirmacao == 's':
            cursor.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))
            conn.commit()
            print("Aluno excluído com sucesso!\n")
        else:
            print("Operação cancelada.\n")
    else:
        print("Aluno não encontrado.\n")

def menu():
    print("===== Sistema de Cadastro de Alunos =====")
    print("1. Adicionar Aluno")
    print("2. Visualizar Alunos")
    print("3. Atualizar Aluno")
    print("4. Excluir Aluno")
    print("5. Sair")

def main():
    conn = conectar_banco()

    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_aluno(conn)
        elif opcao == '2':
            visualizar_alunos(conn)
        elif opcao == '3':
            atualizar_aluno(conn)
        elif opcao == '4':
            excluir_aluno(conn)
        elif opcao == '5':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.\n")

    conn.close()

if __name__ == "__main__":
    main()
