from pathlib import Path

import click

from src.cryptography.rsa import RSA

START = 0
STOP = 100
STEP = 1


@click.group()
def main():
    """
    Ponto de entrada da aplicação

    :return: None
    """
    pass


@main.command(help="Cria uma chave de criptografia")
@click.argument('PRIVATE_KEY', type=click.Path(exists=False, path_type=Path, file_okay=True, dir_okay=False))
@click.argument('PUBLIC_KEY', type=click.Path(exists=False, path_type=Path, file_okay=True, dir_okay=False))
@click.option('--start', type=click.INT, default=START, help="Início do intervalo a partir do qual a chave vai ser gerada")
@click.option('--stop', type=click.INT, default=STOP, help="Fim do intervalo a partir do qual a chave vai ser gerada")
@click.option('--step', type=click.INT, default=STEP, help="Passo do intervalo")
@click.option("--force", is_flag=True, default=False, )
def create(private_key: Path, public_key: Path, start: int, stop: int, step: int, force: bool) -> int:
    """
    :param private_key: O caminho do arquivo onde a chave privada será armazenada.
    :param public_key: o caminho do arquivo onde a chave pública será armazenada.
    :param start: o início do intervalo para gerar a chave.
    :param stop: o final do intervalo para gerar a chave.
    :param step: o valor da etapa para o intervalo.
    :param force: Se for True, substitua as chaves existentes.
    :return: 1 se uma chave já existir e force for False, caso contrário, 0.
    """
    rsa = RSA.with_random_prime_numbers(start, stop, step)
    if private_key.exists() and not force:
        click.echo(f"Uma chave privada já existe em {private_key}")
        return 1

    if public_key.exists() and not force:
        click.echo(f"Uma chave publica já existe em {public_key}")
        return 1

    with open(private_key, 'w') as private_key_file:
        private_key_file.write(f"{rsa.n} {rsa.private_key}")

    click.echo(f'Chave privada criada com sucesso e armazenada em: {private_key}. Não compartilhe com ninguém!')

    with open(public_key, 'w') as public_key_file:
        public_key_file.write(f"{rsa.n} {rsa.public_key}")

    click.echo(f'Chave publica criada com sucesso e armazenada em: {public_key}')


@main.group(help="Criptografa o conteúdo usando a chave pública")
def encrypt():
    """
    Criptografa o conteúdo usando a chave pública.

    :return: Nenhum
    """
    pass


@encrypt.command(help="Criptografa um texto")
@click.argument("CONTENT", type=click.STRING)
@click.argument("PUBLIC_KEY", type=click.Path(exists=True, path_type=Path, file_okay=True, dir_okay=False))
def text(content: str, public_key: Path):
    """
    Criptografa um texto usando criptografia RSA.

    :param content: o texto a ser criptografado.
    :param public_key: o caminho para o arquivo de chave pública.
    :return: o texto criptografado.
    """
    file_content = open(public_key, 'r').read()
    n = int(file_content.split(" ")[0])
    key = int(file_content.split(" ")[1])

    ciphered = RSA.encrypt_with(n, key, content)

    click.echo(ciphered)


@encrypt.command(help="Criptografa um arquivo")
@click.argument('INPUT_FILE', type=click.Path(path_type=Path, exists=True, file_okay=True, dir_okay=False))
@click.argument('OUTPUT', type=click.Path(path_type=Path, file_okay=True, dir_okay=False, exists=False))
@click.argument("PUBLIC_KEY", type=click.Path(exists=True, path_type=Path, file_okay=True, dir_okay=False))
def file(input_file: Path, output: Path, public_key: Path):
    """
    :param input_file: Caminho para o arquivo de entrada que precisa ser criptografado.
    :param output: caminho para o arquivo de saída em que os dados criptografados serão armazenados.
    :param public_key: Caminho para o arquivo que contém a chave pública usada para criptografia.
    :return: Nenhum
    """
    source = open(input_file, 'r').read()

    file_content = open(public_key, 'r').read()
    n = int(file_content.split(" ")[0])
    key = int(file_content.split(" ")[1])

    cyphered = RSA.encrypt_with(n, key, source)
    with open(output, 'w') as f:
        f.write(cyphered)

    click.echo(f"Arquivo encriptado com sucesso! O arquivo encriptado está em: {output}")


@main.group(help="Desencripta usando a chave de criptografia privada")
def decrypt():
    """
    Descriptografa usando a chave de criptografia privada.

    :return: os dados descriptografados.
    """
    pass


@decrypt.command(help="Desencipta um texto")
@click.argument("CONTENT", type=click.STRING)
@click.argument("PRIVATE_KEY", type=click.Path(exists=True, path_type=Path, file_okay=True, dir_okay=False))
def text(content: str, private_key: Path):
    """
    Desencripta um texto.

    :param content: O texto a ser desencriptado.
    :param private_key: O caminho para o arquivo da chave privada.
    :type content: str
    :type private_key: Path
    :return: None
    """
    file_content = open(private_key, 'r').read()
    n = int(file_content.split(" ")[0])
    key = int(file_content.split(" ")[1])

    decrypted = RSA.decrypt_with(n, key, content)

    click.echo(decrypted)


@decrypt.command(help="Desencripta um arquivo")
@click.argument('INPUT_FILE', type=click.Path(path_type=Path, exists=True, file_okay=True, dir_okay=False))
@click.argument('OUTPUT', type=click.Path(path_type=Path, file_okay=True, dir_okay=False, exists=False))
@click.argument("PRIVATE_KEY", type=click.Path(exists=True, path_type=Path, file_okay=True, dir_okay=False))
@click.option("--force", is_flag=True, default=False, help="Forca a sobrescrita das chaves")
def file(input_file: Path, output: Path, private_key: Path, force: bool):
    """
    :param input_file: caminho para o arquivo de entrada que precisa ser descriptografado.
    :param output: Caminho para o arquivo de saída em que o conteúdo descriptografado será salvo.
    :param private_key: Caminho para o arquivo que contém a chave privada usada para descriptografia.
    :param force: um sinalizador booleano que indica se o arquivo de saída deve ser substituído por força, caso ele já exista.
    :return: Nenhum
    """
    source = open(input_file, 'r').read()

    file_content = open(private_key, 'r').read()
    n = int(file_content.split(" ")[0])
    key = int(file_content.split(" ")[1])

    cyphered = RSA.decrypt_with(n, key, source)
    if not output.exists() or force:
        with open(output, 'w') as f:
            f.write(cyphered)

    click.echo(f"Arquivo desencriptado com sucesso! O arquivo encriptado está em: {output}")


if __name__ == '__main__':
    main()
