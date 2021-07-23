import json

pool = list()

with open("resources/data.json", "r", encoding="utf-8") as data_file:
    data = json.load(data_file)

with open("sites.md", "w") as site_file:
    data_length = len(data)
    site_file.write(f'## Lista de Sites Suportados ({data_length} Sites no Total!)\n')

    for social_network in data:
        url_main = data.get(social_network).get("urlMain")
        pool.append((social_network, url_main))

    index = 1
    for social_network, url_main in pool:
        site_file.write(f'{index}. [{social_network}]({url_main})\n')
        index = index + 1


sorted_json_data = json.dumps(data, indent=2, sort_keys=True)

with open("resources/data.json", "w") as data_file:
    data_file.write(sorted_json_data)

print("Concluída a atualização da lista de sites com suporte!")

