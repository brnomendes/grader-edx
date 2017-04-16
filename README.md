# Avaliador Externo - Open edX

Requisitos: Python 3.6+, Pip 9+, Mysql 5.7+, [edX com XQueue](http://edx.readthedocs.io/projects/edx-installing-configuring-and-running/en/latest/installation/fullstack/install_fullstack.html)

Referência: [External Grader](http://edx.readthedocs.io/projects/edx-partner-course-staff/en/latest/exercises_tools/external_graders.html)

### Configuração XQueue
```bash
$ vagrant up # Inicar o edX Fullstack
$ vagrant ssh # Acessar o ambiente com edX
$ sudo -H -u xqueue vim /edx/app/xqueue/xqueue.env.json # Editar o Json de Configuração
```
No arquivo xqueue.env.json deve ser adicionado o nome da fila, por exemplo py-queue, e o endereço:
```
  "XQUEUES": {
      ...
      "py-queue": "http://10.0.2.2:1710",
  },
```
*Necessário reniciar a máquina edX após a mudança.

### Configuração e Execução do Avaliador
Opcionalmente pode ser criado um ambiente virtual Python para isolar as dependências:
```bash
$ sudo pip install virtualenv
$ virtualenv -p python3 venv # Criar o Ambiente Virtual venv
$ . venv/bin/activate # Utilizar o Ambiente Virtual venv
```
**Instalar as dependências**:
```bash
$ git clone https://github.com/brnomendes/grader-edx.git
$ cd grader-edx/
$ pip install -r requirements.txt
```

**Configurando Banco de Dados**:

Variáveis de ambiente a serem configuradas: GRADER_HOST, GRADER_USER, GRADER_PASSWORD

```bash
$ mysql -u USER -p < database.sql
```

**Iniciando o Avaliador**:
```bash
$ python3 main.py
```

### Criando Exercício para o Avaliador Externo
Exemplo de exercício. Deve ser indicado o nome da fila do avaliador no parâmetro queuename.
```xml
<problem>
  <text>
    <p>Create a method and test</p>
  </text>

  <coderesponse queuename="py-queue">
    <textbox mode="python" tabsize="4"/>
    <codeparam></codeparam>
  </coderesponse>
</problem>
```
