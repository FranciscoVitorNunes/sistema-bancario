# Sistema Bancário (projeto de estudo em Python)

Um projeto simples de simulação de operações bancárias em terminal, criado como exercício para aprender controle de fluxo, funções e manipulação de estruturas de dados em Python.

## Recursos / funcionalidades
- Depositar
- Sacar (com limite diário de saques)
- Visualizar extrato
- Cadastrar novo usuário (com verificação de CPF)
- Criar nova conta associada a um usuário existente
- Listar contas registradas

## Requisitos
- Python 3.7+

## Como executar
1. Abra um terminal
2. Navegue até a pasta do projeto `sistema-bancario`
3. Execute:

```bash
python main.py
```

O programa abrirá um menu interativo. Digite a opção desejada e siga as instruções na tela.

## Estrutura do projeto
- `main.py` - lógica principal do programa e menu interativo
- `README.md` - este arquivo

## Notas de implementação
- Os CPFs são normalizados (apenas dígitos) ao cadastrar usuários. Antes de criar uma conta é feita a verificação se o usuário existe pelo CPF.
- O extrato é mantido em memória como uma string simples; para persistência seria necessário salvar em arquivo ou banco de dados.

## Próximos passos / melhorias sugeridas
- Persistência de dados (arquivo JSON / SQLite)
- Validação completa do CPF (algoritmo dos dígitos verificadores)
- Tratamento e mensagens de erro mais robustas para entradas inválidas
- Testes automatizados para as principais funções (sacar, depositar, criar usuário/conta)

## Licença
Este projeto é um exercício de aprendizado; sinta-se livre para usar e adaptar o código.