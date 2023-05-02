import sqlite3
from sqlite3 import Error, OperationalError
import os
from time import sleep
# from IPython import get_ipython
def exibir_cabecalho(mensagem, tipo):
    mensagem = f'Rotina de {mensagem} de dados'
    
    print('\n' + '-' * len(mensagem))
    print(mensagem)
    print('\n' + '-' * len(mensagem))
    
    if(tipo == 1):
        print('\n Insira os dados pela seguinte ordem ID, Nome, Data de Nascimento (YYYY-MM-DD) e Salário.\n')
    if(tipo == 2):
        print('\n Insira o ID que deseja mudar e insira a mudança.\n')
    if(tipo == 3):
        print('\n Insira o ID que deseja excluir.\n')
        
    id = input('ID (0 para voltar): ')
    
    return id
    

def mostrar_registro(registro):
    print('\n====================')
    print('Registro')
    print('--------')
    print('ID..:', registro[0])
    print('Nome:', registro[1])
    print('Data de Nascimento:', registro[2])
    print(f"Salário: {registro[3]}.00")
    print('====================')

def tabela_vazia(conexao):
    cursor = conexao.cursor()
    cursor.execute('SELECT count(*) FROM alunos')
    resultado = cursor.fetchall()
    cursor.close()
    # print(resultado)
    return resultado[0][0] == 0

def verificar_registro_existe(conexao, id):
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM alunos WHERE id=?', (id,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado

def pausa():
    input('\nPressione <ENTER> para continuar')

def conectarBanco():
    conexao = None
    banco = 'unoesc9.db'
    print(f'SQLite versão: {sqlite3.version}\n')
    path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(path, banco)
    print(f'Banco de dados: [{full_path}]\n')
    if not os.path.isfile(full_path):
        continuar = input(
        f'Banco de dados não encontrado, deseja criá-lo? \nSe sim, então o banco de dados será criado no diretório onde o programa está sendo executado [{os.getcwd()}]! [S/N]: ')
        
        if continuar.upper() != 'S':
            raise sqlite3.DatabaseError('Banco de dados não selecionado!')
    conexao = sqlite3.connect(full_path)
    print('BD aberto com sucesso!')
    return conexao

