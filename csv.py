class csv_data:
    def __init__(self,file_path,sep=','):
        self.lines=[]
        self.columns = []
        #Lecture du csv ligne par ligne et stockage
        with open(file_path, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            self.columns = lines[0].strip().split(sep)
            for line in lines[1:]:
                self.lines.append(line.strip().split(sep))
    
        self.data={}
        map_index={}
        for index,column in enumerate(self.columns):
            self.data[column]=[]
            map_index[index] = column

        for i in self.lines:
            print(i)
            for j in range(len(i)):
                self.data[map_index[j]].append(i[j])

        #Enregistrement des types des colonnes dans un dict
        self.dtypes = {}
        for column in self.columns:
            #part du principe que le csv est propre dès le début
            self.dtypes[column] = self.list_type(column)

    def list_type(self,column):
        # à modifier si le csv peut avoir des mixed data
        return type(self.data[column])

    


cd=csv_data("D:\Downloads\iris.csv",sep=";")
print(cd.columns)
print(cd.data)

