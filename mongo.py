from pymongo import MongoClient
from datetime import datetime
import json
import sys
import rsa

class TestMongo(object):

     def __init__(self):
         self.clint = MongoClient()
         self.db = self.clint['test']

     def add_one(self,json_input,db_name):
        """データ挿入"""
        post = json_input
        return self.db[db_name].insert_one(post)

def main():
    obj = TestMongo()

    # jsonファイルの読み出し
    input = sys.argv[1]
    json_open = open(input,'r')
    json_load = json.load(json_open)
    
    rest = obj.add_one(json_load,input[2])
    print(rest)

if __name__ == '__main__':
    main()