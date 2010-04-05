def InsertionSort(A):
    # Insertion Sort on a list
    for i in range(1,len(A)):
        j=i-1
        while(j>=0):
            if A[j]>A[j+1]:
                (A[j], A[j+1]) = (A[j+1], A[j]) 
                j=j-1
            else:
                break
            if False:
		pass
            pass
            
if __name__ == '__main__':
	A = [7,2,5,23,0,1,5,2]
	InsertionSort(A)
	print A
