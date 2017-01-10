'''
Created on Nov 9, 2016

@author: mandar
'''
import urllib2, re
from bs4 import BeautifulSoup
import sys
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree


baseurl="https://www.kickstarter.com/discover/advanced?term=software&woe_id=0&sort=magic&seed=2463224&page="
##https://www.kickstarter.com/discover/advanced?term=software&woe_id=0&sort=magic&seed=2463224&page=
##https://www.kickstarter.com/projects/search?utf8=%E2%9C%93&term=Educational+Communication+Software
PageNum=1


refcount=0
Errorcount=0
projectList=dict()

while PageNum<170:
    newurl=baseurl+str(PageNum)
    print newurl
    #if  PageNum==3:
    #    programPause = raw_input("Press the <ENTER> key to continue...")
    basehtml=urllib2.urlopen(newurl).read()
    baseSoup=BeautifulSoup(basehtml,"html.parser")
    listsoup=baseSoup.find('ul',attrs={"id":"projects_list"})
    tableh = listsoup.findAll('li',attrs={"class":"project col col-3 mb3 mb7-sm"})
    root=Element('data')
    tree=ElementTree(root)        
    for x in tableh:
        try:
        
            if (x.find('div',attrs={"class":"project-profile-title text-truncate-xs"})) is None: 
                #if  (PageNum==26):
                #    print("error")
                if ((x.find("div",{"class": "project-status project-failed"}) is not None) or (x.find("div",{"class": "project-stats-container"}).find("div",{"class": "project-status project-canceled"}) is not None )):
                    project=Element('UnsuccessfulProject')
                    y = x.find('h6',attrs={"class":"project-title"})
                    #try:                                
                    Pro=(y.find('a').get('href')).split("?", 1)[0]
                    url="https://www.kickstarter.com"+Pro                
                    print(url)
                    if (url=="https://www.kickstarter.com/projects/2000266279/karate-do-software-for-tournaments"):
                        print("error")
                    ProjectID=Pro.split("/")[2]                
                    if ProjectID in projectList:
                        projectList[ProjectID]= projectList[ProjectID]+1
                    else:    
                        projectList[ProjectID]=1                    
                        #projectList.append(ProjectID)
                        #if (url =="https://www.kickstarter.com/projects/675352435/destin-learning-free-s-w-training-learning-sans-lo"):                
                        
                        html=urllib2.urlopen(url).read()
                        soup=BeautifulSoup(html,"html.parser")
                        
                        ##title of the project and create a text file with title as name.
                        root.append(project)                    
                        ##Title of the project                    
                        hTitle=y.text
                        #print(y.text)
                        Title=Element('Title')
                        project.append(Title)
                        Title.text=hTitle
                        ## total pledged money till current
                        if (soup.find("div",{"class": "js-pledged"})) is None:
                            pledgedMoney=soup.find("span",{"class": "js-usd_pledged"}).text
                        else:
                            pledgedMoney=soup.find("div",{"class": "js-pledged"}).text    
                        pledgedmoney=Element('pledgedmoney')
                        project.append(pledgedmoney)
                        pledgedmoney.text=pledgedMoney
                        
                        #Project ID
                        projectID=Element('projectID')
                        project.append(projectID)
                        projectID.text=ProjectID
                        ##Total Cost of the Project
                        TotalCost=Element('TotalCost')
                        project.append(TotalCost)
                        if (soup.find("span",{"class": "money usd no-code"})) is None:
                            TotalCost.text=soup.findAll("span",{"class":"money"})[1].text
                        else:
                            TotalCost.text=soup.find("span",{"class": "money usd no-code"}).text
                        #print(TotalCost.text)
                        ##total number of Backers
                        backers=Element('backers')
                        project.append(backers)
                        
                        if (soup.find("span",{"class": "num f2 medium js-backers_count"})) is None:
                            backers.text=soup.find("div",{"id": "backers_count"}).text
                        else:
                            backers.text=soup.find("span",{"class": "num f2 medium js-backers_count"}).text 
                        
                        #print(backers.text)
                        
                        daysLeft=soup.find("div",{"id": "backers_count"}).text    
                        daysleft1=Element('dayleft')
                        project.append(daysleft1)
                        daysleft1.text=str(daysLeft)
                                                            
                        ##Comments
                        Comment=""
                        commentCount=0
                        urlcomments = url +str("/comments")
                        
                        htmlcomments=urllib2.urlopen(urlcomments).read()
                        commentsoup=BeautifulSoup(htmlcomments, "html.parser")                    
                        
                        commentable = commentsoup.findAll('li',attrs={"class":"NS_comments__comment comment item py3 mb3"})
                        for x in commentable:
                            for f in x.findAll('p'):
                                if (commentCount>0):
                                    Comment += " "+f.text
                                    commentCount += 1
                                print(Comment)    
            
                        latestcommentable = commentsoup.findAll('li',attrs={"class":"NS_comments__comment comment item latest_comment mb3 py3"})        
                        for y in latestcommentable:
                            for f in y.findAll('p'):                        
                                Comment += " "+f.text
                                commentCount += 1
                                print(Comment)    
        
                        earliestcommentable = baseSoup.findAll('li',attrs={"class":"NS_comments__comment comment earliest_comment item mb3 py3"})
                        for y in earliestcommentable:
                            for f in y.findAll('p'):                                           
                                Comment += " "+f.text
                                commentCount += 1
                                print(Comment)  
                            
                        comments=Element('comments')
                        project.append(comments)
                        comments.text=Comment
                        countcomments=Element('countcomments')
                        project.append(countcomments)
                        countcomments.text=str(commentCount)               
                        print(str(commentCount))
                        ##Campiagn - Description
                        urlcampaign =url+str("/description")
                        #print (urlcampaign)
                        #if urlcampaign=="https://www.kickstarter.com/projects/1309842538/transformers-more-than-meets-the-eye-youtube-serie/description":
                        #    print "hugh"
                        htmlcampaign=urllib2.urlopen(url).read()
                        campaignsoup=BeautifulSoup(htmlcampaign, "html.parser")
                        ##if (campaignsoup.find("div",{"class": "hidden js-campaign-state js-campaign-state__canceled"})) is None:
                        ##    table = campaignsoup.findAll('div',attrs={"class":"col col-8"})[2]
                        ##else:
                        table = campaignsoup.find('div',attrs={"class":"col col-8 description-container"})    
                        #table = campaignsoup.findAll('div',attrs={"class":"col col-8"})[1]
                        Campaigndescription=""
                        for y in table.findAll('p'):
                            Campaigndescription +=y.text                 
                        for p in table.findAll('h1'):
                            Campaigndescription +=p.text
                        for p in table.findAll('li'):
                            Campaigndescription +=p.text
                        for p in table.findAll('b'):
                            Campaigndescription +=p.text
                        for p in table.findAll('h2'):
                            Campaigndescription +=p.text
                        for p in table.findAll('h3'):
                            Campaigndescription +=p.text
                        for p in table.findAll('i'):
                            Campaigndescription +=p.text
        
                        campaigndescription=Element('campaigndescription')
                        project.append(campaigndescription)
                        campaigndescription.text=Campaigndescription                                               
                        ##Community
                        communityflag=""
                        flagcount=0
                        for h in  campaignsoup.find('div',attrs={"class":"project-nav__links"}).findAll('a'):
                            flagcount+=1                            
                            print(flagcount)
                            print(h.text)
                            print ("Community"==h.text)
                            if (flagcount==5):
                                communityflag="y"
                        
                        if communityflag=="y":                    
                            urlcampaign = url+str("/community")
                            print(urlcampaign)
                             
                            html=urllib2.urlopen(urlcampaign).read()
                            soup=BeautifulSoup(html, "html.parser")
                            if soup.find('div',attrs={"class":"community-section__locations_cities"}) is not None:
                                if (soup.find('div',attrs={"class":"community-section__locations_cities"}).findAll('div',attrs={"class":"location-list__item js-location-item"})) is not None: 
                                    table = soup.find('div',attrs={"class":"community-section__locations_cities"}).findAll('div',attrs={"class":"location-list__item js-location-item"})
                                    backers=Element('backersCities')
                                    project.append(backers)
                                    for x in table:
                                        row=Element('row')
                                        backers.append(row)
                                        for y in x.findAll('div',attrs={"class":"primary-text js-location-primary-text"}):
                                            for z in y.findAll('a'):
                                                city =Element('city')
                                                row.append(city)
                                                city.text= z.text
                                        for u in x.findAll('div',attrs={"class":"secondary-text js-location-secondary-text"}):
                                            for h in u.findAll('a'):
                                                state =Element('state')
                                                row.append(state)
                                                state.text=h.text
                                        for u in x.findAll('div',attrs={"class":"tertiary-text js-location-tertiary-text"}):
                                            count =Element('count')
                                            row.append(count)
                                            count.text=u.text
                                table = soup.find('div',attrs={"class":"community-section__locations_countries"}).findAll('div',attrs={"class":"location-list__item js-location-item"}) 
                                backers=Element('backersCountry')
                                project.append(backers)  
                                #print(table)
                                for x in table:
                                    row=Element('row')
                                    backers.append(row)
                                    for y in x.findAll('div',attrs={"class":"primary-text js-location-primary-text"}):
                                        for z in y.findAll('a'):
                                            city =Element('CountryTotal')
                                            row.append(city)
                                            city.text= z.text
                                    for u in x.findAll('div',attrs={"class":"tertiary-text js-location-tertiary-text"}):
                                        count =Element('count')
                                        row.append(count)
                                        count.text=u.text

        except:
            continue        


    
    PageNum = PageNum + 1
     
    if PageNum==2:
        tree.write(open(r'C:\Users\mandar\Downloads\testing\KickstartDay20unsuccesful.xml','w'))
    else:
        tree.write(open(r'C:\Users\mandar\Downloads\testing\KickstartDay20unsuccesful.xml','a'))

    print(PageNum)


