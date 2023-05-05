import base64

#Open file
words = open("b64.txt","r").read();

#Decode 50 times
for i in range(50):
    words = base64.b64decode(words)

print(f"The flag is: {words.decode('utf8')}")
