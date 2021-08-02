class Banner(object):
    def LoadBanner(self):
        try:
            from termcolor import cprint
            banner = '''
        Developed By: Pollyne Zunino
        https://github.com/Pollyne/osint      
            '''
            cprint(banner, 'green', attrs=['bold'])

        except ImportError as ie:
            print(banner)