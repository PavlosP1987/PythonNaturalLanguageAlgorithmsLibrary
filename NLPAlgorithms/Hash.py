def val(ch): #maps a character to a digit e.g a = 1, b = 2,...
   return ord(ch)-ord("a")+1

def find_occurrences(p,t):
   lp,lt=len(p),len(t)
   m=10**9+7 #modulo (a "big" prime)
   b=30      #numeration system base
   hp=0      #hash of the pattern
   ht=0      #hash of a substring of length |P| of the text
   for i in range(lp):
      hp=(hp*b+val(p[i]))%m
      ht=(ht*b+val(t[i]))%m
   pwr=1
   for i in range(lp-1): 
      pwr=pwr*b%m

   if hp==ht: print 0
   for i in range(1,lt-lp+1):
      #rolling hash
      #remove character i-1:
      ht=(ht-val(t[i-1])*pwr)%m
      ht=(ht+m)%m
      #add character i+|P|-1
      ht=(ht*b+val(t[i+lp-1]))%m
      if ht==hp: print i   
