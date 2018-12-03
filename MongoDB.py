import pymongo

def query_user(username):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Mini_Project3_Mongo"]
    mycol = mydb["users"]
    if (mycol.count()==0):
        print("This User Name is Not Found In Table")
    else:
        for x in mycol.find():
            print(x)
# def add_data(username):
#     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#     mydb = myclient["Mini_Project3_Mongo"]
#     mycol = mydb["users"]


def delete_data(username):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Mini_Project3_Mongo"]
    mycol = mydb["users"]
    delete_name = input("Delete the Twitter ID:")

    mycol.delete_many({ "Twitter ID" : delete_name })



def delete_table():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Mini_Project3_Mongo"]
    mycol = mydb["users"]

    mycol.delete_many({})
    return


def search_keyword(username):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Mini_Project3_Mongo"]
    mycol = mydb["users"]
    twitterIDs=[]
    # username=input("Type the keyword u want to search: ")
    for twitterID in mydb.find():
        labels = twitterID.get('Labels')
        label = labels.split(',')
        if username in label:
            x = twitterID.get('Twitter ID')
            twitterIDs.append(x)
    if twitterIDs == []:
        print("There is no TitterID has the label (", username, ") in their images.")
    else:
        print("These TitterID has the label (", username, ") in their images:")
        # ignore the same users
        l = []
        for i in twitterIDs:
            if not i in l:
                l.append(i)
        print(l)

def show_all_data():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Mini_Project3_Mongo"]
    mycol = mydb["users"]
    mycol.find({})
    for x in mycol.find():
        print(x)
