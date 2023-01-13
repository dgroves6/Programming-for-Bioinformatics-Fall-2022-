#!/usr/bin/env python3

s = "{{}}}{"

if len(s) % 2 != 0:
    print("No")

ans = True
while ans:
    if len(s) == 0: # If all curly braces have pairs, return True
        print("Yes")
        break

    for i in range(len(s)-1): # Iteratively remove pairs of braces {}
        if s[i]=="{" and s[i+1]=="}":
            s = s[:i]+s[i+2:]
            break

        if i==len(s)-2: # If no matching pair is found by end of parse, return False
            ans = False
            print("No")

# Test Cases
'''
a = "{{{}}}"; d = "}}{{"
b = "{{}{}}"; e = "{}}{" 
c = "{{{}}{}}"; f = "{{}}}{"

test = [a,b,c,d,e,f]

for s in test:
    if len(s) % 2 != 0:
        print("No")
        continue
    
    ans = True
    while ans:
        if len(s) == 0: # If all curly braces have pairs, return True
            print("Yes")
            break

        for i in range(len(s)-1): # Iteratively remove pairs of braces {}
            if s[i]=="{" and s[i+1]=="}":
                s = s[:i]+s[i+2:]
                break

            if i==len(s)-2: # If no matching pair is found by end of parse, return False
                ans = False
                print("No")
'''