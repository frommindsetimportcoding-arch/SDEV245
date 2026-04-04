from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import hashlib



# Go through each of the letters in a message
class CaesarSubstitution:
    """ The caesar substitution will take an input and encrypt the message by shifting the ASCII code values and printing the result.
        It will then decrypt the message by inversing the shift in ASCII code back to the original values."""
    FIRST_CHAR_CODE = 97
    LAST_CHAR_CODE = 122
    CHAR_RANGE = 26

    def __init__(self):
        # Initializing the variables. 
        self.msg = input('\nWhat is the message you would like enrypted?  Enter:  ')
        self.shift = 10

    def caesar_encrypt(self):
        """ The encryption function sticks within the range of ASCII codes 97-122 (the lowercase alphabet). 
            It ignores any non-alpha characters. Iteration occurs over the input string and the result of 
            each iteration is appended to the variable 'result'. """
        result = ""
        for char in self.msg.lower():

            if char.isalpha():
                # Convert character to the ASCII code.
                char_code = ord(char)
                new_char_code = char_code + self.shift

                if new_char_code > self.LAST_CHAR_CODE:
                    new_char_code -= self.CHAR_RANGE

                new_char = chr(new_char_code)
                result += new_char
            else:
                result += char

        return result.capitalize()

    def caesar_decrypt(self, message):
        """ The decryption function runs the inverse of the encryption function by shifting the ASCII codes in the 
            opposite direction to retrieve the original input."""
        result = ""
        for char in message.lower():
            if char.isalpha():
                # Conver character to the ASCII code.
                char_code = ord(char)
                new_char_code = char_code - self.shift

                if new_char_code < self.FIRST_CHAR_CODE:
                    new_char_code += self.CHAR_RANGE

                new_char = chr(new_char_code)
                result += new_char

            else:
                result += char

        return result.capitalize()



class HashingSHA:
    """ This will generate SHA-256 hashes for a message input and allow you to see the values of a hash output after modifying the input.""" 
    def __init__(self):
        self.msg = input('\n\nPlease enter the message you would like to see hashed.\nEnter:  ')

    def hash_encode(self):
        """ This will create the hash object and then the digested hexidecimal output."""
        hash_object = hashlib.sha256(self.msg.encode())
        hex_digest = hash_object.hexdigest()

        original_hex = hex_digest
        print(f'\nThe hashed value is below:\n{original_hex}')
    
    def modify_msg(self):
        """ This function modifies the input data and proves that the hash_object has completely changed"""
        self.msg = input('\nNow, modify the original message by 1 or more characters.\nEnter:  ')
        
        hash_object = hashlib.sha256(self.msg.encode())
        hex_digest = hash_object.hexdigest()

        modified_hex = hex_digest
        print(f'\nThe modified hashed value is below:\n{modified_hex}')

    def revert_msg(self):
        """ This function allows you to revert the message by typing the original message and proves that 
            the hash value is the same as the original message."""
        self.msg= input(f'\nNow, enter the original message to see if the hashed value matches again.\nEnter:  ')

        hash_object = hashlib.sha256(self.msg.encode())
        hex_digest = hash_object.hexdigest()

        reverted_hex = hex_digest
        print(f'\nThe reverted hashed value is below:\n{reverted_hex}')



class Signature:
    """ Defines the function of the sender and the function of the receiver. Sender will create a message that will run through hash digestion. 
        Then the sender will encrypt the hashed object with their private key. The receiver function will decrypt the original message and the hash object.
        Then the receiver function will perform  their own hash digestion to compare the hash digest to the one received to verify integrity. The public keys will
        be locally shared in this class, but would traditionally need to be traded in what is known as a handshake."""
    
    def __init__(self):

        self.sender_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.sender_public_key = self.sender_private_key.public_key()

        self.receiver_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.receiver_public_key = self.receiver_private_key.public_key()


    def sender(self):
        
        self.message = (input(f'\nEnter message here:  ')).encode('utf-8')

        self.signature = self.sender_private_key.sign(
            self.message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        print(f'Message signed. Signature: {self.signature.hex()[:20]}...')


    
    def receiver(self):

        try:
            # The verify method compares the signature to a new hash of the message.
            # If it doesn't match, it raises an InvalidSignature exception.
            self.sender_public_key.verify(
                self.signature,
                self.message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            print('Verification successful: The message has been authenticated.')
        except Exception:
            print('Vericfication failed: the message or signature has been tampered with!')


    def tamper(self):
        decision = input('Would you like to tamper with the message? Enter "y" for yes or "n" for no.\nTamper:  ' )

        if decision.lower() == "y":
            self.message = (f'This message has been tampered with.')



# This allows for the user to select from 3 programs  that will be organized into separate class structures.
selection = input('Choose between "caesar", "hashes", or "signature". Enter "quit" to exit.\nEnter:  ')

# Checks to see if the selection matches one of the expected cases. If not it prompts input again or 'quit' to exit. 
while selection != "quit":
    if selection.lower() == "caesar":
        # Selecting the CaesarSubstitution class to complete the substitution cipher.
        substitution = CaesarSubstitution()

        encrypted_msg = substitution.caesar_encrypt()
        print(f'\nThe encrypted message is below:\n{encrypted_msg}\n')

        decrypted_msg = substitution.caesar_decrypt(encrypted_msg)
        print(f'\nThe decrypted message is below:\n{decrypted_msg}\n')

        selection = input('\nChoose between "caesar", "hashes", or "signature". Enter "quit" to exit.\nEnter:  ')    

    elif selection.lower() == "hashes":
        hashyhash = HashingSHA()

        hashyhash.hash_encode()
        hashyhash.modify_msg()
        hashyhash.revert_msg()

        selection = input('\nChoose between "caesar", "hashes", or "signature". Enter "quit" to exit.\nEnter:  ')

    elif selection.lower() == "signature":
        signature = Signature()

        signature.sender()
        signature.tamper()
        signature.receiver()

        selection = input('\nChoose between "caesar", "hashes", or "signature". Enter "quit" to exit.\nEnter:  ')
    else:
        print('You have not selected an appropriate action.\n')
        selection = input('Choose between "caesar", "hashes", or "signature". Enter "quit" to exit.\nEnter:  ')