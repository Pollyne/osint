import os
import platform
import re
import sys
import json
import requests
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from time import monotonic
from requests_futures.sessions import FuturesSession
from colorama import Fore, Style, init
from enum import Enum
from banner.banner import Banner


module_name = "Buscando username em sites"
__version__ = "1.0.0"

class FindUsernameFuturesSession(FuturesSession):
    def request(self, method, url, hooks={}, *args, **kwargs):
        start = monotonic()

        def response_time(resp, *args, **kwargs):
            resp.elapsed = monotonic() - start

            return

        try:
            if isinstance(hooks['response'], list):
                hooks['response'].insert(0, response_time)
            elif isinstance(hooks['response'], tuple):
                hooks['response'] = list(hooks['response'])
                hooks['response'].insert(0, response_time)
            else:
                hooks['response'] = [response_time, hooks['response']]
        except KeyError:
            hooks['response'] = [response_time]

        return super(FindUsernameFuturesSession, self).request(method,
                                                           url,
                                                           hooks=hooks,
                                                           *args, **kwargs)

def get_response(request_future, error_type, social_network):

    response = None

    error_context = "Erro Geral Desconhecido"
    expection_text = None
    try:
        response = request_future.result()
        if response.status_code:
            error_context = None
    except requests.exceptions.HTTPError as errh:
        error_context = "HTTP Error"
        expection_text = str(errh)
    except requests.exceptions.ProxyError as errp:
        error_context = "Proxy Error"
        expection_text = str(errp)
    except requests.exceptions.ConnectionError as errc:
        error_context = "Error Connecting"
        expection_text = str(errc)
    except requests.exceptions.Timeout as errt:
        error_context = "Timeout Error"
        expection_text = str(errt)
    except requests.exceptions.RequestException as err:
        error_context = "Unknown Error"
        expection_text = str(err)

    return response, error_context, expection_text


def findUsername(username, site_data, query_notify,
             proxy=None, timeout=None):

    query_notify.start(username)

    if proxy:
        underlying_session = requests.session()
        underlying_request = requests.Request()
    else:
        underlying_session = requests.session()
        underlying_request = requests.Request()

    if len(site_data) >= 20:
        max_workers=20
    else:
        max_workers=len(site_data)

    session = FindUsernameFuturesSession(max_workers=max_workers,
                                     session=underlying_session)
    results_total = {}

    for social_network, net_info in site_data.items():

        results_site = {}
        results_site['url_main'] = net_info.get("urlMain")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }

        if "headers" in net_info:
            headers.update(net_info["headers"])
        url = net_info["url"].format(username)

        regex_check = net_info.get("regexCheck")
        if regex_check and re.search(regex_check, username) is None:
            results_site['status'] = QueryResult(username,
                                                 social_network,
                                                 url,
                                                 QueryStatus.ILLEGAL)
            results_site["url_user"] = ""
            results_site['http_status'] = ""
            results_site['response_text'] = ""
            query_notify.update(results_site['status'])
        else:
            results_site["url_user"] = url
            url_probe = net_info.get("urlProbe")
            if url_probe is None:
                url_probe = url
            else:
                url_probe = url_probe.format(username)

            if (net_info["errorType"] == 'status_code' and
                net_info.get("request_head_only", True) == True):
                request_method = session.head
            else:
                request_method = session.get

            if net_info["errorType"] == "response_url":
                allow_redirects = False
            else:
                allow_redirects = True

            if proxy is not None:
                proxies = {"http": proxy, "https": proxy}
                future = request_method(url=url_probe, headers=headers,
                                        proxies=proxies,
                                        allow_redirects=allow_redirects,
                                        timeout=timeout
                                        )
            else:
                future = request_method(url=url_probe, headers=headers,
                                        allow_redirects=allow_redirects,
                                        timeout=timeout
                                        )

            net_info["request_future"] = future

        results_total[social_network] = results_site

    for social_network, net_info in site_data.items():
    
        results_site = results_total.get(social_network)
        url = results_site.get("url_user")
        status = results_site.get("status")

        if status is not None:
            continue

        error_type = net_info["errorType"]
        future = net_info["request_future"]
        r, error_text, expection_text = get_response(request_future=future,
                                                     error_type=error_type,
                                                     social_network=social_network)

        try:
            response_time = r.elapsed
        except AttributeError:
            response_time = None

        try:
            http_status = r.status_code
        except:
            http_status = "?"
        try:
            response_text = r.text.encode(r.encoding)
        except:
            response_text = ""

        if error_text is not None:
            result = QueryResult(username,
                                 social_network,
                                 url,
                                 QueryStatus.UNKNOWN,
                                 query_time=response_time,
                                 context=error_text)
        elif error_type == "message":
            error_flag = True
            errors=net_info.get("errorMsg")
            if isinstance(errors,str):
                if errors in r.text:
                    error_flag = False
            else:
                for error in errors:
                    if error in r.text:
                        error_flag = False
                        break
            if error_flag:
                result = QueryResult(username,
                                     social_network,
                                     url,
                                     QueryStatus.CLAIMED,
                                     query_time=response_time)
            else:
                result = QueryResult(username,
                                     social_network,
                                     url,
                                     QueryStatus.AVAILABLE,
                                     query_time=response_time)
        elif error_type == "status_code":
            if not r.status_code >= 300 or r.status_code < 200:
                result = QueryResult(username,
                                     social_network,
                                     url,
                                     QueryStatus.CLAIMED,
                                     query_time=response_time)
            else:
                result = QueryResult(username,
                                     social_network,
                                     url,
                                     QueryStatus.AVAILABLE,
                                     query_time=response_time)
        elif error_type == "response_url":
            if 200 <= r.status_code < 300:
                result = QueryResult(username,
                                     social_network,
                                     url,
                                     QueryStatus.CLAIMED,
                                     query_time=response_time)
            else:
                result = QueryResult(username,
                                     social_network,
                                     url,
                                     QueryStatus.AVAILABLE,
                                     query_time=response_time)
        else:
            raise ValueError(f"Unknown Error Type '{error_type}' for "
                             f"site '{social_network}'")

        query_notify.update(result)
        results_site['status'] = result
        results_site['http_status'] = http_status
        results_site['response_text'] = response_text
        results_total[social_network] = results_site

    query_notify.finish()

    return results_total


