import praw

#This info is needed to connect the account and the program
secret = ""
ID = ""

reddit = praw.Reddit(
    client_id=ID,
    client_secret=secret,
    user_agent="Reddit scraper",
    username="YOUR USERNAME",
    password="YOUR PASSWORD",
)

#Array where usernames will be stored
usernames = []


#Ask user for info,
print("-----HELLOOOO------")
numberkeywords = int(input("Number of keywords you wish to use? "))
keywords = []

#Itterate through the array and place words
for i in range(numberkeywords):
    keyword = input("Writte keyword number " + str(i+1) + " ").upper()
    keywords.append(keyword)

#Ask subreddit and number of posts
sub = input("Input the subreddit to search: ")
range_ = int(input("How many posts would you like to search through?: "))



#Type of search (i.e. if it should search only the title, content, or both
typeSearch = input("Do you want to search only the title, the content, or any? Only the title(T), Only the content(C), Any(A)")  .upper()


if typeSearch == "T" :
    print("Tittle it is")
elif typeSearch== "C":
    print("Content it is")
else:
    typeSearch = "B"
    print("Both it is then")



#Ask userr if they wish to save users who commented on post
UserWhoCommented = input("Do you wish to also message and save the users who commented in the post with the keyword? Y/N").upper()
if UserWhoCommented == "Y":
    print("Got it, user who commented will be saved. An array will be created where they will be stored")
    UserWhoCommented =  True
else:
    print("Got it, user who commented will NOT be saved")
    UserWhoCommented = False

UserCommented = []



#Type of keyword
typeKeywords = input("Does the post have to have every single keyword? Or just one? The default just one. Every keyword(E) Just one(O) ").upper()

#Start looking for posts, with EVERY keyword in them.
if typeKeywords == "E":
   print("Every keyword it is then!  \n")

   for post in reddit.subreddit(sub).new(limit=range_):
        d = 0
        for i in range(numberkeywords):

            #Slightly impractical, but the code will branch out in the 3 possibilities for search type of searach
            if typeSearch == "T":
              if keywords[i] in post.title.upper():
                d += 1
            elif typeSearch == "C":
                if keywords[i] in post.selftext.upper():
                    d += 1
            else:
                if keywords[i] in post.selftext.upper() or keywords[i] in post.title.upper():
                    d+=1

        if d == numberkeywords:
            print("Title of post: " + str(post.title))
            print("user " + post.author.name)
            print(post.url + "\n")
            if post.author.name not in usernames:
                usernames.append(post.author.name)

            ##Search trough comments and add users who commented
            if UserWhoCommented:
                for comment in post.comments:
                    if comment.author not in UserCommented and comment.author not in usernames:
                        UserCommented.append(comment.author.name)



#Look for post with one keyword or more
else:
    print("Only one keyword then! \n")

    for post in reddit.subreddit(sub).new(limit=range_):

        for i in range(numberkeywords):

            #check every single combination, if one of them is true, proceed with code
            if typeSearch == "T" and keywords[i] in post.title.upper() or typeSearch == "C" and keywords[i] in post.selftext.upper() or typeSearch == "B" and (keywords[i] in post.selftext.upper() or keywords[i] in post.title.upper()):
                    print("Title of post: " + str(post.title))
                    print("user " + post.author.name)
                    print(post.url + "\n")

                    if  post.author.name not in usernames:
                        usernames.append(post.author.name)

                    ##Search trough replies and add users who commented
                    if UserWhoCommented:
                        for comment in post.comments:
                            if comment.author not in UserCommented and comment.author not in usernames:
                                UserCommented.append(comment.author.name)

                    break


print("Users who posted: ")
print(usernames)

print("Users who Commented: ")
print(UserCommented)


Ask = input("Now, wold you like to send a private message to the users? Y/N ").upper()
if Ask == "N":
    print("Got it, hope this information was helpful then :)")
    exit()

##Now we message them, it will be imposible to message some user though, as they might have a whitelist turned on
Message = input("Okay, now please write the message you wish to send")
Subject = input("Input the subject of this mail")
print("This message will now be sent to both users who posted a post with the keyword, and users who commented in set post")

for i in usernames:
    try:
        reddit.redditor(i).message(subject=Subject, message=Message)
    except:
        print("We where unable to message " + i + " they probably have a whitelish turned on")

print("Message sent to usernames who posted ")

for i in UserCommented:
    try:
        reddit.redditor(i).message(subject=Subject, message=Message)
    except:
        print("We where unable to message " + i + " they probably have a whitelist turned on")
print("Message sent to usernames who commented ")

print("Job done :))")











