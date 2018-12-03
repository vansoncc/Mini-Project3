import Tweepy1 as Tweepy
import MySQL
import MongoDB
import pymysql


def get_input_num():
    num=None
    while num is None:
        try:
            num = int(input("Type a number to choose function: "))
        except ValueError:
            print("Type a number to choose function")
    return num



def main():
    print("#############  Menu:  ############\n1.Add new TwitterID\n2.Delete a user\n3.Clean the database\n"
          "4.Search keyword\n5.Query Data\n6.Show All Data\n7. Return")
    data = get_input_num();

    if(data==1):
        username= input('Enter the username to Insert: ')
        base =int(input('1.MySQL   2.MongoDB: '))
        h = Tweepy.count_file_number()
        if(base ==1):
            Tweepy.main(username,h,1)
        elif(base ==2):
            Tweepy.main(username,h, 2)
        else:
            print('Wrong Input')
            return


    elif(data == 2):
        username = input('Enter the username to Delete: ')
        base = int(input('1.MySQL   2.MongoDB: '))
        if (base == 1):

            MySQL.delete_user(username)
        elif (base == 2):
            MongoDB.delete_data(username)
        else:
            print('Wrong Input')
            return

    elif(data==3):
        base = int(input('1.MySQL   2.MongoDB: '))
        if (base == 1):

            MySQL.Clean_table_data()

        elif (base == 2):

            MongoDB.delete_table()
        else:
            print('Wrong Input')
            return

    elif(data==4):
        username = input('Enter the keyword to search: ')
        base = int(input('1.MySQL   2.MongoDB: '))
        if (base == 1):
            MySQL.searchbykewords(username)
        elif (base == 2):

            MongoDB.search_keyword(username)
        else:
            print('Wrong Input')
            return

    elif(data==5):
        username = input('Enter the username to query: ')
        base = int(input('1.MySQL   2.MongoDB: '))
        if (base == 1):
            MySQL.query_user(username)
        elif (base == 2):

            MongoDB.query_user(username)
        else:
            print('Wrong Input')
            return

    elif(data==6):
        base = int(input('1.MySQL   2.MongoDB: '))
        if (base==1):
            MySQL.show_all()
        elif (base == 2):
            print('The data in MonogoDB:\n')
            MongoDB.show_all_data()
        else:
            print('Wrong Input')
            return


    elif (data == 7):

        return

main()






