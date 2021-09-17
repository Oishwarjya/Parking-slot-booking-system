from django.conf import settings
from datetime import datetime
import hashlib, binascii
import pymongo
import random
import time

from dotenv import load_dotenv
import os

from pymongo.message import update

load_dotenv()

class UserEntry():
    def __init__(self) -> None:
        """
        Connect to MongoDB
        """
        client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        self.db = client["Parking-Slot-Booking"]["User-Details"]

    def insert_user(self, name: str, email: str, pwd: str, dob: str):
        """Insert user into collection

        Args:
            name : User Name
            email : User Email ID
            pwd : User Account Password
            dob : User Date Of Birth

        Returns:
                void : inserts user into db
        """
        # print("UNHASHED Password: ", pwd)
        pwd = self.hash_password(pwd)
        # print("HASHED Password: ", pwd)

        rec ={
            'Username': name,
            'Email':email,
            'Password': pwd,
            'DOB':dob
        }
        self.db.insert_one(rec)


    def check_user_exists(self, email: str) -> bool:
        """Checks if user exists in database

        Args:
            email : User Email ID

        Returns:
            bool
        """
        if value := self.db.find_one(
                {"Email": email}
        ):
            #return value
            return True
        return False


    def add_verif_code(self, email: str, check_recursive_correctness: int) -> int:
        """Adds verification code & timestamp for reset password functionality

        Args:
            email : User Email ID
            check_recursive_correctness : Value to check recursive function

        Returns:
            int : Verification code generated for the user
        """
        # To check if recursive call is working correctly 
        # if check_recursive_correctness==0:
        #     verif_code = 883330
        # else:
        #    verif_code = random.randint(100000, 999999)
        verif_code = random.randint(100000, 999999)
        
        print("VERIF CODE BEFORE IF:", verif_code)

        if value := self.db.find_one(
                {"verif_code": verif_code}
        ):
            print("Verification code already exists, Entering RECURSIVE function")
            self.add_verif_code(email, 1)

        else:
            print("ELSE VERIF CODE:", verif_code)
            #verif_code_init_timestamp = datetime.strftime(datetime.now(), format="%H:%M:%S")
            verif_code_init_timestamp = datetime.now()
            print("Current DATETIME:", verif_code_init_timestamp)
            self.db.update_one(
                {"Email":email},
                {"$set": {
                    "verif_code": verif_code, 
                    "timestamp_created": verif_code_init_timestamp
                }
            })

            print(self.db.find_one({"Email": email}))
            return verif_code


    def check_verif_code(self, code: int) -> bool:
        """Checks if verification code is valid

        Args:
            code : Verification Code
            
        Returns:
            bool
        """
        #Time when user enters the verification code
        verif_code_entry_time = datetime.now()

        if value := self.db.find_one(
                {"verif_code": code}
        ):
            email = value["Email"]
            #Time when verification code was generated
            timetamp_created = value["timestamp_created"]

            if (verif_code_entry_time-timetamp_created).total_seconds() > 3600:
                self.db.update_one(
                    {"Email": email},
                    {"$unset": {
                        "verif_code": "",
                        "timestamp_created": ""
                    }
                })
                print("Verification Code Expired, Try Again To Generate New Code")
                return False
            else:
                print("Removed Verification Code & Timestamp as code was used successfully")
                return True

        print("Verif Code doesnt match or may not exist")
        return False

        
    def hash_password(self, pwd: str) -> str:
        """Hashes password using salted password hashing (SHA512 & PBKDF_HMAC2)

        Args:
            pwd : Password to be hashed
            
        Returns:
            str : Hashed password
        """
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        print("SALT1: ", salt)
        pwd_hash = hashlib.pbkdf2_hmac('sha512', pwd.encode('utf-8'), salt, 100000)
        pwd_hash = binascii.hexlify(pwd_hash)
        final_hashed_pwd = (salt + pwd_hash).decode('ascii')
        return final_hashed_pwd


    def check_hash(self, email: str, pwd: str) -> bool:
        """Verifies hashed password with stored hash & verifies user before login

        Args:
            email : Email ID of User
            pwd : Password to be checked
            
        Returns:
            bool
        """
        if value := self.db.find_one(
                {"Email": email}
        ):
            dbpwd = value['Password']
            #print("DBPWD: ", dbpwd)

            #PASSWORD HASH AND SALT STORED IN DATABASE
            salt = dbpwd[:64]
            #print("SALT2: ", salt)
            dbpwd = dbpwd[64:]
            #print("Stored password hash: ", dbpwd)
            
            #PASSWORD HASH FOR PASSWORD THAT USER HAS CURRENTLY ENTERED
            pwd_hash = hashlib.pbkdf2_hmac('sha512', pwd.encode('utf-8'), salt.encode('ascii'), 100000)
            pwd_hash = binascii.hexlify(pwd_hash).decode('ascii')
            #print("pwd_hash: ", pwd_hash)
            
            if pwd_hash==dbpwd:
                print("Hash Match")
                return True
            else:
                print("Hash does NOT match")
                return False

        else:
            print("User NOT in DB")
            return False


    def reset_password(self, pwd: str, code: int) -> bool:
        """Resets user password to updated password and deletes verification code

        Args:
            pwd : New Password
            code : Verification code
            
        Returns:
            bool
        """
        if value := self.db.find_one(
                {"verif_code": code}
        ):
            email = value["Email"]
            self.db.find_one_and_update(
                {"Email": email},
                update={
                    "$set": {
                        "Password": self.hash_password(pwd)
                    },
                    "$unset": {
                        "verif_code": "",
                        "timestamp_created": ""
                    }
                }
            )
            print("Password Reset Successfully & verification code deleted")
            return True
        print("Incorrect Verification Code")
        return False
    



s= UserEntry()
#print(S.check_user_exists(self,'aac@gmail.com'))
# insert_user('Oishwarjya', 'ob7029@srmist.edu.in', 'apple123', '22 Nov 2001')
s.insert_user('Aradhya', 'abc@gmail.com', 'balls', '23 Aug 2002')
# print(check_hash('ob7029@srmist.edu.in', 'apple123'))
# print(check_hash('nv9824@srmist.edu.in', 'abc123AB'))
# print(check_hash('nv9824@srmist.edu.in', 'abc123ABC'))  
# verif_code = add_verif_code("nv9824@srmist.edu.in", 0)
# print(check_verif_code(635594))
# reset_password("abc123ABC", 217352)