# botfood-parser
Scripts to parse Facebook and Skype message history for training chatbots with [socketteer/neural-chatbot]

## Usage

### Getting Facebook data

On Facebook desktop, click the down arrow at the upper right corner of the screen and go to Settings -> General. Click the link that says "Download a copy of your Facebook data" and then click "Start my archive." It will take anywhere from a few minutes to a few hours for Facebook to compile your data. You should get an email and a notification when it is ready for download.

Download the zip file called facebook-<your_username>.zip. The "messages" folder in the zip file is the only part you will need. 

Create a new folder in botfood-parser/facebook (you may call it your name or your facebook username). Copy all the html files in "messages" to this folder. Run the fb_parser.py script using:

```bash
$ python fb_parser.py <name of new folder> <your facebook display name>
```

Make sure the name argument is exactly the same as your display name for Facebook, otherwise the script will not parse the data correctly! You will get a warning if it seems like you used the wrong name.

You can use the -g or --groupchat flag to enable parsing data from groupchats. This is not recommended unless you are very active in most of the groupchats you're in.

Running the above command will generate a text file in botfood-parser/corpus called facebook-<your_first_name>.txt. This prepared botfood.

### Getting Skype data

You will need Skype classic on desktop to export your Skype history. Select Tools -> Options and select Privacy, then Export Chat History. Copy the csv file to botfood-parser/skype.

Run the skype_parser.py script using:

```bash
$ python skype_parser.py <skype_username> <csv_file>
```

Running the above command will generate a text file in botfood-parser/corpus called facebook-<skype_username>.txt. This prepared botfood.
