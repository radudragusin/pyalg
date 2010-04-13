def Partition(A,i,j):
    x = A[i]
    h = i
    for k in range(i+1,j):
        if A[k] < x:
            h = h + 1
            A[h], A[k] = A[k], A[h]
    A[h], A[i] = A[i], A[h]    
    return h
        
def QuickSort(A,p=0,r=-1):
    if r is -1:
        r = len(A)
    if p < r - 1:
        q = Partition(A,p,r)
        QuickSort(A,p,q)
        QuickSort(A,q+1,r)
