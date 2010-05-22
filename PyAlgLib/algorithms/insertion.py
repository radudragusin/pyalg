def InsertionSort(A):
    for i in range(1,len(A)):
        j = i - 1
        while(j >= 0):
            if A[j] > A[j+1]:
                (A[j], A[j+1]) = (A[j+1], A[j]) 
                j = j - 1
            else:
                break
            pass
