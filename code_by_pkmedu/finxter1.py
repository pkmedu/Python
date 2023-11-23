# Python Riddle: Guess the output of this code snippet

s = "asxhtlitycoliqnab"
mystery = s[1:4:2] + s[6:8] + ('x' if not s else s[9:11]) + s[12:-1:2] + 's'

print(f'https://blog.finxter.com/{mystery}/')
