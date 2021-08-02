# OSINT
```text
Darksearch pode realizar queries na deepweb via terminal usando a API darksearch.io
Baseado no projeto: https://github.com/josh0xA/darkdump

Numberverify realiza buscas sobre um determinado numero de telefone via terminal usando a API numberverify
https://numverify.com/dashboard
Baseado no projeto: https://github.com/sundowndev/phoneinfoga

Usernamesearch busca pelo username em diversos sites predefinidos em resources/data.json (Lista completa em sites.md)
Baseado no projeto: https://github.com/sherlock-project/sherlock
```
## Instalação 

```bash
git clone https://github.com/Pollyne/osint.git
cd osint
python3 -m pip install -r requirements.txt

# Para o Numberverify é necessário configurar a API
# Crie um registro grátis no site https://numverify.com/
# Em https://numverify.com/dashboard copiar a Chave.
# No arquivo numberverify.py em access_key="CHAVE_API_AQUI" substituir pela chave.
```

<p align="center">
  <img src="https://github.com/Pollyne/osint/blob/main/imagens/chave_numberverify.png?raw=true">
</p>

<p align="center">
  <img src="https://github.com/Pollyne/osint/blob/main/imagens/chave_api.png?raw=true">
</p>

## Uso

```bash
# Darksearch
python3 darksearch.py -h
python3 darksearch.py -q hackers
python3 darksearch.py -v
python3 darksearch.py -q hackers --page 2

# O argumento 'page' filtra as paginas
# de acordo com a quantidade de resultados,
# por default ele lista os resultados da pagina 1 
```

```bash
# Numberverify
python3 numberverify.py -h
python3 numberverify.py -n +5585988405936
```

```bash
# Usernamesearch
python3 usernamesearch.py pollynezunino
python3 usernamesearch.py pollynezunino --print-all
python3 usernamesearch.py pollynezunino --version
python3 usernamesearch.py pollynezunino --verbose
python3 usernamesearch.py pollynezunino --site instagram
```

## Darksearch
<p align="center">
  <img src="https://github.com/Pollyne/osint/blob/main/imagens/darksearch_output.png?raw=true">
</p>

## Numberverify
<p align="center">
  <img src="https://github.com/Pollyne/osint/blob/main/imagens/numberverify_output.png?raw=true">
</p>

## Usernamesearch
<p align="center">
  <img src="https://github.com/Pollyne/osint/blob/main/imagens/username_search.png?raw=true">
</p>

## Aviso
O desenvolvedor deste programa, não é responsável pelo uso indevido desta ferramenta de coleta de dados. Não use o darksearch para navegar em sites que participam de qualquer atividade identificada como ilegal de acordo com as leis e regulamentos de seu governo.

## Licença
[MIT](https://choosealicense.com/licenses/mit/)
