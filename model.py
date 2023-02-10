class Model:
    def __init__(self, json):
        self.tables = {}
        self.forms = []
        list = json["tables"]
        for obj in list:
            tbl = Table(obj)
            self.tables[tbl.name] = tbl
        if "forms" in json:
            list = json["forms"]
            bFirst = True
            for obj in list:
                self.forms.append(Form(obj, bFirst))
                bFirst = False

class Table:
    def __init__(self, model):
        self.name = model["name"]
        self.classname = model["name"]
        self.pkColumns = []
        self.columns = []
        list = model["columns"]
        for obj in list:
            col = Column(obj)
            if col.primaryKey:
                self.pkColumns.append(col.name)
            self.columns.append(col)
        self.constraints = []
        if "constraints" in model:
            list = model["constraints"]
            for obj in list:
                self.constraints.append(Constraint(obj))

    def getSearchableColumns(self):
        ret = []
        for col in self.columns:
            if col.searchable:
                ret.append(col)
        return ret

    def getColumns(self):
        columns = ["'"+column.name+"'" for column in self.columns]
        return ",".join(columns)

    def getUpdateById(self) -> str:
        columns = [column.name+" = ?" for column in self.columns if not column.primaryKey]
        ret = f"UPDATE {self.name} SET {','.join(columns)} WHERE {self.pkColumns[0]} = ?"
        return ret

    def getUpdateFields(self, objName: str) -> str: 
        columns = [f"{objName}.{column.name}" for column in self.columns if not column.primaryKey]
        return ",".join(columns)

    def getInsert(self) -> str:
        columns = [column.name+" = ?" for column in self.columns if not column.primaryKey]
        vals = ['?']*len(columns)
        ret = f"INSERT INTO {self.name} ( {','.join(columns)} ) VALUES ({','.join(vals)})"
        return ret

    def getFindByMethod(self, colname):
        return "find_{}_by_{}".format(self.classname, colname)


class Column:
    def __init__(self, model):
        self.name = model["name"]
        self.type = (model["type"] if "type" in model else "text")
        self.primaryKey = (model["primary_key"] if "primary_key" in model else False)
        self.notNull = (model["not_null"] if "not_null" in model else False)
        self.autoincrement = (model["autoincrement"] if "autoincrement" in model else False)
        self.searchable = (model["searchable"] if "searchable" in model else False)

class Constraint:
    def __init__(self, model):
        self.type = model["type"]
        self.columns = model["columns"]
        if "references" in model:
            self.references = model["references"]

class Form:
    def __init__(self, model, mainForm=False):
        self.mainForm = mainForm
        self.name = model["name"]
        self.table = model["table"]
        self.showFilter = (model["show_filter"] if "show_filter" in model else False)
        self.showChildren = (model["show_children"] if "show_children" in model else False)
