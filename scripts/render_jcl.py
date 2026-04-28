def ask(msg):
    return input(msg + ": ")

system_code = ask("Código do sistema (3 letras maiúsculas)").upper()
table_name = ask("Nome da tabela").upper()
db2 = ask("Subsystem DB2")

# Campos dinâmicos
columns = []
while True:
    col = ask("Nome do campo (enter para sair)")
    if not col:
        break
    tipo = ask("Tipo (CHAR, INT, etc)")
    tamanho = ask("Tamanho")
    columns.append(f"{col.upper()} {tipo.upper()}({tamanho})")

columns_sql = ",\n".join(columns)

# carregar templates
def load(path):
    with open(path) as f:
        return f.read()

ddl = load("templates/ddl.sql")
bind = load("templates/bind.jclpart")
rebuild = load("templates/rebuild.jclpart")
declgen = load("templates/declare_gen.jclpart")
main = load("templates/main.jcl")

# render simples
def render(t):
    return t.replace("{{SYSTEM_CODE}}", system_code)\
            .replace("{{TABLE_NAME}}", table_name)\
            .replace("{{DB2_SUBSYSTEM}}", db2)\
            .replace("{{COLUMNS}}", columns_sql)

ddl = render(ddl)
bind = render(bind)
rebuild = render(rebuild)
declgen = render(declgen)

final = main.replace("{{DDL_SQL}}", ddl)\
            .replace("{{BIND_STEP}}", bind)\
            .replace("{{REBUILD_STEP}}", rebuild)\
            .replace("{{DECLGEN_STEP}}", declgen)\
            .replace("{{JOB_NAME}}", f"{system_code}JOB01")\
            .replace("{{RUNLIB}}", "DSN!!0.RUNLIB.LOAD")

with open("final.jcl", "w") as f:
    f.write(final)

print("JCL gerado com sucesso: final.jcl")
