# Networked KALAH

# How to use


## Server

To run the server, simply execute the file `network_kalah_server` by passing the desired port in the command line:
```bash
$ python network_kalah_server 8000
```

## Client

To create a client that can be run in a remote tournament on the server, just follow these steps:

1) Make sure the evaluation function is already implemented, for example the one given for `el caos inteligente`:
```python
def f_caos_intel(estado,jogador):
    """Quando é terminal: +100 para vitória, -100 para a derrota e 0 para o empate.
       Quando o tabuleiro é não terminal devolve 0, o que quer dizer que como o minimax baralha as acções, será random"""
    if estado.is_game_over():
        aux = estado.result()
        return aux*100 if jogador == estado.SOUTH else aux*-100
    return 0
```

2) Create a file and store in a variable an object of the JogadorAlfaBeta class (it is present in `jogador.py`, just import it). Note that the name will be used to identify the bot on the server, so try to use unique names to distinguish who won :)


```python
el_caos_int6 = JogadorAlfaBeta("El Caos Inteligente 6",6,f_caos_intel)
```

3) Just import the function  `network_kalah_client_start` from `network_kalah_client.py` and call it with the server’s IP address, port, and the player variable (you can also pass the port in the command line for easier changes):
```python
network_kalah_client_start('127.0.0.1', 25510, el_caos_int6)
```

4) Execute the Python file and wait for the result on the server:
```python
$ python network_caos_intel.py
```

The code for this example of implementing el caos intel is available in the file `network_caos_intel`


## Tips for competing against others

Use the FCUL VPN so that you are on the same network, making it easier to connect to the server running on another PC.