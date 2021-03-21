import os
import os.path
import discord
from discord.ext.commands.core import check
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from discord.ext import commands, tasks
from itertools import cycle
import asyncio
from pathlib import Path
import json
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
          "https://www.googleapis.com/auth/classroom.coursework.students", "https://www.googleapis.com/auth/classroom.announcements.readonly",
          "https://www.googleapis.com/auth/classroom.announcements"]


# This is going to be our creditals
creds = None

# Creating our client that will alow us to run commands
client = commands.Bot(command_prefix="", case_insensitive=True)

# A variable to check the author that is sending the message
msg_author = {"name": ""}
announcment = False

# Create the search engine
service = None


# This gonna work when the user sign in (is online)
@client.event
async def on_ready():
    # We are chainging the status of the bot, and displaying this messaage
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("use gc£help to get help"))


# This command is going to be responsible for showing all the commands that the bot use
@client.command(name="gc£help")
async def get_help(ctx):
    my_embed = discord.Embed(color=0x00ff00)
    my_embed.set_author(name="Help command")

    # sign in command
    my_embed.add_field(
        name=" gc£sign_in ", value="This command is to sign in so the bot can get access to your data", inline=False)

    my_embed.add_field(
        name=" gc£re_sign_in ", value="This command is to resign in in case you want to log in with another account", inline=False)

    # Show courses command
    my_embed.add_field(
        name=" gc£courses", value="This command will show you all the courses that you have", inline=False)

    # Get announcement command
    my_embed.add_field(
        name="gc£set_announcement", value="""This command will let you create an announcement channel for one of your courses,
        you will get a notfiction if something new happens.""", inline=True)

    await ctx.send(embed=my_embed)


# This code is to check if the person who called the command is the
# same person who loged in
def check_author(author):
    # Checking if the file exists and comparing the user name for the person who
    # loged in with the person who called the command
    if os.path.exists("name.json"):
        data = Path("name.json").read_text()
        data_1 = json.loads(data)

        return author == data_1["name"]

    return False


@client.command(name="gc£sign_in")
async def _log_in(ctx):
    global creds, msg_author

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # print(check_author(ctx.author))

    if os.path.exists('token.json') and check_author(str(ctx.author)):
        # setting the credits to defult and removing the token file in case they exists
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        await ctx.send("You're already loged")

    else:
        # In case there are not exist, the script won't get an error
        try:
            creds = None
            os.remove("token.json")
            os.remove("name.json")

        except:
            pass

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        # Checking if the creds is expired, is theier a creds
        if creds and creds.expired and creds.refresh_token:
            # Refresheing the token acess
            creds.refresh(Request())

        else:
            # Creating a flow object from the credentials file
            #  so we can use it to get access to the user data
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes=SCOPES, redirect_uri="urn:ietf:wg:oauth:2.0:oob")

            # Runing the server so the user can log in and returning the token acess
            auth_url = flow.authorization_url(prompt="consent")

            # Sending the url to the user
            await ctx.send("Please go to this url to sign in: {} ".format(auth_url[0]))

            await ctx.send("Please enter the authorizen code: ")

            # Creating a function to check the message getting from the user
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            msg = await client.wait_for("message", check=check)
            msg_author["name"] = str(msg.author)

            # With this code so even if the code is wrong and an error appears
            # So the script won't go down and it will keep runing
            try:
                # Completes the Authorization Flow and obtains an access token
                flow.fetch_token(code=msg.content)

                # Getting the credentials
                creds = flow.credentials

                with open("token.json", "w") as token:
                    token.write(creds.to_json())

                with open("name.json", "w") as name:
                    json.dump(msg_author, name)
                # data1 = json.dumps(msg_author)
                # Path("name.json").write_text(data1)
                print(msg_author)

                await ctx.send("Successfully loged")

            except Exception as e:
                await ctx.send(e)

# This command is for you if you want to sign in with another account


@client.command(name="gc£re_sign_in")
async def reload(ctx):
    try:
        os.remove("name.json")
        os.remove("token.json")
    except:
        pass

    # Creating a flow object from the credentials file
    #  so we can use it to get access to the user data
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', scopes=SCOPES, redirect_uri="urn:ietf:wg:oauth:2.0:oob")

    # Runing the server so the user can log in and returning the token acess
    auth_url = flow.authorization_url(prompt="consent")

    # Sending the url to the user
    await ctx.send("Please go to this url to sign in: {} ".format(auth_url[0]))

    await ctx.send("Please enter the authorizen code: ")

    # Creating a function to check the message getting from the user
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for("message", check=check)
    msg_author["name"] = str(msg.author)

    # With this code so even if the code is wrong and an error appears
    # So the script won't go down and it will keep runing
    try:
        # Completes the Authorization Flow and obtains an access token
        flow.fetch_token(code=msg.content)

        # Getting the credentials
        creds = flow.credentials

        with open("token.json", "w") as token:
            token.write(creds.to_json())

        with open("name.json", "w") as name:
            json.dump(msg_author, name)
        # data1 = json.dumps(msg_author)
        # Path("name.json").write_text(data1)
        print(msg_author)

        await ctx.send("Successfully loged")

    except Exception as e:
        await ctx.send(e)


