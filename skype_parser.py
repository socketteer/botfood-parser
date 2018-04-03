import csv
import re
import vocab_cleaner
import argparse 

def cleanMarkup(string):
    string = re.sub("&apos;", "\'", string)
    string = re.sub("&quot;", "\"", string)
    string = re.sub("<ss type=\"heart\">&lt;3</ss>", "<3", string)
    string = re.sub("<ss type=\"wink\">;\)</ss>", ";)", string)
    string = re.sub("<ss type=\"smile\">:\)</ss>", ":)", string)
    string = re.sub("<ss type=\"cry\">;\(</ss>", ":'(", string)
    string = re.sub("<ss type=\"surprised\">:O</ss>", ":O", string)
    string = re.sub("<ss type=\"laugh\">:D</ss>", ":D", string)
    string = re.sub(r"<ss type=.+?</ss>", "", string)
    string = re.sub("<b raw_pre=\"\*\" raw_post=\"\*\">", "*", string)
    string = re.sub("</b>", "*", string)
    string = re.sub("<URIObject uri=.+?</URIObject>", "", string)
    string = re.sub(r"<meta type=.+?>", "", string)
    string = re.sub("<a href=\".+?\">", "", string)
    string = re.sub("</a>", "", string)
    string = re.sub("<.+?>[\S\s]+?<.+?>", "", string)
    string = re.sub("</.+?>", "", string)
    return string


ConvoID = []
AuthorName = []
Content = []
Timestamp = []

parser = argparse.ArgumentParser()
parser.add_argument("username", metavar = 'U', help="skype username")
parser.add_argument("filename", metavar = 'F', help=".csv file containing skype history")
args = parser.parse_args()

username = args.username
filename = args.filename

output_file = './corpus/skype_%s.txt' %username
input_file = './skype/%s' %filename

with open(input_file) as skypedata:
    with open(output_file, 'w', encoding='utf-8') as output:
        csvReader = csv.reader(skypedata)
        for row in csvReader:
            ConvoID.append(row[0])
            AuthorName.append(row[3])
            Timestamp.append(row[5])
            Content.append(row[6])
     
        ConvoID = ConvoID[1:]
        AuthorName = AuthorName[1:]
        Content = Content[1:]
        for i, message in enumerate(Content):
            Content[i] = cleanMarkup(message)
            Content[i] = vocab_cleaner.filter_non_ascii(Content[i])
            if(Content[i].isspace() or not Content[i]):
                continue
            if(i < 1 or (not ConvoID[i-1] == ConvoID[i])):
                output.write("<START>\n")
            elif(i > 1 and (int(Timestamp[i]) - int(Timestamp[i-1])) > 10000000):
                output.write("<START>\n")
            if(i < 1 or (not AuthorName[i-1] == AuthorName[i])):
                output.write("<switch>\n")
            if(Content[i]):
                if(AuthorName[i] == username):
                    output.write(">")
                
            output.write("%s\n" % Content[i])
        print("Skype data parsed into botfood!")
                
