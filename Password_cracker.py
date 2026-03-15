wordlist = [
        "password",
        "123456",
        "admin",
        "hunter2",
        "qwerty"
        ]
real_password = "hunter2"

def cracker(wordlist):
    attempts = 0
    for word in wordlist:
        print(f"Trying: {word}")
        attempts += 1
        if word == real_password:
            print("")
            print(f"Password found: {real_password}")
            print(f"Attempts: {attempts}")
            break
    else:
        print("\nPassword not found in wordlist")

cracker(wordlist)

guesses = [
"admin",
"password",
"123456",
"s3cur3",
"root"
]
password2 = "s3cur3"

def brute_force_sim(guesses):
    attempts = 0
    for guess in guesses:
        attempts += 1
        print(f"Trying: {guess}")
        if guess == password2:
            print("Access granted")
            break
        elif attempts >= 3:
            print("Account locked after 3 failed attempts")
            break

brute_force_sim(guesses)


