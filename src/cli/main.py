from pathlib import Path

import click
from twisted.internet import stdio
from twisted.internet import reactor

from src.chat.chat import ChatFactory
from src.chat.stdio import StdioInput
from src.cryptography.rsa import RSA
from src.daemon.service_discover import ServiceDiscovery
from rich.console import Console

START = 0
STOP = 100
STEP = 1

console = Console()

@click.group()
def main():
    pass


@main.command()
@click.argument('PRIVATE_KEY', type=click.Path(exists=False, path_type=Path, file_okay=True, dir_okay=False))
@click.argument('PUBLIC_KEY', type=click.Path(exists=False, path_type=Path, file_okay=True, dir_okay=False))
@click.option('--start', type=click.INT, default=START)
@click.option('--stop', type=click.INT, default=STOP)
@click.option('--step', type=click.INT, default=STEP)
@click.option("--force", is_flag=True, default=False, )
def create(private_key: Path, public_key: Path, start: int, stop: int, step: int, force: bool) -> int:
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


@main.group()
def encrypt():
    pass


@encrypt.command()
@click.argument("CONTENT", type=click.STRING)
@click.argument("PUBLIC_KEY", type=click.Path(exists=True, path_type=Path, file_okay=True, dir_okay=False))
def text(content: str, public_key: Path):
    file_content = open(public_key, 'r').read()
    n = int(file_content.split(" ")[0])
    key = int(file_content.split(" ")[1])

    ciphered = RSA.encrypt_with(n, key, content)

    click.echo(f"A mensagem foi encriptada com sucesso: {ciphered}")


@encrypt.command()
@click.argument('INPUT_FILE', type=click.Path(path_type=Path, exists=True, file_okay=True, dir_okay=False))
@click.argument('OUTPUT', type=click.Path(path_type=Path, file_okay=True, dir_okay=False, exists=False))
@click.argument("PUBLIC_KEY", type=click.Path(exists=True, path_type=Path, file_okay=True, dir_okay=False))
def file(input_file: Path, output: Path, public_key: Path):
    source = open(input_file, 'r').read()

    file_content = open(public_key, 'r').read()
    n = int(file_content.split(" ")[0])
    key = int(file_content.split(" ")[1])

    cyphered = RSA.encrypt_with(n, key, source)
    with open(output, 'w') as f:
        f.write(cyphered)

    click.echo(f"Arquivo encriptado com sucesso! O arquivo encriptado está em: {output}")


@main.group()
def decrypt():
    pass


@decrypt.command()
@click.argument("CONTENT", type=click.STRING)
@click.argument("PRIVATE_KEY", type=click.Path(exists=True, path_type=Path, file_okay=True, dir_okay=False))
def text(content: str, private_key: Path):
    file_content = open(private_key, 'r').read()
    n = int(file_content.split(" ")[0])
    key = int(file_content.split(" ")[1])

    decrypted = RSA.decrypt_with(n, key, content)

    click.echo(f"A mensagem foi desencriptada com sucesso: {decrypted}")


@decrypt.command()
@click.argument('INPUT_FILE', type=click.Path(path_type=Path, exists=True, file_okay=True, dir_okay=False))
@click.argument('OUTPUT', type=click.Path(path_type=Path, file_okay=True, dir_okay=False, exists=False))
@click.argument("PRIVATE_KEY", type=click.Path(exists=True, path_type=Path, file_okay=True, dir_okay=False))
@click.option("--force", is_flag=True, default=False)
def file(input_file: Path, output: Path, private_key: Path, force: bool):
    source = open(input_file, 'r').read()

    file_content = open(private_key, 'r').read()
    n = int(file_content.split(" ")[0])
    key = int(file_content.split(" ")[1])

    cyphered = RSA.decrypt_with(n, key, source)
    if not output.exists() or force:
        with open(output, 'w') as f:
            f.write(cyphered)

    click.echo(f"Arquivo desencriptado com sucesso! O arquivo encriptado está em: {output}")


@main.command()
@click.option('--name', prompt='Enter your name', help='Your chat name.')
@click.option('--port', default=12345, help='Port to listen on.')
@click.option('--start', type=int, default=1000, help='Start range for prime numbers.')
@click.option('--stop', type=int, default=5000, help='Stop range for prime numbers.')
@click.option('--step', type=int, default=1, help='Step for prime numbers.')
def start(name, port, start, stop, step):
    rsa = RSA.with_random_prime_numbers(start, stop, step)
    service_discovery = ServiceDiscovery('_chat._tcp.local.')

    service_discovery.register_service(name, port)
    service_discovery.start_discovery()

    factory = ChatFactory(rsa)
    reactor.listenTCP(port, factory)
    console.print(f"Server started on port {port} with name {name}")
    console.print(f"Public key: {rsa.public_key}, n: {rsa.n}")

    stdio.StandardIO(StdioInput(factory.buildProtocol(None)))
    reactor.run()

    service_discovery.unregister_service(name)
    service_discovery.close()


if __name__ == '__main__':
    main()
