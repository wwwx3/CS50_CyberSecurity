#ROT code is for solving Ceasar Cipher ROT stands for "rotate" 
# which is a simple letter substitution cipher that shifts letters 
# by a fixed number down the alphabet.



#This algorithm works by brute forcing all 26 possible shifts(ROT0 to ROT25))



def caesar(s, shift):
    result = ""
    for ch in s:
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            result += chr((ord(ch) - ord(base) + shift) % 26 + ord(base))
        else:
            result += ch
    return result

cipher = input("Enter the cipher text: ")
for shift in range(26):
    print(f"Shift {shift:2}: {caesar(cipher, shift)}")