def timeout_check(value):

    from argparse import ArgumentTypeError

    try:
        timeout = float(value)
    except:
        raise ArgumentTypeError(f"Timeout '{value}' must be a number.")
    if timeout <= 0:
        raise ArgumentTypeError(f"Timeout '{value}' must be greater than 0.0s.")
    return timeout

# notify --- inicio -----
class QueryNotify():
    def __init__(self, result=None):
        self.result = result
        return

    def start(self, message=None):
        return

    def update(self, result):
        self.result = result
        return

    def finish(self, message=None):
        return

    def __str__(self):
        result = str(self.result)
        return result


class QueryNotifyPrint(QueryNotify):
    def __init__(self, result=None, verbose=False, color=True, print_all=False):

        init(autoreset=True)

        super().__init__(result)
        self.verbose = verbose
        self.print_all = print_all
        self.color = color

        return

    def start(self, message):
        title = "Checando username"
        if self.color:
            print(Style.BRIGHT + Fore.GREEN + "[" +
                Fore.YELLOW + "*" +
                Fore.GREEN + f"] {title}" +
                Fore.WHITE + f" {message}" +
                Fore.GREEN + " on:")
        else:
            print(f"[*] {title} {message} on:")

        return

    def update(self, result):
        self.result = result

        if self.verbose == False or self.result.query_time is None:
            response_time_text = ""
        else:
            response_time_text = f" [{round(self.result.query_time * 1000)} ms]"

        if result.status == QueryStatus.CLAIMED:
            if self.color:
                print((Style.BRIGHT + Fore.WHITE + "[" +
                       Fore.GREEN + "+" +
                       Fore.WHITE + "]" +
                       response_time_text +
                       Fore.GREEN +
                       f" {self.result.site_name}: " +
                       Style.RESET_ALL +
                       f"{self.result.site_url_user}"))
            else:
                print(f"[+]{response_time_text} {self.result.site_name}: {self.result.site_url_user}")

        elif result.status == QueryStatus.AVAILABLE:
            if self.print_all:
                if self.color:
                    print((Style.BRIGHT + Fore.WHITE + "[" +
                        Fore.RED + "-" +
                        Fore.WHITE + "]" +
                        response_time_text +
                        Fore.GREEN + f" {self.result.site_name}:" +
                        Fore.YELLOW + " Not Found!"))
                else:
                    print(f"[-]{response_time_text} {self.result.site_name}: Not Found!")

        elif result.status == QueryStatus.UNKNOWN:
            if self.print_all:
                if self.color:
                    print(Style.BRIGHT + Fore.WHITE + "[" +
                          Fore.RED + "-" +
                          Fore.WHITE + "]" +
                          Fore.GREEN + f" {self.result.site_name}:" +
                          Fore.RED + f" {self.result.context}" +
                          Fore.YELLOW + f" ")
                else:
                    print(f"[-] {self.result.site_name}: {self.result.context} ")

        elif result.status == QueryStatus.ILLEGAL:
            if self.print_all:
                msg = "Illegal Username Format For This Site!"
                if self.color:
                    print((Style.BRIGHT + Fore.WHITE + "[" +
                           Fore.RED + "-" +
                           Fore.WHITE + "]" +
                           Fore.GREEN + f" {self.result.site_name}:" +
                           Fore.YELLOW + f" {msg}"))
                else:
                    print(f"[-] {self.result.site_name} {msg}")

        else:
            raise ValueError(f"Status de consulta desconhecido '{str(result.status)}' para o "
                             f"site '{self.result.site_name}'")
        return

    def __str__(self):
        result = str(self.result)
        return result
