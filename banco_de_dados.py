import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='92147124Joao!#$',

      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `movieverse`;")

cursor.execute("CREATE DATABASE `movieverse`;")

cursor.execute("USE `movieverse`;")

# criando tabelas
TABLES = {}
TABLES['movieverse'] = ('''
      CREATE TABLE `filmes` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `titulo` varchar(50) NOT NULL,
      `anoDeLancamento` int(4) NOT NULL,
      `genero` varchar(20) NOT NULL,
      `descricao` varchar(600) NOT NULL,

      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo jogos
filmes_sql = 'INSERT INTO filmes (titulo, anoDeLancamento, genero, descricao) VALUES (%s, %s, %s, %s)'
filmes = [
      ('Homem de Ferro', 2008, 'Ação', 'Tony Stark é um industrial bilionário e inventor brilhante que realiza testes bélicos no exterior, mas é sequestrado por terroristas que o forçam a construir uma arma devastadora. Em vez disso, ele constrói uma armadura blindada e enfrenta seus sequestradores. Quando volta aos Estados Unidos, Stark aprimora a armadura e a utiliza para combater o crime.'),
      ('Homem de Ferro 2', 2010, 'Ação', 'Em um mundo ciente da existência do Homem de Ferro, o inventor bilionário Tony Stark sofre pressão de todos os lados para compartilhar sua tecnologia com as forças armadas. Ele resiste para divulgar os segredos de sua inigualável armadura, com medo de que estas informações caiam nas mãos erradas'),
      ('Homem de Ferro 3', 2013, 'Ação', 'Depois de um inimigo reduzir o mundo de Tony Stark a destroços, o Homem de Ferro precisa aprender a confiar em seus instintos para proteger aqueles que ama, especialmente sua namorada, e lutar contra seu maior medo: o fracasso.'),

]
cursor.executemany(filmes_sql, filmes)

cursor.execute('select * from MovieVerse.filmes')
print(' -------------  Filmes:  -------------')
for filme in cursor.fetchall():
    print(filme[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()