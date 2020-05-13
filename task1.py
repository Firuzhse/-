import numpy as np

   
def generate_matrix( vector, n, increasing=False ):
    
    if not increasing:
        out = np.array([x**(n-1-i) for x in vector for i in range(n)]).reshape(vector.size,n)
    elif increasing:
        out = np.array([x**i for x in vector for i in range(n)]).reshape(vector.size,n)
    
    return out

inputvector = np.array([1,2,3,4,5])
n = 3


print("matrix decreasing:\n\n", generate_matrix(inputvector,n ,False) ,"\n")
print("matrix increasing:\n\n", generate_matrix(inputvector,n ,True) ,"\n")

