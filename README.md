# Nome do Projeto

## Sobre

Esse projeto fora feito com o intuito de implementar o funcionamento da criptografia RSA no que tange à matéria de
Matemática Discreta ministrada na UFLA no primeiro período de 2024.

Este projeto usa algoritmos de criptografia RSA. A criptografia RSA é um sistema de criptografia de dados que usa
números primos muito grandes para gerar suas chaves. Baseia-se na dificuldade de fatorar o produto de dois grandes
números primos, o "problema de fatoração de números inteiros". Chaves RSA podem ser tão grandes quanto 4096 bits.

## Configuração do Ambiente

Clone o repositório ou baixe-o na forma de um arquivo zipado.

### Criar o Ambiente Virtual (venv)

Para isolar as dependências deste projeto das suas outras instalações Python, é boa prática usar um ambiente virtual.

1. No seu terminal, navegue até a pasta onde você deseja colocar o ambiente virtual
2. Digite o comando `python3 -m venv nome_do_ambiente`
3. Para ativar o ambiente, use `source nome_do_ambiente/bin/activate` se estiver no bash
   ou `nome_do_ambiente\Scripts\activate` se estiver no cmd
4. Você saberá que o ambiente está ativo porque o nome dele aparecerá no início da linha no terminal

### Instalar Dependências

Agora, precisamos instalar todas as bibliotecas Python necessárias para este projeto. Os nomes destas bibliotecas estão
no arquivo `requirements.txt`.

No terminal, com o venv ativado, digite `pip install -r requirements.txt`.

## Como Usar

Para utilizar o projeto rode, na raiz do projeto: `python main.py --help`. Instruções adicionais quanto a uso aparecerão
na tela. Se quiseres simplificar o processo de execução, rode `pip install .` na raiz do projeto. Isso instalará o
projeto no seu ambiente python, seja ele um venv ou global. A execução será simplificada para `cryptography --help`
