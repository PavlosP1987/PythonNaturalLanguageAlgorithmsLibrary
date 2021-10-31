def zeta(s):
   n=len(s)
   z=[0]*n
   L,R=-1,-1
   for i in range(1,n):
      j,k=0,i
      if L<=i<=R:
         ii = i-L
         j=min(ii+z[ii], R-L+1)-ii
         k=i+j
      while k<n and s[j]==s[k]: 
         j+=1
         k+=1
      z[i]=k-i
      if z[i]>0 and i+z[i]-1>R: 
         L,R=i,i+z[i]-1
   return z

def find_occurrences(p,t):
   lp,lt=len(p),len(t)
   z=zeta(p+t)
   for i in range(lp,lp+lt):
      if z[i]>=lp: print i-lp
