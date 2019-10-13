#!/usr/bin/env python3

from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv

#local python files
import emailAlert
import configs

#make a get request to Alamo's webserver
session = HTMLSession()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'}
resp = session.get("https://drafthouse.com/ajax/.signature-series-past/86", headers=headers)

#use beautiful soup to parse the html
soup = BeautifulSoup(resp.html.html, "lxml")
titleTags = soup.find_all(class_="Card-overlayHeading")
imgTags = soup.find_all("img")

#makes a list of all movie titles
alamoTitles = []
for tag in titleTags:
    alamoTitles.append(tag.text.encode("cp437", "ignore").strip().decode('cp437'))

#makes a list of all movie poster links
alamoPosters = []
for tag in imgTags:
    alamoPosters.append("https:" + tag['src'].encode("cp437", "ignore").strip().decode('cp437'))

#if there were no movies found there was a problem and an error email is sent
if(len(alamoTitles) <= 0 or (len(alamoTitles) != len(alamoPosters))):
    emailAlert.htmlSend(from_addr= configs.fromAddress, 
          to_addr = configs.toAddress,
          subject      = "Error Getting Alamo Recommended Movies!", 
          message      = "", 
          login        = configs.login)
    exit()

#makes a list of the movies already saved locally in movies.csv
oldTitles = []
oldPosters = []
with open('movies.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        oldTitles.append(row[0])
        oldPosters.append(row[1])

#filters the movies so that newTitles only has movies found on the Alamo's server that were not saved locally
newTitles = list(set(alamoTitles) - set(oldTitles))
newMovies = []
for i in range(0, len(newTitles)):
    newTitle = newTitles[i].encode("cp437", "ignore").strip().decode('cp437')
    newPoster = alamoPosters[alamoTitles.index(newTitles[i])].encode("cp437", "ignore").strip().decode('cp437')
    newMovies.append([newTitle, newPoster])

#if there were new movies found an email is sent and the new movies are saved to the csv file
if(len(newMovies) > 0):
    message = "<html><br>"
    subject = "Alamo Recommends: "
    for movie in newMovies:
        message += "<h1>" + movie[0].title() + "</h1>"
        message += "<img src='" + movie[1] + "'><br>"
        subject += movie[0].title() + ", "
    message += "<a href='" + configs.alamoLocation + "'>Check out these movies Here!</a></html>"
    subject = subject[:-2]

    emailAlert.htmlSend(from_addr= configs.fromAddress, 
          to_addr = configs.toAddress,
          subject      = subject, 
          message      = message, 
          login        = configs.login)

    with open('movies.csv', mode='a', newline='') as file:
        csvWriter = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for movie in newMovies:
            csvWriter.writerow(movie)



