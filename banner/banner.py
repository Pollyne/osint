class Banner(object):
    def LoadBanner(self):
        try:
            from termcolor import cprint
            banner = '''
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
            '''
            cprint(banner, 'green', attrs=['bold'])

        except ImportError as ie:
            print(banner)