class csv_data:
    def __init__(self,file_path,sep=','):
        """Crée l'objet cd (moche il faut changer le nom psk cd ca fait commande terminal et j'aime pas)
        Il a plusieurs attributs sympas: 
        data -> data sous forme de dictionnaire avec les colonnes
        lines-> data sous forme de lignes, pas sur que j'aime bien, peut être à retirer si ca sert à rien honnêtement
        columns -> liste des colonnes
        dtypes -> les types de chaque colonne
        """
        self.lines=[]
        self.columns = []
        #Lecture du csv ligne par ligne et stockage
        with open(file_path, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            self.columns = lines[0].strip().split(sep)
            for line in lines[1:]:
                self.lines.append(line.strip().split(sep))
    
        #Data sous forme de colonnes
        self.data={}
        map_index={}
        for index,column in enumerate(self.columns):
            self.data[column]=[]
            map_index[index] = column

        for i in self.lines:
            for j in range(len(i)):
                self.data[map_index[j]].append(i[j])

        #Enregistrement des types des colonnes dans un dict
        self.dtypes = {}
        for column in self.columns:
            #part du principe que le csv est propre dès le début
            #à changer si les csv peuvent être sales mais flemme un peu psk 
            # c'est long et pas opti
            self.dtypes[column] = self.list_type(column)

    def list_type(self,column):
        # à modifier si le csv peut avoir des mixed data
        if self.data[column][0]=='':
            return None
        
        try:
            type_value = type(int(self.data[column][0]))
            return type_value
        except:
            pass

        try: 
            type_value = type(float(self.data[column][0]))
            return type_value
        except:
            pass

        return type(self.data[column][0])
    
    def types(self):
        """Affiche les types de colonnes en plus joli"""
        print('Les types de chaque colonne:')
        for column, type in self.dtypes.items():
            print(f"\t- {column}: {str(type).split()[1][1:-2]}")
        

    


cd=csv_data("D:\Downloads\iris.csv",sep=";")
print(cd.columns)
print(cd.types())

