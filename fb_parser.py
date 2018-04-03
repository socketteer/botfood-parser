#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
import glob
import os
import vocab_cleaner
import argparse 

def same_convo(timestamp1, timestamp2):
    date1 = timestamp1.getText().split()
    date2 = timestamp1.getText().split()
    if(date1[2] == date2[2]):
        return 1
    else:
        return 0

def parse_fb(input_path, output_file, my_name, enablegroupchat = 0):
    numsent = 0
    print('parsing %s\'s facebook messages...\n' % my_name)
    with open(output_file, 'w', encoding='utf-8') as output:
        for filename in glob.glob(os.path.join(input_path, '*.html')):
            with open(filename, mode='r', encoding = 'utf8') as html:
                soup = bs(html, "lxml")
            
            names = soup.find_all('span', attrs={'class':'user'})
            timestamps = soup.find_all('span', attrs={'class':'meta'})
            participants = soup.find('h3').next_sibling.split(', ')
            participants[0] = participants[0].split(': ')[1]
    
            
            if(len(participants) > 1):
                if(enablegroupchat == 0):
                    continue
            
            print(filename)
            author_name = my_name
                
            names.reverse()               
            i = 0
            for name in names:
                
                #if conversation happens on a new day
                if(i == 0):
                    output.write('<START>\n')
                elif(timestamps[i].get_text().split()[2] != timestamps[i-1].get_text().split()[2]):
                    output.write('<START>\n')
                
                message = names[i].parent.parent.find_next_sibling('p')
                #if author switches
                try:
                    if(author_name != names[i].getText()):
                        try:
                            author_name = names[i].getText()
                        except IndexError:
                            pass
                        output.write('<switch>\n')
                except IndexError:
                    pass
                
                if(message.getText()):
                    #if I am the author of the message
                    if(author_name == my_name):
                        output.write('>')
                        numsent = numsent+1 
                    string =  "%s\n" % message.getText()
                    string = vocab_cleaner.filter_non_ascii(string)
                    output.write(string)
                i += 1
        print("Facebook data parsed into botfood!")
        if(numsent == 0):
            print("WARNING: Did not find any messages authored by \"%s\". Make sure name is exactly the same as facebook name." %my_name)

parser = argparse.ArgumentParser()
parser.add_argument("inputfolder", metavar = 'I', help="name of folder containing facebook history .html files")
parser.add_argument("myname", metavar = 'N', help="your full facebook name")
parser.add_argument("-g", "--groupchat", help="enable include data from group chats in corpus",
                    action="store_true")
args = parser.parse_args()

input_folder = "./facebook/%s" % args.inputfolder
my_name = args.myname
output_file = "./corpus/facebook_%s.txt" %my_name.split(' ')[0]
enable_group_chat = args.groupchat

parse_fb(input_folder, output_file, my_name, enable_group_chat)
