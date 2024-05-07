class ListElements:
    def __init__(self, ls):
        self.ls = ls

    def print_list(self):
        print(self.ls)


def add_element(ls):
    ls.append(1)


ls1 = [5]
listEm = ListElements(ls1)
listEm.print_list()
add_element(ls1)
listEm.print_list()