def criar_tabela(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                data_nascimento DATE NOT NULL DEFAULT (date_format(now(), '%Y-%m-%d')),
                salario REAL NOT NULL CHECK (salario >= 0) DEFAULT 0.00
                )
                   """)
    conexao.commit()
    if cursor:
        cursor.close()
def listar(conexao):
    if tabela_vazia(conexao):
        print('\n*** TABELA INEXISTENTE ***')
        pausa()
        return
    print('\n----------------------')
    print('Listagem dos Registros')
    print('----------------------\n')
    cursor = conexao.execute('SELECT * from alunos')
    registros = cursor.fetchall()

    for registro in registros:
        print('ID..:', registro[0])
        print('Nome:', registro[1])
        print("Data de nascimento:", registro[2])
        print(f"Salário: {registro[3]}.00")
        print('-----')

    pausa()
    cursor.close()

def incluir(conexao):
    id = exibir_cabecalho('inclusão', 1)
    if int(id) == 0:
        return
    if verificar_registro_existe(conexao, id):
        print('\nID já existe!')
        sleep(2)
    else:
        nome = input('\nNome: ')
        data_nascimento = input("Data de Nascimento: ")
        salario = input("Salário: " )
        confirma = input('\nConfirma a inclusão [S/N]? ').upper()
        if confirma == 'S':
            comando = f'INSERT INTO alunos VALUES({id}, "{nome}", "{data_nascimento}", {salario})'
            print(comando)
            cursor = conexao.cursor()
            cursor.execute(comando)
            conexao.commit()
            cursor.close()

def alterar(conexao):
    if tabela_vazia(conexao):
        print('\n*** TABELA INEXISTENTE ***')
        pausa()
        return
    id = exibir_cabecalho('alteração', 2)
    if int(id) == 0:
        return
    resultado = verificar_registro_existe(conexao, id)
    if not resultado:
        print('\nID não existe!')
        sleep(2)
    else:
        mostrar_registro(resultado)
        print('Escolha o que quer mudar!(NOME, DATA, SALARIO)')
        alter = input('').upper()
        
        if alter == 'NOME':
            nome = input('\nNome: ')
            confirma = input('\nConfirma a alteração [S/N]? ').upper()
            if confirma == 'S':
                cursor = conexao.cursor()
                cursor.execute('UPDATE alunos SET nome=?WHERE id=?', (nome, id))
                conexao.commit()
                cursor.close()
        
        if alter == 'DATA':
            data = input('\nData de Nascimento: ')
            confirma = input('\nConfirma a alteração [S/N]? ').upper()
            if confirma == 'S':
                cursor = conexao.cursor()
                cursor.execute('UPDATE alunos SET data_nascimento=?WHERE id=?', (data, id))
                conexao.commit()
                cursor.close()
                
        if alter == 'SALARIO':
            salario = input('\nSalário: ')
            confirma = input('\nConfirma a alteração [S/N]? ').upper()
            if confirma == 'S':
                cursor = conexao.cursor()
                cursor.execute('UPDATE alunos SET salario=?WHERE id=?', (salario, id))
                conexao.commit()
                cursor.close()
        else:
            print('\nIsso não está no meu Banco De Dados!!')
            print('LEIA NOVAMENTE E ATENTAMENTE!! \n')
            sleep(3)
            alterar(conexao)
            
def excluir(conexao):
    if tabela_vazia(conexao):
        print('\n*** TABELA VAZIA ***')
        pausa()
        return
    id = exibir_cabecalho('alteração', 3)
    if int(id) == 0:
        return
    resultado = verificar_registro_existe(conexao, id)
    if not resultado:
        print('\nID não existe!')
        sleep(2)
    else:
        mostrar_registro(resultado)
        confirma = input('\nConfirma a exclusão [S/N]? ').upper()
        if confirma == 'S':
            cursor = conexao.cursor()
            cursor.execute('DELETE FROM alunos WHERE id=?', (id,))
            conexao.commit()
            cursor.close()
            print(f'\n Item Excluido... {resultado}\n')
            
def buscar(conexao):
    print('\n----------------------')
    print('ESCOLHA POR QUAL TIPO DE REGISTRO DESEJA')
    print('Por ID, NOME, DATA, ou SALARIO.')
    print('----------------------\n')
    
    print('Digite 0 para voltar!')
    
    busque = input('Buscar Por: ').upper()
    
    if busque == 0:
        return menu(conexao)
    
    if tabela_vazia(conexao):
        print('\n*** TABELA INEXISTENTE ***')
        pausa()
        return

    elif busque == 'ID':
        id = input("Qual ID: ")
        cursor = conexao.cursor()
        comando = cursor.execute('SELECT * FROM alunos WHERE id=?', (id,))
        resultado = cursor.fetchone()
        if resultado:
            print(resultado)
        if not resultado:
            print('\n*********************************')
            print('Resultado não foi encontrado!')
            print('*********************************')
        conexao.commit()
        cursor.close()
        
    elif busque == 'NOME':
        nome = input("Qual NOME: ")
        cursor = conexao.cursor()
        comando = cursor.execute('SELECT * FROM alunos WHERE NOME=?', (nome,))
        resultado = cursor.fetchall()
        if resultado:
            print(resultado)
        if not resultado:
            print('\n*********************************')
            print('Resultado não foi encontrado!')
            print('*********************************')
        conexao.commit()
        cursor.close()
        
    elif busque == 'DATA':
        data = input("Qual DATA: ")
        cursor = conexao.cursor()
        comando = cursor.execute('SELECT * FROM alunos WHERE data_nascimento=?', (data,))
        resultado = cursor.fetchall()
        if resultado:
            print(resultado)
        if not resultado:
            print('\n*********************************')
            print('Resultado não foi encontrado!')
            print('*********************************')
        conexao.commit()
        cursor.close()
    
    elif busque == 'SALARIO':
        salario = input("Qual SALARIO: ")
        cursor = conexao.cursor()
        comando = cursor.execute('SELECT * FROM alunos WHERE salario=?', (salario,))
        resultado = cursor.fetchall()
        if resultado:
            print(resultado)
        if not resultado:
            print('\n*********************************')
            print('Resultado não foi encontrado!')
            print('*********************************')
        conexao.commit()
        cursor.close()

    else:
        print("\nTa Fora de Orbita Volte E REVEJA AS OPCOES ACIMA!")
        sleep(3)
        

def menu(conexao):
    opcao = 1
    while opcao != 6:
        # if 'SPY_PYTHONPATH' in os.environ:
        # get_ipython().magic('clear')
        # else:
        # os.system('cls' if os.name == 'nt' else 'clear')
        print()
        print()
        print('--------------')
        print('MENU DE OPÇÕES')
        print('--------------')
        print('1. Incluir Um Registro.')
        print('2. Alterar Um Registro.')
        print('3. Excluir Um Registro.')
        print('4. Listar Todos Os Registros.')
        print('5. Buscar Registro.')
        print('6. Sair.')
        # Tratamento de erros no caso de entrada alfanumérica no input()
        try:
            opcao = int(input('\nOpção [1-6]: '))
            print()
            print()
            
        except ValueError:
            opcao = 0
        if opcao == 1:
            incluir(conexao)
        elif opcao == 2:
            alterar(conexao)
        elif opcao == 3:
            excluir(conexao)
        elif opcao == 4:
            listar(conexao)
        elif opcao == 5:
            buscar(conexao)
        elif opcao != 6:
            print('Opção inválida, tente novamente')
            sleep(2)
            print()

    return opcao
if __name__ == '__main__':
    conn = None
    while True:
        try:
            conn = conectarBanco()
            criar_tabela(conn)
            # incluirUmRegistro(conn)
            # incluirVariosRegistros(conn)
            if menu(conn) == 6:
                break
        except OperationalError as e:
            print('Erro operacional:', e)
        except sqlite3.DatabaseError as e:
            print('Erro database:', e)
            # Não mostra o traceback
            raise SystemExit()
        except Error as e:
            print('Erro SQLite3:', e)
            # Não mostra o traceback
            raise SystemExit()
        except Exception as e:
            print('Erro durante a execução do sistema!')
            print(e)
        finally:
            if conn:
                print('Liberando a conexão...')
                conn.commit()
                conn.close()
print('Encerrando...')