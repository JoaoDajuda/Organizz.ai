from ORCAMENTO.soma import addvalor
from ORCAMENTO.subtracao import subvalor
from ORCAMENTO.ver_saldo import versaldo

def main():
    while True:
        print('Digite o que deseja realizar:')
        print('1 - "Adicionar" saldo')
        print('2 - "Subtrair" compra')
        print('3 - "ver" saldo') 
        print('4 - "fechar" programa')
        print('=-=-=-=-=-=-=-')
        choose = (' ')
        choose = input('digite uma opção: ').lower().strip()
        
        if choose == '1' or choose == 'adicionar':
            addvalor()
        elif choose == '2' or choose == 'subtrair':
            subvalor()
        elif choose == '3' or choose == 'ver':
            versaldo()
        elif choose == '4' or choose == 'fechar':
            print("finalizando programa...")
            break
        else:
            print('=-=-==-=-=-=')
            print('formato inválido ou opção inexistente, digite novamente')
            print('=-=-=-==-=-')