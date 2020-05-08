# https://codeforces.com/problemset/problem/931/A

def f(n):
    return (n*(n+1))//2

a=int(input())
b=int(input())
dist = abs(a-b)
aMoves = (dist+1)//2
bMoves = dist//2
print(f(aMoves)+f(bMoves))
