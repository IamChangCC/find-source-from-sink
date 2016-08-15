#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
from joern.all import JoernSteps
from collections import Counter
import tree,node
#from joerntools.shelltool.ChunkStartTool import ChunkStartTool
#import get_all_functions
#from node_strcture import node
#from edge_structure import edge

NEO4J_URL ='http://localhost:7474/db/data/'
PARAMETER = 'Parameter'
VARIABLE = 'Variable'
CALLEE = 'Callee'
PATH=[]
#FILE_PATH = '/home/chucky/chucky/multilayer_embedder/tmp_folder'


########################################################################
class get_source():
  """"""

  #----------------------------------------------------------------------
  def __init__(self):
    """Constructor"""
    self.JS = JoernSteps()
    self.JS.setGraphDbURL(NEO4J_URL)
    self.JS.connectToDatabase()     
    #self.source_sink_path=[]
    #self.sink_source_tree=tree()
    
  """given a nodeId , this can get the type of the node ,result is utf string"""
  def get_type(self,node_id):
    query_get_type="""g.v(%s).getProperty("type")"""%node_id 
    query_result = self.JS.runGremlinQuery(query_get_type)
    return query_result.encode('utf-8')     
  
  '''given a node that means sink, this can get the sources in the function''' 
  def get_source_within_func(self,node_id):
    get_source_query="""g.v(%s).sources().id"""%node_id
    #getArguments("printf", "1")
    query_result = self.JS.runGremlinQuery(get_source_query)
    source_node_list=[]#store the source nodes
    source_node_tmp=[]#store the source nodes temply
    for r in query_result:
      if self.get_type(r) != "Parameter":
        print "the source node %s is not the \"Parameter\" type"
      else:
        source_node_list.append(r)
    return source_node_list
  
  '''given a node that means sink, this can get the sources in the function''' 
  def get_source_of_IdentifierDeclStatement(self,node_id):
    source_node_list=[]#store the source nodes
    source_node_tmp=[]#store the source nodes temply      
    if self.get_type(node_id)=="IdentifierDeclStatement":
      get_source_query="""g.v(%s).out("USE").filter{it.type=="Symbol"}.in("DEF").id"""%node_id
      query_result = self.JS.runGremlinQuery(get_source_query)
      for r in query_result:
        if self.get_type(r) != "Parameter":
          print "the source node %s is not the \"Parameter\" type"
        else:
          source_node_list.append(r)
            
    return source_node_list  
  
  
  '''get the source parameter's Identifier node'''
  def get_Identifier_source(self,node_id):
    get_Identifier_source="""g.v(%s).out("IS_AST_PARENT").filter{it.type=="Identifier"}.id"""%node_id
        #getArguments("printf", "1")
    source_Identifier_node = self.JS.runGremlinQuery(get_Identifier_source)    
    return source_Identifier_node    
  
  '''get the source parameter's Identifier node'''
  def get_ParameterType_source(self,node_id):
    get_ParameterType_source="""g.v(%s).out("IS_AST_PARENT").filter{it.type=="ParameterType"}.id"""%node_id
        #getArguments("printf", "1")
    source_ParameterType_node = self.JS.runGremlinQuery(get_ParameterType_source)    
    return source_ParameterType_node    
  
  
  '''given a node that means sink, this can get the sources out of the function''' 
  def get_source_between_func(self,node_id):
    get_source_query="""g.v(%s).in("IS_ARG").id"""%node_id
    #getArguments("printf", "1")
    query_result = self.JS.runGremlinQuery(get_source_query)
    source_node_list=[]#store the source nodes
      #source_node_tmp=[]#store the source nodes temply
    for r in query_result:
      if r not in source_node_list:
        source_node_list.append(r)
    return source_node_list  
  
  
  '''get the sink nodes of specified function'''
  def get_sink(self,function_name,arg_num):
    sink_query="""getArguments(\"%s\", \"%s\").id"""%(function_name,arg_num)
    query_result = self.JS.runGremlinQuery(sink_query)
    sink_node_list=[]
    for r in query_result:
      if r not in sink_node_list:
        sink_node_list.append(r)   
    return sink_node_list     

  '''decide whether the node is over'''
  def wether_is_over(self,node_id):
    leble=False
    '''the symbol has not def nodes'''
    if self.get_type(node_id)=="Symbol":
      query="""g.v(%s).in("DEF").id"""%node_id
      query_result=self.JS.runGremlinQuery(query)
      if len(query_result) == 0:
        leble=True
    '''the PARAMETER has not Identifier nodes'''
    if self.get_type(node_id)=="Parameter":
      query="""g.v(%s).out("IS_AST_PARENT").filter{it.type=="Identifier"}.in("IS_ARG").id"""%node_id
      query_result=self.JS.runGremlinQuery(query)
      if len(query_result) == 0:
        leble=True     
    '''the PARAMETER has not Identifier nodes'''
    if self.get_type(node_id)=="IdentifierDeclStatement":
      query="""g.v(%s).out("USE").filter{it.type=="Symbol"}.in("DEF").id"""%node_id
      query_result=self.JS.runGremlinQuery(query)
      if len(query_result) == 0:
        leble=True 
    '''the PARAMETER has not Identifier nodes'''
    if self.get_type(node_id)=="Identifier":
      query="""g.v(%s).out.id"""%node_id
      query_result=self.JS.runGremlinQuery(query)
      query_has_arg="""g.v(%s).in("IS_ARG").id"""%node_id
      query_result1=self.JS.runGremlinQuery(query_has_arg)
      if len(query_result)==0 and len(query_result1) == 0:
        leble=True     
    return leble
  
  '''get the source node of specified sink node'''
  def get_source(self,node):
    #source_current_func=get_source_within_func(node_id)
    #node.add(node_id)
    node_id = node.getdata()
    last_source=node_id
    if not self.wether_is_over(last_source):
      ###sources() get the parameter nodes'''
      if self.get_type(last_source)=="Argument":        
        last_source_tmp=self.get_source_within_func(last_source)
        last_sources=last_source_tmp
        for last_source in last_sources:
          node.add(tree.node(last_source))
        for source_node in last_sources:
          identifier_node=self.get_Identifier_source(source_node)
          if identifier_node is not None:
            for neighbor_source in identifier_node:
            
              node.add(self.get_source(neighbor_source))
      ###this should get the arguement nodes'''
      elif len(self.get_source_between_func(last_source))!=0:   
        last_source_tmp=self.get_source_between_func(last_source)
        last_source=last_source_tmp
        node.add(last_source)
        for source_node in last_source:
          identifier_node=self.get_Identifier_source(source_node)
          if identifier_node is not None:
            for neighbor_source in identifier_node:
              node.add(self.get_source(neighbor_source)) 
       ###sources() get the IdentifierDeclStatement nodes'''
      elif len(self.get_source_of_IdentifierDeclStatement(last_source))!=0:
        last_source_tmp=self.get_source_of_IdentifierDeclStatement(last_source)
        last_source=last_source_tmp
        node.add(last_source)
        for source_node in last_source:
          identifier_node=self.get_Identifier_source(source_node)
          if identifier_node is not None:
            for neighbor_source in identifier_node:
              node.add(self.get_source(neighbor_source))           
  
  
  def execute(self): 
    sink_func=sys.argv[0]
    arg_num=sys.argv[1]
    
    #root_node = tree.node(sink_func)
    for node_id in self.get_sink(sink_func,arg_num):
      print "Now, the sink node id is ",node_id
      sink_node = tree.node(node_id)
      self.sink_source_tree._head.add(sink_node)
      current_path=[]
      self.get_source(sink_node)
      print "ok"
      '''current_node.add(node_id)
      sources = self.get_source_within_func(node_id)
      for node in sources:
        print self.get_Identifier_source(node)
        print self.get_ParameterType_source(node)'''
      
    

  
if __name__ == '__main__':
  get_source().execute()


