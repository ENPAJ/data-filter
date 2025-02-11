from rich.console import Console
from rich.table import Table

def read_file(file_path,sep=",",encoding="utf-8"):
    if file_path.split(".")[1]=="csv":
        read_csv(file_path,sep=sep,encoding=encoding)
    elif file_path.split(".")[1]=="json":
        read_json(file_path)
    elif file_path.split(".")[1]=="yaml":
        read_yaml(file_path)
    elif file_path.split(".")[1]=="xml":
        read_xml(file_path)

def read_xml(file_path):
    pass

def read_yaml(file_path):
    pass

def read_json(file_path):
    pass


def read_csv(file_path, sep=",",encoding='utf-8'):
    """Lecture du fichier csv, prend le séparateur et le file_path"""
    with open(file_path, mode='r',encoding='utf-8') as f:
        lines = f.readlines()

    columns = lines[0].strip().split(sep)
    data = [line.strip().split(sep) for line in lines[1:]]
    return csv_data(columns,data)






class csv_data:
    def __init__(self,columns,data,sep=','):
        """Crée l'objet cd (moche il faut changer le nom psk cd ca fait commande terminal et j'aime pas)
        Il a plusieurs attributs sympas: 
        data -> data sous forme de dictionnaire avec les colonnes
        lines-> data sous forme de lignes, pas sur que j'aime bien, peut être à retirer si ca sert à rien honnêtement
        columns -> liste des colonnes
        dtypes -> les types de chaque colonne
        """
        self.lines=data
        self.columns = columns
    
        #Data sous forme de colonnes
        self.data={}
        map_index={}
        for index,column in enumerate(self.columns):
            self.data[column]=[]
            for row in self.lines:
                self.data[column].append(row[index])

        #Enregistrement des types des colonnes dans un dict
        self.dtypes = {}
        for column in self.columns:
            #part du principe que le csv est propre dès le début
            #à changer si les csv peuvent être sales mais flemme un peu psk 
            # c'est long et pas opti
            self.dtypes[column] = self.list_type(column)
            if self.dtypes[column]=='int':
                self.data[column]=list(map(int,self.data[column]))
            if self.dtypes[column]=='float':
                self.data[column]=list(map(float,self.data[column]))
            #ajouter les types suivants
        

            
    def __getitem__(self, key):
        if isinstance(key,int):
            return self.lines[key]
        
        if isinstance(key,str):
            return self.data[key]
        
        if isinstance(key,slice):
            pass
        

    def list_type(self,column):
        # à modifier si le csv peut avoir des mixed data
        if self.data[column][0]=='':
            return None
        
        try:
            type_value = type(int(self.data[column][0]))
            return str(type_value).split()[1][1:-2]
        except:
            pass

        try: 
            type_value = type(float(self.data[column][0]))
            return str(type_value).split()[1][1:-2]
        except:
            pass

        return str(type(self.data[column][0])).split()[1][1:-2]
    
    def types(self):
        """Affiche les types de colonnes en plus joli"""
        print('Les types de chaque colonne:')
        for column, type in self.dtypes.items():
            print(f"\t- {column}: {type}")
        

    def describe(self):
        '''Description du dataset (colonnes) Pour le moment uniquement valeurs numériques, mais par la suite 
        on traitera aussi le reste je pense'''
        stats = {}
        for column in self.columns:
            if self.dtypes[column]=='float' or self.dtypes[column]=='int':
                stats[column]={}
                stats[column]['sum'] = sum(self.data[column])
                stats[column]['mean'] = sum(self.data[column])/len(self.data[column])
                stats[column]['min'] = min(self.data[column])
                stats[column]['max'] = max(self.data[column])

            if self.dtypes[column]=='list':
                pass

            if self.dtypes[column]=='bool':
                pass


        for col,values in stats.items():
            print(f"Stats de {col}")
            for stat, value in values.items():
                print(f"\t- {stat}: {value}")
            
    def sort(self,cols,ascending=True,inplace=False):
        if isinstance(cols, str):  
            cols = [cols]
            

        indices = [self.columns.index(col) for col in cols]
        self.lines.sort(key=lambda x:tuple(x[i] for i in indices), reverse=not ascending)

        for i, col in enumerate(self.columns):
            self.data[col] = [row[i] for row in self.lines]

    



    def head(self, n=5):
        console = Console()
        table = Table(show_header=True, header_style="bold cyan")

        # Add columns with styling
        for col in self.columns:
            table.add_column(col, justify="left", style="bold white")

        # Add rows
        for i in range(min(n, len(self.lines))):
            row = [str(self.data[col][i]) for col in self.columns]
            table.add_row(*row)

        console.print(table)



cd=read_csv("D:\Downloads\iris.csv",sep=";")
cd.sort([cd.columns[1],cd.columns[0]],ascending=False)
cd.head()
