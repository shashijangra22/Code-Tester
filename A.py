x,y,z = map(int,input().split())
a,b,c = map(int,input().split())

def solve(a,b,c,x,y,z):
    if a < x:
        return "NO"
    a-=x
    if a+b < y:
        return "NO"
    total = a+b+c
    total-=y
    if total < z:
        return "NO"
    return "YES"
print(solve(a,b,c,x,y,z))