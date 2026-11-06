# Exercício Prático - Mock Object (`custom-stack`)

O projeto testa a classe `CustomStack` com 100% de cobertura de linhas e ramos e implementa `NumberAscOrder`, que ordena as dezenas da Mega-Sena armazenadas na pilha. Os testes usam tanto uma pilha real quanto um mock configurado com `pytest-mock`.

## Estrutura do projeto

```text
custom-stack/
├── src/
│   ├── __init__.py
│   ├── custom_stack_class.py       # pilha limitada e exceções
│   └── number_asc_order_class.py   # ordenação das dezenas
├── test/
│   ├── __init__.py
│   ├── custom_stack_test.py        # testes da CustomStack
│   └── number_asc_order_test.py    # testes da ordenação e do mock
├── .gitignore
├── README.md
└── requirements.txt
```

A pasta `venv/` é criada localmente durante o preparo do ambiente e está no `.gitignore`, assim como caches, resultados de cobertura e configurações locais do editor.

## Preparo do ambiente

É necessário Python 3.9 ou superior. Crie a venv na raiz do projeto, ative-a e instale as dependências do arquivo `requirements.txt`.

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

## Executar os testes e medir a cobertura

Com a venv ativada, execute na raiz do projeto:

```sh
python -m pytest test --cov=src --cov-branch --cov-fail-under=100 --cov-report=term-missing
```

Na última execução, os 18 testes passaram. O relatório marcou 100% de cobertura em `src`, com 49 instruções e 26 ramos cobertos. `--cov=src` limita a medição ao código de produção; `--cov-branch` também verifica os caminhos verdadeiro e falso das condições; e `--cov-fail-under=100` faz o comando falhar se a meta não for atingida.

Para gerar um relatório HTML:

```sh
python -m pytest test --cov=src --cov-branch --cov-report=html
```

Depois de executar o comando, abra `htmlcov/index.html` no navegador.

## Parte 1: efetividade dos testes da `CustomStack`

O teste fornecido inicialmente exercitava apenas o `push()` de um elemento e verificava `is_empty()`, `top()` e `size()`. Isso não avaliava completamente o comportamento da pilha: com um único valor, por exemplo, um `top()` que retornasse o primeiro elemento poderia passar mesmo que a ordem LIFO estivesse implementada incorretamente.

O enunciado informa que a cobertura inicial era de 79%. O teste inicial também não exercitava a remoção de elementos, o limite da pilha ou as exceções para operações inválidas. A cobertura de linhas, sozinha, pode ocultar esse problema: uma linha condicional pode ser executada sem que os dois resultados possíveis da condição sejam testados. Por isso a suíte usa cobertura de ramos.

### Defeito encontrado em `push()`

O código inicial comparava `self.size`, que é uma referência ao método, com o limite numérico da pilha:

```python
if self.size == self.limit:
```

Como o método não era chamado, a condição não detectava a pilha cheia e `StackFullException` não era lançado. A correção chama `size()`:

```python
if self.size() == self.limit:
```

Essa alteração corrige um método existente. Nenhum método foi acrescentado à classe `CustomStack`.

### Casos da pilha

Os testes verificam a pilha recém-criada, inserção e remoção em ordem LIFO, `top()`, tamanho, estado vazio, tentativa de inserir além da capacidade e as exceções de `pop()` e `top()` quando a pilha está vazia. Esses casos cobrem os caminhos verdadeiro e falso do limite e das verificações de pilha vazia.

## Parte 2: `NumberAscOrder.sort(stack)`

O uso é feito por uma instância da classe:

```python
numbers = NumberAscOrder().sort(stack)
```

O método valida o argumento e a pilha antes de ordenar:

1. Se o argumento não for uma instância de `CustomStack`, lança `TypeError`.
2. A capacidade deve ser exatamente 6; caso contrário, lança `ValueError`.
3. Uma pilha válida e vazia retorna `[]`.
4. Uma pilha parcialmente preenchida lança `ValueError` sem remover seus elementos.
5. Uma pilha preenchida deve conter seis inteiros distintos entre 1 e 60. Valores inválidos lançam `ValueError`.
6. Para um sorteio válido, o método retorna uma nova lista em ordem crescente e mantém o conteúdo e a ordem da pilha original.

O método retira os valores com `pop()`, que os entrega em ordem inversa à inserção por causa do comportamento LIFO. Em um bloco `finally`, reinsere os valores em ordem reversa à retirada, restaurando a ordem original. A validação ocorre após a restauração, portanto dezenas inválidas não deixam a pilha vazia.

## Uso do mock

O teste isolado da ordenação cria a pilha simulada com `mocker.create_autospec(CustomStack, instance=True)`. O `autospec` restringe a interface simulada à API da classe `CustomStack`, e o mock com especificação é reconhecido como uma instância dessa classe durante a verificação de tipo.

O teste define `stack.pop.side_effect` como uma sequência de seis valores. Cada chamada sucessiva a `pop()` devolve o próximo valor da sequência. Em seguida, verifica o resultado ordenado, as seis chamadas a `pop()` e os argumentos das chamadas a `push()`, que devem reconstruir a ordem original. Como o teste observa as chamadas além de configurar os retornos, o objeto atua como um mock, conforme a distinção do diagrama fornecido.

Não é necessário usar `mocker.patch`: a dependência já é recebida como argumento de `sort()`. Um teste separado usa uma `CustomStack` real para confirmar que a ordenação funciona em integração com a pilha concreta.

## Cenários cobertos para a ordenação

| Cenário | Resultado verificado |
|---|---|
| Seis dezenas fora de ordem em uma pilha real | Retorna `[1, 5, 12, 34, 42, 60]` e preserva a pilha. |
| Seis dezenas selecionadas com `random.sample` | Retorna `sorted(draw)` e preserva a pilha. |
| Pilha de capacidade 6 vazia | Retorna `[]`. |
| Seis retornos simulados de `pop()` | Ordena os valores, chama `pop()` seis vezes e restaura a ordem via `push()`. |
| Argumento que não é `CustomStack` | Lança `TypeError`. |
| Capacidade diferente de 6 | Lança `ValueError`. |
| Pilha parcialmente preenchida | Lança `ValueError` e mantém os elementos. |
| Dezena fora do intervalo (0 ou 61) | Lança `ValueError` e mantém os elementos. |
| Dezena repetida | Lança `ValueError` e mantém os elementos. |
| Valor que não é inteiro (`True`, `5.0` ou `"5"`) | Lança `ValueError` e mantém os elementos. |

O caso fixo fora de ordem garante que o teste detecte uma implementação que apenas devolva os valores recebidos. O teste com mock isola a lógica de `NumberAscOrder`; os testes da `CustomStack` cobrem separadamente o comportamento real da pilha.
