# OSINT
Ferramentas de Osint rescritas ou desenvolvidas do zero

## DarkSearch - Buscas na deepweb em seu terminal 

## Sobre Darksearch
Darksearch é um script simples escrito em python 3.8 onde o usuario pode realizar querys na deepweb via terminal usando a API darksearch.io. 

Foi rescrito baseado no projeto: https://github.com/josh0xA/darkdump

## Instalação
1) ``git clone https://github.com/Pollyne/osint.git``<br/>
2) ``cd osint``<br/>
3) ``python3 -m pip install -r requirements.txt``<br/>
4) ``python3 darksearch.py --help``<br/>

## Uso 
Example 1: ``python3 darksearch.py -h``<br/>
Example 2: ``python3 darksearch.py -q hackers``<br/>
Example 3: ``python3 darksearch.py -v``<br/>
Example 4: ``python3 darksearch.py -q hackers --page 2``<br/>
 - Nota: O argumento 'page' filtra as paginas de acordo com a quantidade de resultados, por default ele lista os resultados da pagina 1 <br/>

## Menu
```

        ¨ ¨ ¨ ¨ ¨ ¨ ¨▲.︵.▲
        ¨ ¨ ¨ ¨ ¨ ¨ ¨◄ƒ░░ 0 }…..︵.
        ¨ ¨ ¨ ¨ ¨ ¨◄ƒ░░░░░░ o”)
        ¨ ¨ ¨ ¨ ¨ ◄ƒ░░░(────.·^”’
        ¨ ¨ ¨ ¨ ¨ ◄ƒ░░░§ ´
        )\¨ ¨ ¨ ¨ ◄ƒ░░░░§ ¨ ¨ ¨✺✺✺
        ) \ ¨ ¨ ¨◄ƒ░░░░░§¨ ¨ ¨\|//✺
        );;\ ¨ ¨ ◄ƒ░.︵.░░░§__(((
        );;;\¨ ¨◄ƒ░(░░)\______//
        );;;;\¨◄ƒ░░░░░░__//
        );;;;;\◄ƒ░░░░░░░░§
        );;;;;;;\░░░░░░░░░(((
        Developed By: Pollyne Zunino
        https://github.com/Pollyne      
            
usage: darksearch.py [-h] [-v] [-q QUERY] [-p PAGE]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version
  -q QUERY, --query QUERY
  -p PAGE, --page PAGE

```
## Visual
<p align="center">
  <img src="https://github.com/Pollyne/osint/blob/main/imagens/darksearch_output.png?raw=true">
</p>

## Ethical Notice
O desenvolvedor deste programa, Pollyne Zunino, não é responsável pelo uso indevido desta ferramenta de coleta de dados. Não use o darksearch para navegar em sites que participam de qualquer atividade identificada como ilegal de acordo com as leis e regulamentos de seu governo.

## License 
MIT License<br/>
Copyright (c) Pollyne Zunino

