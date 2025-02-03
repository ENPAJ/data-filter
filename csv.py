class csv_data:
    def __init__(self,file_path,sep=','):
        #Lecture du csv ligne par ligne et stockage
        with open(file_path, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            self.columns = lines[0].split(sep)
            for line in lines[1:]:
                