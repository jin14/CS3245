class Cacher:

##    This is a cacher class that is used to keep track of the queries made. It is instantiated with a size limit inputted by the user.
##    It keep tracks of the frequency of each of the query as well as the results of the query.
   
    
    def __init__(self,limit):
        self.cache = {}
        self.limit = limit
    
    def contains(self,key): # check if a query has been cached before
        
        return key in self.cache
    
    def update(self,key,value): # update the frequency count of the query
        
        if len(self.cache) >= self.limit:
            self.cache.pop(min(self.cache.items(),key = lambda x: x[1]["c"])[0])
            
            self.cache[key] = {"p": value, "c":1}
        
        else:
            self.cache[key] = {"p":value, "c":1}
            
    def get(self,key): # return the result of the cached query
        self.cache[key]["c"]+=1
        return self.cache[key]["p"]