# With this line of code so we can avoid repeation in the code
def get_courses():
    global service
    # Setting the creds in case it's NONE
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Creating a resource object that we use to send a request
    service = build('classroom', 'v1', credentials=creds)

    # Calling the Classroom API, and returning a dictionary
    results = service.courses().list(pageSize=10).execute()
    return results.get('courses', [])


@client.command(name="gc£courses")
async def show_couses(ctx):
    # If the person who called the command is not the same person that loged in
    # So this message will show up, same thing if you are not loged in
    if not check_author(str(ctx.author)):
        await ctx.send("You didn't log in, do that first with the command: gc£sign_in")

    else:
        # Getting the courses
        courses = get_courses()

        if not courses:
            await ctx.send('No courses found.')
        else:
            # Creating an embed to show all the courses at once
            my_embed = discord.Embed(title="Courses", color=0x00ff00)
            my_fields = []
            for course in courses:
                my_fields.append(my_embed.add_field(
                    name=" \u200b ", value=course["name"], inline=False))
            await ctx.send(embed=my_embed)


async def announcements_task(ctx, course_iterator):
    skip = True

    # Getting the current course
    current_course = next(course_iterator)

    await ctx.send("Please set announcement channel for {} (set to stop or skip to skip)".format(current_course[0]))

    # Getting the courses
    courses = get_courses()

    # Creating an inner function to get the number of announcement in the current
    # The porpuse is to avoid repeation
    def get_length_announcements():
        # Here we are returning the current announcements in the current course
        announcements = service.courses().announcements().list(
            courseId=current_course[1]).execute()

        # Returning the length of the list
        return [len(announcements["announcements"]), announcements["announcements"][0]["alternateLink"]]

    # The current length of the announcements
    current_nr_of_announcemets = get_length_announcements()
    # msg = msg.content.lower()

    # Checking the message
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    # Waiting the user to replay
    msg = await client.wait_for("message", check=check)
    while True:
        # If this is true, so we are going to check the announcements
        if msg.content.lower() == "set" or not skip:
            try:
                length_2 = get_length_announcements()[0]

                # If this returns true, so that means that there is a new announcement is published
                if length_2 > current_nr_of_announcemets:
                    await ctx.send("A new announcement: link {}".format(get_length_announcements()[1]))
                    current_nr_of_announcemets = length_2

                else:
                    pass

            # If any erorr appears so this gonna take care of it
            except Exception as e:
                await ctx.send(e)

            # This will break the loop for 30 sekunds, this loop will run 120 per hour
            # Which means that it will check the classroom 2 times per minute
            await asyncio.sleep(5)

        elif msg.content.lower() == "skip" or skip:
            try:
                # We get the next course in the list, and then we send to the user
                current_course = next(course_iterator)
                await ctx.send("Please set announcement channel for {} (set to stop or skip to skip)".format(current_course[0]))

                msg = await client.wait_for("message", check=check)

                if msg.content.lower() == "set":

                    # Getting the number of messages
                    current_nr_of_announcemets = get_length_announcements()[0]
                    skip = False

                elif msg.content.lower() == "skip":
                    skip = True

            # If there is no more courses, so this gonna work
            except Exception:
                await ctx.send("There is no more courses.")
                break

        await client.process_commands(msg)


@client.command(name="gc£set_announcement")
async def set_announcement(ctx):
    if not check_author(str(ctx.author)):
        await ctx.send("You didn't log in, do that first with the command: gc£sign_in")

    else:
        await ctx.send("Working...")
        # Returning the courses
        courses = get_courses()

        # Here we are going to store the name and the ID of the course
        course_info = []

        # Converting the list to an iterator
        course_iterator = iter(course_info)

        # Getting the name of each course
        for course in courses:
            course_info.append((course["name"], course["id"]))

        # Putting it into a try box to handle errors
        try:

            # Creating a task that is gonna check if there is any new announcements
            client.loop.create_task(announcements_task(
                ctx, course_iterator))

        except Exception as e:
            await ctx.send(e)

client.run(bot_token)
