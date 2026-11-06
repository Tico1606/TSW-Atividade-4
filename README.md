# CustomStack e ordenação da Mega-Sena

Projeto de exercício em Python com uma pilha de tamanho limitado e a classe `NumberAscOrder`, que ordena as seis dezenas de um sorteio da Mega-Sena.

## Requisitos

- Python 3.9 ou superior

## Preparar o ambiente

Crie e ative uma venv na raiz do projeto e instale as dependências:

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Linux/macOS

```sh
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Executar os testes

Com a venv ativada, execute:

```sh
python -m pytest test --cov=src --cov-branch --cov-fail-under=100 --cov-report=term-missing
```

## Ordenar um sorteio

`NumberAscOrder.sort(stack)` recebe uma `CustomStack` com capacidade 6. Para uma pilha vazia, retorna `[]`. Para uma pilha preenchida, exige seis inteiros distintos entre 1 e 60 e retorna as dezenas em ordem crescente, preservando a pilha.
