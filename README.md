# OSINT
Ferramentas de Osint rescritas ou desenvolvidas do zero

## Instalação
1) ``git clone https://github.com/Pollyne/osint.git``<br/>
2) ``cd osint``<br/>
3) ``python3 -m pip install -r requirements.txt``<br/>

# DarkSearch - Buscas na deepweb em seu terminal 

## Sobre Darksearch
Darksearch é um script simples escrito em python 3 onde o usuario pode realizar querys na deepweb via terminal usando a API darksearch.io. 

Foi rescrito baseado no projeto: https://github.com/josh0xA/darkdump

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

# numberverify - Informações de um número de telefone baseado na API numberverify

## Sobre numberverify
numberverify é um script simples escrito em python 3 onde o usuario pode realizar buscas sobre um determinado numero de telefone via terminal usando a API numberverify (https://numverify.com/dashboard)

Foi rescrito baseado no projeto: https://github.com/sundowndev/phoneinfoga

## configuração de chave para API

Criar um regristro grátis no site (https://numverify.com/) em (https://numverify.com/dashboard) copiar a Chave para a API 

<p align="center">
  <img src="https://github.com/Pollyne/osint/blob/main/imagens/chave_numberverify.png?raw=true">
</p>

Colocar sua CHAVE no local indicado: (access_key="CHAVE_API_AQUI")

<p align="center">
  <img src="https://github.com/Pollyne/osint/blob/main/imagens/chave_api.png?raw=true">
</p>

## Uso 
Example 1: ``python3 numberverify.py -h``<br/>
Example 2: ``python3 numberverify.py -n +5585988405936``<br/>

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
            
usage: numberverify.py [-h] [-n number] [-o output]

optional arguments:
  -h, --help            show this help message and exit
  -n number, --number number
  -o output, --output output

```

## Visual
<p align="center">
  <img src="https://github.com/Pollyne/osint/blob/main/imagens/numberverify_output.png?raw=true">
</p>

# usernamesearch - Busca pelo username em diversos sites 

## Sobre usernamesearch
Script simples que busca pelo username em diversos sites predefinidos em resources/data.json (Lista completa em sites.md). 

Foi rescrito baseado no projeto: https://github.com/sherlock-project/sherlock

## Uso 

Example 1: ``python3 usernamesearch.py pollynezunino``<br/>
Example 2: ``python3 usernamesearch.py pollynezunino --print-all``<br/>
Example 3: ``python3 usernamesearch.py pollynezunino --version``<br/>
Example 4: ``python3 usernamesearch.py pollynezunino --verbose``<br/>
Example 5: ``python3 usernamesearch.py pollynezunino --site instagram``<br/>

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
            
usage: usernamesearch.py [-h] [--version] [--verbose] [--output OUTPUT] [--site SITE_NAME] [--print-all] [--local] USERNAMES [USERNAMES ...]

Buscando username em sites (Version 0.0.1)

positional arguments:
  USERNAMES

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --verbose, -v, -d, --debug
  --output OUTPUT, -o OUTPUT
  --site SITE_NAME
  --print-all
  --local, -l

```

## Visual
<p align="center">
  <img src="https://github.com/Pollyne/osint/blob/main/imagens/username_search.png?raw=true">
</p>

## Ethical Notice
O desenvolvedor deste programa, Pollyne Zunino, não é responsável pelo uso indevido desta ferramenta de coleta de dados. Não use o darksearch para navegar em sites que participam de qualquer atividade identificada como ilegal de acordo com as leis e regulamentos de seu governo.

## License 
MIT License<br/>
Copyright (c) Pollyne Zunino