# notify --- Fim -----

# result --- inicio -----
class QueryStatus(Enum):
    CLAIMED   = "Claimed"
    AVAILABLE = "Available"
    UNKNOWN   = "Unknown"
    ILLEGAL   = "Illegal"

    def __str__(self):
        return self.value

class QueryResult():
    def __init__(self, username, site_name, site_url_user, status,
                 query_time=None, context=None):
        self.username      = username
        self.site_name     = site_name
        self.site_url_user = site_url_user
        self.status        = status
        self.query_time    = query_time
        self.context       = context
        return

    def __str__(self):
        status = str(self.status)
        if self.context is not None:
            status += f" ({self.context})"
        return status
# result --- Fim -----

# Sites --- inicio -----
class SiteInformation():
    def __init__(self, name, url_home, url_username_format, username_claimed,
                 username_unclaimed, information):

        self.name                = name
        self.url_home            = url_home
        self.url_username_format = url_username_format

        self.username_claimed    = username_claimed
        self.username_unclaimed  = username_unclaimed
        self.information         = information

        return

    def __str__(self):
        return f"{self.name} ({self.url_home})"

class SitesInformation():
    def __init__(self, data_file_path=None):
        if data_file_path is None:
            data_file_path = 'resources/data.json'

        if not data_file_path.lower().endswith(".json"):
            raise FileNotFoundError(f"Extensão de arquivo JSON incorreta para arquivo de dados '{data_file_path}'.")

        if "http://"  == data_file_path[:7].lower() or "https://" == data_file_path[:8].lower():
            try:
                response = requests.get(url=data_file_path)
            except Exception as error:
                raise FileNotFoundError(f"Problema ao tentar acessar "
                                        f"URL do arquivo de dados '{data_file_path}':  "
                                        f"{str(error)}"
                                       )
            if response.status_code == 200:
                try:
                    site_data = response.json()
                except Exception as error:
                    raise ValueError(f"Problema ao analisar o conteúdo json em "
                                     f"'{data_file_path}':  {str(error)}."
                                    )
            else:
                raise FileNotFoundError(f"Resposta ruim ao acessar "
                                        f"URL do arquivo de dados '{data_file_path}'."
                                       )
        else:
            try:
                with open(data_file_path, "r", encoding="utf-8") as file:
                    try:
                        site_data = json.load(file)
                    except Exception as error:
                        raise ValueError(f"Problema ao analisar o conteúdo json em "
                                         f"'{data_file_path}':  {str(error)}."
                                        )
            except FileNotFoundError as error:
                raise FileNotFoundError(f"Problema ao tentar acessar "
                                        f"arquivo de dados '{data_file_path}'."
                                       )
        self.sites = {}

        for site_name in site_data:
            try:

                self.sites[site_name] = \
                    SiteInformation(site_name,
                                    site_data[site_name]["urlMain"],
                                    site_data[site_name]["url"],
                                    site_data[site_name]["username_claimed"],
                                    site_data[site_name]["username_unclaimed"],
                                    site_data[site_name]
                                   )
            except KeyError as error:
                raise ValueError(f"Problema ao analisar o conteúdo json em "
                                 f"'{data_file_path}':  "
                                 f"Atributo ausente {str(error)}."
                                )
        return

    def site_name_list(self):
        site_names = sorted([site.name for site in self], key=str.lower)
        return site_names

    def __iter__(self):
        for site_name in self.sites:
            yield self.sites[site_name]

    def __len__(self):
        return len(self.sites)
