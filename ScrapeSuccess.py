'''
Created on Dec 29, 2016

@author: mandar
'''
import urllib2, re
from bs4 import BeautifulSoup
import sys
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree

try:
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
                if (x.find('div',attrs={"class":"project-profile-title text-truncate-xs"}))  is not None:      
                    tableSuccess = x.find('div',attrs={"class":"project-profile-title text-truncate-xs"})
                    #for x in tableSuccess: 
                    y = tableSuccess.find('a')           
                    url="https://www.kickstarter.com"+(y.get('href')).split("?", 1)[0]
                    ProjectID=(y.get('href')).split("?", 1)[0].split("/")[2]
                    html=urllib2.urlopen(url).read()
                    soup=BeautifulSoup(html,"html.parser")
                    try:
                        hTitle=str(y.text.decode("utf8"))
                        print(hTitle)
                    except:
                        hTitle=(y.get('href')).split("?", 1)[0].split("/")[3] 
                    if hTitle in projectList:
                        projectList[hTitle+": "+ProjectID]= projectList[hTitle+": "+ProjectID]+1
                    else:    
                        projectList[hTitle+": "+ProjectID]=1
                        project=Element('successproject')
                        root.append(project)
                        ##Title of the project
                        #hTitle=soup.title.string
                        Title=Element('Title')
                        project.append(Title)
                        Title.text=hTitle
                        ## total pledged money till current 
                        pledgedMoney=(soup.find('div',attrs={"class":"col-right col-4 py3 border-left"})).find("h3",{"class": "mb0"}).find("span",{"class": "money"}).text    
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
                        TotalCost.text=(soup.find('div',attrs={"class":"col-right col-4 py3 border-left"})).find("div",{"class": "type-12 medium navy-500"}).find("span",{"class": "money"}).text
                        ##total number of Backers
                        backers=Element('backers')
                        project.append(backers)
                        backers.text=(soup.find('div',attrs={"class":"col-right col-4 py3 border-left"})).find("div",{"class": "mb0"}).find("h3",{"class": "mb0"}).text 
                        ##Comments
                        Comment=""
                        commentCount=0
                        urlcomments = url +str("/comments")
                        htmlcomments=urllib2.urlopen(urlcomments).read()
                        commentsoup=BeautifulSoup(htmlcomments, "html.parser")
                        commentable = soup.findAll('li',attrs={"class":"NS_comments__comment collaborator comment item latest_comment mb3 py3"})
                        for x in commentable:
                            for y in x.findAll('p'):
                                Comment += y.text
                                commentCount+=1
                               
                        commentablereg = soup.findAll('li',attrs={"class":"NS_comments__comment comment item py3 mb3"})
                        for x in commentable:
                            for g in x.findAll('p'):
                                Comment += g.text
                                commentCount+=1
                               
                        comments=Element('comments')
                        project.append(comments)
                        comments.text=Comment
                        countcomments=Element('countcomments')
                        project.append(countcomments)
                        countcomments.text=str(commentCount)               
                        ##Campiagn - Description
                        urlcampaign =url+str("/description")
                        htmlcampaign=urllib2.urlopen(url).read()
                        campaignsoup=BeautifulSoup(htmlcampaign, "html.parser")
                        if (campaignsoup.find("div",{"class": "hidden js-campaign-state js-campaign-state__canceled"})) is None:
                            table = campaignsoup.find('div',attrs={"class":"full-description js-full-description responsive-media formatted-lists"})
                        else:
                            table = campaignsoup.find('div',attrs={"class":"col col-8 description-container"})    
                    
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
                        urlcampaign = url+str("/community")
                        html=urllib2.urlopen(urlcampaign).read() 
                        soup=BeautifulSoup(html, "html.parser")                
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
                        for x in table:
                            row=Element('row')
                            backers.append(row)
                            for y in x.findAll('div',attrs={"class":"primary-text js-location-primary-text"}):
                                for z in y.findAll('a'):
                                    city =Element('CountryTotal')
                                    row.append(city)
                                    city.text= z.text
                                    print(z.text)
                            for u in x.findAll('div',attrs={"class":"tertiary-text js-location-tertiary-text"}):
                                count =Element('count')
                                row.append(count)
                                count.text=u.text
                                print(u.text)                                                            
            except:   
                print("error")
                continue        
    
    
        
        PageNum = PageNum + 1
        if PageNum==2:
            tree.write(open(r'C:\Users\mandar\Downloads\testing\KickstartDay20Success.xml','w'))
        else:
            tree.write(open(r'C:\Users\mandar\Downloads\testing\KickstartDay20Success.xml','a'))
    
        print(PageNum)

except:
    print("error")

