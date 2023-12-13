import socket, subprocess, requests, geoip2.database, os, time, sys
from colorama import Fore

# para resolver o bug das cores no terminal.
os.system('@chcp 65001 >nul')

# Bancos de Dados para o IPLookup
asn_db = 'geolite_dbs/GeoLite2-ASN.mmdb'
country_db = 'geolite_dbs/GeoLite2-Country.mmdb'
city_db = 'geolite_dbs/GeoLite2-City.mmdb'

def IPLookup(ip):
    # Faz a leitura dos Bancos de Dados
    read_asn = geoip2.database.Reader(asn_db)
    read_country = geoip2.database.Reader(country_db)
    read_city = geoip2.database.Reader(city_db)

    try:
        # captura as informações dos Bancos de Dados
        infos_asn = read_asn.asn(ip)
        infos_country = read_country.country(ip)
        infos_city = read_city.city(ip)
        print(f"""
        {Fore.RED}IP: {Fore.WHITE}{ip}
        {Fore.RED}Cidade: {Fore.WHITE}{infos_city.city.name}
        {Fore.RED}Estado: {Fore.WHITE}{infos_city.subdivisions.most_specific.name}
        {Fore.RED}País: {Fore.WHITE}{infos_country.country.name}
        {Fore.RED}Organização: {Fore.WHITE}{infos_asn.autonomous_system_organization}
        {Fore.RED}Latitude: {Fore.WHITE}{infos_city.location.latitude}
        {Fore.RED}Longitude: {Fore.WHITE}{infos_city.location.longitude}
        """)
    except geoip2.errors.AddressNotFoundError:
        print(f"{Fore.RED} - IP {Fore.WHITE}{ip} {Fore.RED}não encontrado nos Bancos de Dados.")

    read_asn.close()
    read_country.close()
    read_city.close()

class main:
    def __init__(self):
        try:
            os.system('cls && title OmeTV/Omegle IP Sniffer')
            print(f"""{Fore.RED}
                        ╔═╗╔╦╗╔═╗╔═╗╔╗╔╦╔═╗╔═╗╔═╗╦═╗
                        ║ ║║║║║╣ ╚═╗║║║║╠╣ ╠╣ ║╣ ╠╦╝
                        ╚═╝╩ ╩╚═╝╚═╝╝╚╝╩╚  ╚  ╚═╝╩╚═
                   Developed by 27prxblms - © AFTER DAWN ™
                         {Fore.RED}Commands{Fore.WHITE}: '{Fore.GREEN}start{Fore.WHITE}' - '{Fore.GREEN}exit{Fore.WHITE}'
            """)
            start = input(f"{Fore.RED} OmeSniffer {Fore.WHITE}>>> {Fore.GREEN}")
            if start == 'exit':
                sys.exit()
            if start == 'start':
                try:
                    wireshark = r"D:\System\Wireshark\tshark.exe -i 4"

                    process = subprocess.Popen(wireshark, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    my_ip = socket.gethostbyname(socket.gethostname())

                    ip_list = []

                    for line in iter(process.stdout.readline, b""):
                        columns = str(line).split(" ")

                        # Verifica se no processo o IP encontrado pelo wireshark é UDP ou SKYPE.
                        if "SKYPE" in columns or "UDP" in columns:
                            if "->" in columns:
                                ip = columns[columns.index("->") - 1]
                            elif "\\xe2\\x86\\x92" in columns:
                                ip = columns[columns.index("\\xe2\\x86\\x92") - 1]
                            else:
                                continue

                            if ip not in ip_list:
                                ip_list.append(ip)
                                IPLookup(ip)
                except KeyboardInterrupt:
                    print(f" Escaneamente concluído ou cancelado, retornando ao menu...")
                    time.sleep(2)
                    main()
            
            else:
                print(f" Você precisa digitar START para iniciar o escaneamento...")
                time.sleep(2)
                main()

        except KeyboardInterrupt:
            sys.exit()
                        
if __name__ == '__main__':
    main()