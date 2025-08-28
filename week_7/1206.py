import math
N=int(input())
I,o=[float(input()) for _ in range(N)],0
def check(o):
    for x in I:
        l,r=0,10*o
        while l<r:
            mid=math.floor((l+r)/2)
            if (mid/o)<x: l=mid+1
            else: r=mid
        if math.trunc((l/o)*1000)/1000!=x: return False
    return True
while o < 1000:
    o+=1
    if check(o): break
print(o)