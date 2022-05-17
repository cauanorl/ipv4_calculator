class Ipv4:
    def __init__(self, rede: str):
        self.location_network = self.valid_network(rede)
        self.network = self.f_network()
        self.cidr = self.f_cidr()
        self.sub_net_mask = self.sub_network_mask()
        self.ip_network = self.f_ip_network()
        self.broadcast = self.f_broadcast()

    def binary(self) -> str:
        rede = self.location_network.replace('/', '.')
        rede = rede.split('.')
        del rede[-1]  # deleta o CIDR
        ip = ''
        for number in rede:
            bin = self.binary_converter(number)
            ip += self.octal_base(bin)
            ip += ' '  # Adiciona um espaço para separar um valor binário do outro

        return ip.strip()

    def f_network(self) -> str:
        return self.location_network.split('/')[0]

    def f_cidr(self) -> str:
        cidr = self.location_network.split('/')[1]
        return f'/{cidr}'

    def sub_network_mask(self) -> str:
        net_bin = self.network_mask_bin()
        network_mask = ''
        for number in net_bin.split(' '):
            network_mask += self.decimal_converter(number)
            network_mask += ' '
        return network_mask.strip().replace(' ', '.')

    def network_mask_bin(self) -> str:
        cidr = self.location_network.split('/')[-1]
        net_mask_temp = ''
        net_mask = ''
        count = 0
        net_mask_list = ['', '', '', '']
        for _ in range(int(cidr)):
            net_mask_temp += '1'
            if len(net_mask_temp) == 8:
                net_mask_list[count] = net_mask_temp
                net_mask_temp = ''
                count += 1
        for index, numbers in enumerate(net_mask_list):
            if numbers == '':
                if net_mask_temp == '':
                    net_mask_temp = '0'
                net_mask_list[index] = net_mask_temp
                net_mask_temp = '0'  

        net_mask = [
            self.octal_base(bin, mask=True) for bin in net_mask_list
        ]
        
        return ' '.join(net_mask)

    def ip_for_use(self) -> int:
        bin_network = self.network_mask_bin()
        return 2 ** bin_network.count('0') - 2

    def total_ip(self) -> int:
        bin_network = self.network_mask_bin()
        return 2 ** bin_network.count('0')

    def f_ip_network(self, broadcast=False) -> str:
        net = ''.join(self.binary().split(' '))
        ip = ''
        ip_final = ['', '', '', '']
        max = int(self.f_cidr().replace('/', ''))
        count = 0

        for number in range(max):
            ip += net[number]
            if len(ip) == 8:
                ip_final[count] = ip
                ip = ''
                count += 1

        for index, number in enumerate(ip_final):
            if len(number) == 0:
                ip_final[index] = ip
                if broadcast:
                    ip = '1'
                else:
                    ip = '0'
        
        if broadcast:
            return ip_final
        ip_temp = ' '.join(ip_final) + ip
        ip_final = ''

        for number in ip_temp.split(' '):
            ip_final += self.decimal_converter(
                self.octal_base(number, mask=True)
            )
            ip_final += ' '

        return ip_final.strip().replace(' ', '.') + f'/{max}'

    def f_broadcast(self) -> str:
        broadcast = self.f_ip_network(True)
        broadcast = [self.octal_base(broad, mask=True, one=True) for broad in broadcast]
        final_broadcast = [
            self.decimal_converter(broad) for broad in broadcast
        ]
        return '.'.join(final_broadcast)

    def position_ip(self, first=False) -> str:
        value = -1 if not first else +1

        if first:
            ip = self.f_ip_network().replace(f'{self.f_cidr()}', '')
        else:
            ip = self.f_broadcast().replace(f'{self.f_cidr()}', '')

        last_ip = ip.split('.')
        last_ip[-1] = str(int(last_ip[-1]) + value)

        return '.'.join(last_ip)

    def details(self) -> None:
        print(
            f'------- CONFIGURAÇÕES PARA REDE {self.location_network} --------\n\n'
            f'{"Endereço/Rede:":<22} {self.location_network:>35}\n'
            f'{"Endereço:":<22} {self.network:>35}\n'
            f'{"Prefixo CIDR:":<22} {self.cidr:>35}\n'
            f'{"Máscara de sub-rede:":<22} {self.sub_net_mask:>35}\n'
            f'{"Ip da rede:":<22} {self.ip_network:>35}\n'
            f'{"Broadcast da rede:":<22} {self.broadcast:>35}\n'
            f'{"Primeiro Host:":<22} {self.position_ip(True):>35}\n'
            f'{"Ultimo Host:":<22} {self.position_ip():>35}\n'
            f'{"Range de IPs:":<22} {f"{self.ip_network} - {self.broadcast}":>35}\n'
            f'{"Total de IPs:":<22} {self.total_ip():>35}\n'
            f'{"Total de IPs para uso:":<22} {self.ip_for_use():>35}\n\n'
            f'{"-" * 59}' 
        )

    @staticmethod
    def valid_network(rede: str) -> str:
        try:
            rede = rede.replace('/', '.')
            rede = rede.split('.')  # Separa a rede completa em uma lista
            if int(rede[-1]) > 32 or int(rede[-1]) < 0: # Verifica se o prefixo CIDR é válido
                raise
            for number in rede[:-1]:  # Faz um laço na lista que contem os números da rede excluindo o CIDR
                number = int(number)
                if number > 255 or number < 0:  # Verifica se os números passados são superiores a 255 ou menor que 0
                    raise
            return '.'.join(rede[:-1]) + f'/{rede[-1]}'  # Faz a lista voltar a string no padrão ipv4
        except:
            raise
 
    @staticmethod
    def decimal_converter(valor: str) -> str:
        decimal = 0
        list_number = list(reversed([2**value for value in range(0, len(valor))]))
        for index, number in enumerate(list_number):
            decimal += int(valor[index]) * number
        return str(decimal)

    @staticmethod
    def octal_base(valor: str, mask=False, one=False) -> str:
        missing = len(valor)
        
        if missing == 8:
            return valor
        if one:
            missing = '1' * (8 - missing)
        else:
            missing = '0' * (8 - missing)
        if mask:
            return str(valor + missing)
        return str(missing + valor)

    @staticmethod
    def binary_converter(valor: str) -> str:
        binary = ''
        valor = int(valor)

        if valor <= 0:
            return 0

        while valor != 1:
            binary += str(valor % 2)
            valor //= 2
        return ''.join(list(reversed(binary + '1')))
