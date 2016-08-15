
'''
########################################################################
class tree_node:
    """the path from sink to sources can be discribed like a tree"""

    #----------------------------------------------------------------------
    def __init__(self,node_id):
        """Constructor"""
        self.node_id=node_id
        self.child_list=[]
        self.parent_id=0
    
    #----------------------------------------------------------------------
    def add_child(self,parent_node,child_node):
        """add a new node to the tree"""
        child = self.__init__(child_node)
        child
'''        


class node():
    def __init__(self, data):
        self._data = data
        self._children = []

    def getdata(self):
        return self._data

    def getchildren(self):
        return self._children

    def add(self, node):
        ##if full
        if len(self._children) == 6:
            return False
        else:
            self._children.append(node)

    def search_children(self, data):
        for child in self._children:
            if child.getdata() == data:
                return child
        return None
    
        
    


    #----------------------------------------------------------------------
    """def search_node(self,data):
        
        cur = self._head
        if cur.getdata()==data:
            return cur
        else :            
            while len(cur.getchildren())>0:
                if cur.search_children(data)!=None:
                    return cur.search_children(data)
                else:
                    
       """             
            
        
        

        
    
    