import sys
from colorama import Fore, Style
import argparse
from banner.banner import Banner
import json
import re
import requests
import phonenumbers
from phonenumbers import carrier
from phonenumbers import geocoder
from phonenumbers import timezone

parser = argparse.ArgumentParser(prog='numberverify.py')
parser.add_argument('-n', '--number', metavar='number', type=str)
parser.add_argument('-o', '--output', metavar="output", type=argparse.FileType('w'))
bn = Banner()
bn.LoadBanner()
args = parser.parse_args()

scanners = ['any', 'all', 'numverify']

number = '' # Full number format
localNumber = '' # Local number format
internationalNumber = '' # International numberformat
numberCountryCode = '' # Dial code; e.g:"+33"
numberCountry = '' # Country; e.g:France

def formatNumber(InputNumber):
    return re.sub("(?:\+)?(?:[^[0-9]*)", "", InputNumber)

def localScan(InputNumber):
    global number
    global localNumber
    global internationalNumber
    global numberCountryCode
    global numberCountry

    print(code_info + 'Running local scan...')

    FormattedPhoneNumber = "+" + formatNumber(InputNumber)

    try:
        PhoneNumberObject = phonenumbers.parse(FormattedPhoneNumber, None)
    except:
        return False
    else:
        if not phonenumbers.is_valid_number(PhoneNumberObject):
            return False

        number = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.E164).replace('+', '')
        numberCountryCode = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.INTERNATIONAL).split(' ')[0]

        countryRequest = json.loads(requests.request('GET', 'https://restcountries.eu/rest/v2/callingcode/{}'.format(numberCountryCode.replace('+', ''))).content)
        numberCountry = countryRequest[0]['alpha2Code']

        localNumber = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.E164).replace(numberCountryCode, '')
        internationalNumber = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        print(code_result + 'International format: {}'.format(internationalNumber))
        print(code_result + 'Local format: 0{}'.format(localNumber))
        print(code_result + 'Country code: {}'.format(numberCountryCode))
        print(code_result + 'Location: {}'.format(geocoder.description_for_number(PhoneNumberObject, "en")))
        print(code_result + 'Carrier: {}'.format(carrier.name_for_number(PhoneNumberObject, 'en')))
        print(code_result + 'Area: {}'.format(geocoder.description_for_number(PhoneNumberObject, 'en')))
        for timezoneResult in timezone.time_zones_for_number(PhoneNumberObject):
            print(code_result + 'Timezone: {}'.format(timezoneResult))

        if phonenumbers.is_possible_number(PhoneNumberObject):
            print(code_info + 'The number is valid and possible.')
        else:
            print(code_warning + 'The number is valid but might not be possible.')

def numverifyScan():
    global number

    print('\n' + code_info + 'Running Numverify.com scan...')

    access_key="CHAVE_API_AQUI"
    response = requests.request("GET", "http://apilayer.net/api/validate?access_key={}&number={}".format(access_key, number), data="")

    if response.content == "Unauthorized" or response.status_code != 200:
        print((code_error + "An error occured while calling the API (bad request or wrong api key)."))
        return -1

    data = json.loads(response.content)

    if data["valid"] == False:
        print((code_error + "Error: Please specify a valid phone number. Example: +6464806649"))
        sys.exit()

    InternationalNumber = '({}){}'.format(data["country_prefix"], data["local_format"])

    print((code_result + "Number: ({}) {}").format(data["country_prefix"],data["local_format"]))
    print((code_result + "Country: {} ({})").format(data["country_name"],data["country_code"]))
    print((code_result + "Location: {}").format(data["location"]))
    print((code_result + "Carrier: {}").format(data["carrier"]))
    print((code_result + "Line type: {}").format(data["line_type"]))

    if data["line_type"] == 'landline':
        print((code_warning + "This is most likely a landline, but it can still be a fixed VoIP number."))
    elif data["line_type"] == 'mobile':
        print((code_warning + "This is most likely a mobile number, but it can still be a VoIP number."))

def scanNumber(InputNumber):
    print(code_title + "[!] ---- Fetching informations for {} ---- [!]".format(formatNumber(InputNumber)))

    localScan(InputNumber)

    global number
    global localNumber
    global internationalNumber
    global numberCountryCode
    global numberCountry

    if not number:
        print((code_error + "Error: number {} is not valid. Skipping.".format(formatNumber(InputNumber))))
        sys.exit()

    numverifyScan()

    print(code_info + "Scan finished.")

    print('\n' + Style.RESET_ALL)

try:
    if args.output:
        code_info = '[*] '
        code_warning = '(!) '
        code_result = '[+] '
        code_error = '[!] '
        code_title = ''

        sys.stdout = args.output
    else:
        code_info = Fore.RESET + Style.BRIGHT + '[*] '
        code_warning = Fore.YELLOW + Style.BRIGHT + '(!) '
        code_result = Fore.GREEN + Style.BRIGHT + '[+] '
        code_error = Fore.RED + Style.BRIGHT + '[!] '
        code_title = Fore.YELLOW + Style.BRIGHT

    if args.number:
        scanNumber(args.number)
        
    if args.output:
        args.output.close()
except KeyboardInterrupt:
    print(("\n" + code_error + "Scan interrupted. Good bye!"))
    sys.exit()
