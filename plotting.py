import json 

def read_data(filename: str):
    f = open(filename)
    data = json.load(f)
    

if __main__ == "__main__":
    print
