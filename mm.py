import random
import time

class DataTable():
    size = 10000
    def __init__(self):
        self.table = list([0] * self.size)
        self.__candidates = self.size

    def remove_candidate(self, num):
        if self.table[num] == 0:
            self.table[num] = 1
            self.__candidates -= 1

    def candidate_number(self):
        return self.__candidates


class InputReader:
    def getInput(self, dtype = str, msg = "Input: ", valid = None):
        data = None
        while data is None:
            inp = raw_input(msg).strip()
            try:
                data = dtype(inp)
            except:
                print("[ERROR] Incorrect input given for %s" % dtype)
            if dtype is str and len(data) == 0:
                print ("[ERROR] Input length is 0.")
                data = None
            if (not valid is None) and not(data in valid):
                print("[ERROR] Invalid data.")
                data = None
        return data

class MatchCategories:
    FULL = "B"
    PARTIAL = "F"

class MasterMinder():
    __datatable = None
    __secret = ""
    __guess = ""
    __reader = None
    __evaluated_guess = ""
    __matches = MatchCategories()
    __full = 0
    __partial = 0

    def __init__(self):
        self.__datatable = DataTable()
        self.__reader = InputReader()
        random.seed(time.time())
        self.__generateSecret()

    def __reset(self):
        self.__datatable = DataTable()
        self.__generateSecret()

    def __generateSecret(self):
        num = random.randint(0, 9999)
        self.__secret = self.__num_to_string(num)
        #print("Secret: %s" % self.__secret)

    def __num_to_string(self, num):
        retvalue = None
        try:
            n = int(num)
            retvalue = "%04d" % n
        except:
            pass
        return retvalue

    def __update_table(self):
        for i in range(self.__datatable.size):
            f, p = self.__evaluate_guess(secret = self.__guess, guess = self.__num_to_string(i))
            if (f, p) != (self.__full, self.__partial):
                self.__datatable.remove_candidate(i)
        return self.__datatable.candidate_number()

    def start_game(self):
        self.__full = 0
        count = 0
        while self.__full < 4:
            g = self.__reader.getInput(msg ="Please give a guess: " )
            g = self.__num_to_string(g)
            if g is None:
                continue
            else:
                self.__guess = g
            self.__full, self.__partial = self.__evaluate_guess(secret = self.__secret, guess = self.__guess)
            rem = self.__update_table() 
            count += 1
            print("%d) %s %d %d [%d left]" %(count, self.__guess, self.__full, self.__partial, rem))
            if self.__full == 4:
                print("Nice! You have found the code by only %d guesses." % count)
                response = self.__reader.getInput(msg ="Do you want to play again? (y/n): ", valid = ["y", "n"])
                if response == "y":
                    self.__full = 0
                    self.__reset()
                    count = 0
        print("Thanks for playing. Bye.")

    def __evaluate_guess(self, secret, guess):
       a = list(secret)
       b = list(guess)
       if a == b:
           return 4, 0
       for index, e in enumerate (zip(a,b)):
            if e[0] == e[1]:
                a[index] = self.__matches.FULL
                b[index] = self.__matches.FULL
       for index, e in enumerate(a):
           if (not e in [self.__matches.FULL, self.__matches.PARTIAL]) and e in b:
               a[index] = self.__matches.PARTIAL
               ix = b.index(e)
               b[ix] = self.__matches.PARTIAL
       fullmatch = a.count(self.__matches.FULL)
       partmatch = a.count(self.__matches.PARTIAL)
       return fullmatch, partmatch

    @property
    def secret(self):
        return self.__secret
    @property
    def guess(self):
        return self.__guess


if __name__ == "__main__":
    mm = MasterMinder()
    mm.start_game()

