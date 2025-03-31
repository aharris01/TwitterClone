from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from bitarray import bitarray
import mmh3
import math
import os


# The following implementation of a Bloom filter was taken from https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/
class BloomFilter:
    def __init__(self):
        self.falsePositive = 0.05
        self.itemCount = 499
        self.size = self.get_size(self.itemCount, self.falsePositive)
        self.hashCount = self.get_hash_count(self.size, self.itemCount)
        self.bitArray = bitarray(self.size)

        self.bitArray.setall(0)

    def add(self, item):
        """
        Add an item in the filter
        """
        digests = []
        for i in range(self.hashCount):

            # create digest for given item.
            # i work as seed to mmh3.hash() function
            # With different seed, digest created is different
            digest = mmh3.hash(item, i) % self.size
            digests.append(digest)

            # set the bit True in bitArray
            self.bitArray[digest] = True

    def check(self, item):
        """
        Check for existence of an item in filter
        """
        for i in range(self.hashCount):
            digest = mmh3.hash(item, i) % self.size
            if self.bitArray[digest] == False:

                # if any of bit is False then,its not present
                # in filter
                # else there is probability that it exist
                return False
        return True

    @classmethod
    def get_size(self, n, p):
        """
        Return the size of bit array(m) to used using
        following formula
        m = -(n * lg(p)) / (lg(2)^2)
        n : int
            number of items expected to be stored in filter
        p : float
            False Positive probability in decimal
        """
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @classmethod
    def get_hash_count(self, m, n):
        """
        Return the hash function(k) to be used using
        following formula
        k = (m/n) * lg(2)

        m : int
            size of bit array
        n : int
            number of items expected to be stored in filter
        """
        k = (m / n) * math.log(2)
        return int(k)


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

bl = BloomFilter()

baseDir = os.path.dirname(os.path.abspath(__file__))

filePath = os.path.join(baseDir, "static", "500-worst-passwords.txt")

with open(filePath, "r") as f:
    for line in f:
        password = line.rstrip("\n")
        bl.add(password)
