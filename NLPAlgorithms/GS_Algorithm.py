def stableMatching(n, menPreferences, womenPreferences):
    
    unmarriedMen = list(range(n))
   
    manSpouse = [None] * n                      
    
    womanSpouse = [None] * n                      
    
    nextManChoice = [0] * n                       
    
   
    while unmarriedMen:
        
        he = unmarriedMen[0]                      
        
        hisPreferences = menPreferences[he]       
        
        she = hisPreferences[nextManChoice[he]] 
       
        herPreferences = womenPreferences[she]
        
        currentHusband = womanSpouse[she]
       
        
        
        if currentHusband == None:
          
          womanSpouse[she] = he
          manSpouse[he] = she
          
          nextManChoice[he] = nextManChoice[he] + 1
          
          unmarriedMen.pop(0)
        else:
          
          currentIndex = herPreferences.index(currentHusband)
          hisIndex = herPreferences.index(he)
         
          if currentIndex > hisIndex:
             #New stable match is found for "her"
             womanSpouse[she] = he
             manSpouse[he] = she
             nextManChoice[he] = nextManChoice[he] + 1
             #Pop the newly wed husband
             unmarriedMen.pop(0)
             #Now the previous husband is unmarried add
             #him to the unmarried list
             unmarriedMen.insert(0,currentHusband)
          else:
             nextManChoice[he] = nextManChoice[he] + 1
   
    return manSpouse