# Sites --- Fim -----

def main():
    bn = Banner()
    bn.LoadBanner()
    version_string = f"%(prog)s {__version__}\n" +  \
                     f"{requests.__description__}:  {requests.__version__}\n" + \
                     f"Python:  {platform.python_version()}"

    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=f"{module_name} (Version {__version__})"
                            )
    parser.add_argument("--version", action="version",  version=version_string)
    parser.add_argument("--verbose", "-v", "-d", "--debug", action="store_true",  dest="verbose", default=False)
    parser.add_argument("--output", "-o", dest="output")
    parser.add_argument("--site", action="append", metavar='SITE_NAME', dest="site_list", default=None)
    parser.add_argument("--print-all", action="store_true", dest="print_all")
    parser.add_argument("username", nargs='+', metavar='USERNAMES', action="store")
    parser.add_argument("--local", "-l", action="store_true", default=False)
    args = parser.parse_args()

    if args.output is not None:
        print("You can only use one of the output methods.")
        sys.exit(1)

    if args.output is not None and len(args.username) != 1:
        print("You can only use --output with a single username")
        sys.exit(1)

    try:
        if args.local:
            sites = SitesInformation(os.path.join(os.path.dirname(__file__), 'resources/data.json'))
        else:
            sites = SitesInformation(os.path.join(os.path.dirname(__file__), 'resources/data.json'))
    except Exception as error:
        print(f"ERROR:  {error}")
        sys.exit(1)

    site_data_all = {}
    for site in sites:
        site_data_all[site.name] = site.information

    if args.site_list is None:

        site_data = site_data_all
    else:

        site_data = {}
        site_missing = []
        for site in args.site_list:
            counter = 0
            for existing_site in site_data_all:
                if site.lower() == existing_site.lower():
                    site_data[existing_site] = site_data_all[existing_site]
                    counter += 1
            if counter == 0:

                site_missing.append(f"'{site}'")

        if site_missing:
            print(f"Erro: sites desejados não encontrados: {', '.join(site_missing)}.")

        if not site_data:
            sys.exit(1)

    query_notify = QueryNotifyPrint(result=None,
                                    verbose=args.verbose,
                                    print_all=args.print_all)

    for username in args.username:
        results = findUsername(username,
                           site_data,
                           query_notify)

        if args.output:
            result_file = args.output
        else:
            result_file = f"{username}.txt"

        with open(result_file, "w", encoding="utf-8") as file:
            exists_counter = 0
            for website_name in results:
                dictionary = results[website_name]
                if dictionary.get("status").status == QueryStatus.CLAIMED:
                    exists_counter += 1
                    file.write(dictionary["url_user"] + "\n")
            file.write(f"Total de usernames de sites detectados em : {exists_counter}\n")
        print()

if __name__ == "__main__":
    main()
    major = sys.version_info[0]
    minor = sys.version_info[1]
    
    python_version = str(sys.version_info[0])+"."+str(sys.version_info[1])+"."+str(sys.version_info[2])

    if major != 3 or major == 3 and minor < 6:
        print("Requer Python 3.6+\nvocê esta usando Python %s, esta versao nao esta suportada" % (python_version))
        sys.exit(1)