class Graphs():
    #defininig class for graph
    def __init__(self):
        self.graph={}                   #i implemented graph using dictionary 
        #self.nofedges=0                 #number of edges in graph
        #self.nofvert=0                  #number of vertices in the graph

    def add_edge(self,u,v,c):
        #function to add edge in the graph
        #keys store vertex, items store tuple of the other vertex of edge and capacity of edge
        #it is undirected graph, hence links are bidirectional with same capacity
        if u in self.graph and v in self.graph:                 #various cases to add edge to the graph
            self.graph[u].append((v,c))
            self.graph[v].append((u,c))
            #self.nofedges+=1    
        elif u not in self.graph and v in self.graph:
            self.graph[v].append((u,c))
            self.graph[u]=[(v,c)]
            #self.nofedges+=1                                    #updating number of edges for each case
            #self.nofvert+=1                                     #updating number of vertices for each case
        elif u in self.graph and v not in self.graph:
            self.graph[u].append((v,c))
            self.graph[v]=[(u,c)]
            #self.nofedges+=1
            #self.nofvert+=1
        else:
            self.graph[u]=[(v,c)]
            self.graph[v]=[(u,c)]
            #self.nofedges+=1                
            #self.nofvert+=2

    def get_vernodes(self):                     
        #it gives list of all vertices of the graph, it is not used in my code
        L=[]
        for i in self.graph.keys():
            L.append(i)
        return L        
    

class maxheaps():
    #defining maximum heap class

    def _parent(self,j):
        return (j-1)//2

    def _left(self,j):
        return 2*j+1

    def _right(self,j):
        return 2*j+2

    def _has_leftchild(self,j):
        return self._left(j)<len(self.hpnodelis)

    def _has_rightchild(self,j):
        return self._right(j)<len(self.hpnodelis)

    def swap(self,i,j):
        self.hpnodelis[i],self.hpnodelis[j]=self.hpnodelis[j],self.hpnodelis[i]
    
    def upheap(self,j):
        parent=self._parent(j)          #parent of j
        if j!=0 and j<self.lenheap():               
            if self.hpnodelis[parent][2]<self.hpnodelis[j][2]:      #if element at parent is smaller than at j we swap to maintain heap property and repeat for parent
                self.swap(parent,j)
                self.upheap(parent)
    
    def downheap(self,j):
        if self._has_leftchild or self._has_rightchild:             #if node has any child
            leftch,rightch=None,None
            if self._has_leftchild(j):                              #if left child present
                leftch=self._left(j)
                biggerch=leftch
                if self._has_rightchild(j):                         #if right child present
                    rightch=self._right(j)
                    if self.hpnodelis[rightch][2]>self.hpnodelis[leftch][2]:        #taking bigger child
                        biggerch=rightch
                if self.hpnodelis[biggerch][2]>self.hpnodelis[j][2]:            #maintaining heap property
                    self.swap(biggerch,j)
                    self.downheap(biggerch)
                
    def __init__(self,s):
        #self.nodeind=[i for i in range(len(unvis))]
        ink=float('inf')                #assigning infinity
        self.hpnodelis=[[s,s,ink]]      #initial element of heap
    
    def heapify(self):
        #to satisfy heap property we use heapify
        srt=self._parent(len(self.hpnodelis)-1)
        for i in range(srt, -1, -1): 
            self.downheap(i)

    def addnode(self,parent,new,cap):
        #add new node in heap and rebalances to mantain heap property
        self.hpnodelis.append([parent,new,cap])
        if self.lenheap()>1:
            self.upheap(len(self.hpnodelis)-1)

    def lenheap(self):
        #return length of heap
        return len(self.hpnodelis)  

    def extract_max(self):
        #returns maximum element(w.r.t. capacity) of heap
        return self.hpnodelis[0]

    def delmax(self):
        #delete maximum element and return it
        if self.lenheap()!=0:
            self.swap(0,self.lenheap()-1)           #swap first(maximum) element with last element
            delnode=self.hpnodelis.pop()            #delete and return last node
            self.downheap(0)                        #to maintain heap property
            return delnode


def findMaxCapacity(n,links,s,t):
    #function to find maximum capacity and the path with maximum capacity between s and t 

    #create graph for the links of routers given
    G=Graphs()
    for i in links:
        G.add_edge(i[0],i[1],i[2])      #each link is bidirectional with same capacity

    ink=float('inf')        #represent infinity
    heap=maxheaps(s)        #max heap creation with source vertex

    #l=G.nofvert 
    parentlis=[0]*n             #list to store parent vertex of all vertices
    maxcap=[-ink]*n             #list to store maximum capacity (for max capacity path) for each vertices
    maxcap[s]=ink               #initialise infinity for source vertex
    tf=[False]*n                #list storing explore status of vertices
    #vv=[]
    
    while heap.extract_max()[1]!=t :                    #till we reach destination vertex
        maxver=heap.delmax()                            #extract and delete maximum element from heap
        curr_ver=maxver[1]                              #current vertex

        if maxcap[curr_ver]==maxver[2]:                 #check for heap node to be explored or not

            if tf[curr_ver]==False:                     #check explored status
                tf[curr_ver]=True  
                #vv.append(maxver[1])  
                                
                neighbours=G.graph[curr_ver]            #neighbours of current vertex
                for vertex in neighbours:               #checking for each neighbour
                    
                    temp=min(vertex[1],maxver[2])               #calculate widest possible path beyond
                    currcap=max(temp,maxcap[vertex[0]])
                    
                    if currcap>maxcap[vertex[0]]:               #we will update only if we get new capacity more than the previos one
                        
                        maxcap[vertex[0]]=currcap               #updating max capacty for neighbour vertex
                        heap.addnode(curr_ver,vertex[0],currcap)        #addiing neighbour in heap to visit later
                        parentlis[vertex[0]]=curr_ver                   #storing parent vertex for neighbour

    #print(vv) 
    path=getpath(t,parentlis,s)                   #to get the path from s to t of maximum capacity we recur over parent list

    #return list of max capacity and path of max capacity from s to t
    return (maxcap[t],path)

def getpath(ver,parlis,s):
    #function to get widest path between source and target vertex 
    L=[]
    while ver!=s:
        L.append(ver)
        ver=parlis[ver]
    L.append(s)
    L.reverse()
    return L
