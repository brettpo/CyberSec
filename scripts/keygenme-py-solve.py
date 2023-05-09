import hashlib
from cryptography.fernet import Fernet
import base64


key_part_static1_trial = "picoCTF{1n_7h3_|<3y_of_"
key_part_dynamic1_trial = "xxxxxxxx"
key_part_static2_trial = "}"
key_full_template_trial = key_part_static1_trial + key_part_dynamic1_trial + key_part_static2_trial

bUsername_trial = b"FRASER"

potential_dynamic_key = ""

#start decrypting after "_" of key_part_static1_trial, ie. 23rd position

offset = 23 

#check dynmaic part function positions = [4][5][3][6][2][7][1][8]

positions = [4,5,3,6,2,7,1,8]


#loop through positions and get sha256 for p

for p in positions:
	potential_dynamic_key += hashlib.sha256(bUsername_trial).hexdigest()[p]
	
#set the key to part 1 + the key from potential dynamic key + part 2
	
key = key_part_static1_trial + potential_dynamic_key + key_part_static2_trial
print(key)
