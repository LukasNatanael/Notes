class File:
    '''
        r  -> read mode
        w  -> write mode
        a  -> append mode
        r+ -> read and write
        
        => ler fotos
            rb -> read binary
            wb -> write binary

        read()      -> retorna o conteúdo do arquivo
        readlines() -> retornar uma lista de cada linha do arquivo
        readline()  -> retorna a primeira linha arquivo
    '''

    def __init__(self, filename):
        self.name = filename

    def read(self):
        try:
            with open(self.name, 'r') as file:
                for line in file:
                    print(line, end='')

        except FileNotFoundError:
            print(f'{self.name} was created successfully')
            file = open(self.name, 'w+')
            

    def write(self, content):
        try:
            with open(self.name, 'w') as file:
                file.write(content)

        except FileNotFoundError:
            print(f'{self.name} was created successfully')
            file = open(self.name, 'w+')

            with open(self.name, 'w') as file:
                file.write(content)

    def insert(self, newContent):
        with open(self.name, 'a') as file:
            file.write(newContent)

    def delete(self):
        from os import system
        system(f'PowerShell Remove-Item {self.name}')
        print(f'{self.name} was removed successfully!')

    def open(self):
        from os import system
        system(f'PowerShell notepad {self.name}')
