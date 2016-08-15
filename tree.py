import node
########################################################################
class tree():
    """"""

    #----------------------------------------------------------------------
    def __init__(self,node_id):
        """Constructor"""
        self._head = node.node(node_id)
    #----------------------------------------------------------------------
    def linktohead(self,node):
        """"""
        self._head.add(node)
        
    #----------------------------------------------------------------------
    def insert(self,path,data):
        """"""
        cur_node = self._head
        for step in path:
            if cur.search_children(step)==None:
                return False
            else:
                cur=cur.search_children(step)
        cur.add(node(data))
        return True
    
    #----------------------------------------------------------------------
    def search(self,path):
        """"""
        cur = self._head
        for step in path:
            if cur.search_children(step) == None:
                return None
            else:
                cur = cur.search_children(step)
        return cur
    
    def add_subtree(self,parent_node,sub_tree):    
        parent_node._children.append(sub_tree._head)        
    
    
    '''class tree:
    
        def __init__(self,node_id):
            self._head = node(node_id)
    
        def linktohead(self, node):
            self._head.add(node)
    
        def insert(self, path, data):
            cur = self._head
            for step in path:
                if cur.search_children(step) == None:
                    return False
                else:
                    cur = cur.search_children(step)
            cur.add(node(data))
            return True
    
        def search(self, path):
            cur = self._head
            for step in path:
                if cur.search_children(step) == None:
                    return None
                else:
                    cur = cur.search_children(step)
            return cur'''
        
    
    