def get_similarity(hash0,hash1):
    size=len(hash0)
    bit_difference_count=0
    # print("hash0 = ",hash0)
    # print("hash1 = ",hash1)
    for i in range(0,size-1):
        if(hash0[i]!=hash1[i]):
            # print("pass",i,"done")
            bit_difference_count+=1
    return ((1-(bit_difference_count/size))*100)
