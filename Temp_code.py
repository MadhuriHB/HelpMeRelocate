 # if childnode.nodeName == 'gsId':
                #     gsid = childnode.childNodes[0].toxml()
                         
                # elif childnode.nodeName == 'name':
                #     if childnode.hasChildNodes():
                #         name = childnode.childNodes[0].toxml()
                #     else:
                #         name = childnode.toxml()    
           
                # elif childnode.nodeName == 'type':
                #     if childnode.hasChildNodes():
                #         school_type = childnode.childNodes[0].toxml()
                #     else:
                #         school_type = childnode.toxml()

                # elif childnode.nodeName == 'gradeRange':
                #     if childnode.hasChildNodes():
                #         gradeRange = childnode.childNodes[0].toxml()
                #     else:
                #         gradeRange = childnode.toxml()           

                # elif childnode.nodeName == 'parentRating':
                #     if childnode.hasChildNodes():
                #         parentRating = childnode.childNodes[0].toxml()
                #     else:
                #         parentRating = childnode.toxml()

                # elif childnode.nodeName == 'city':
                #     if childnode.hasChildNodes():
                #         city = childnode.childNodes[0].toxml()
                #     else:
                #         city = childnode.toxml()            

                # elif childnode.nodeName == 'state':
                #     if childnode.hasChildNodes():
                #         state = childnode.childNodes[0].toxml()
                #     else:
                #         state = childnode.toxml()           
            
                # elif childnode.nodeName == 'address':
                #     if childnode.hasChildNodes():
                #         address = childnode.childNodes[0].toxml()
                #     else:
                #         address = childnode.toxml()                

                # elif childnode.nodeName == 'phone':
                #     if childnode.hasChildNodes():
                #         phone = childnode.childNodes[0].toxml()
                #     else:
                #         phone = childnode.toxml()           

                # elif childnode.nodeName == 'website':
                #     if childnode.hasChildNodes():
                #         website = childnode.childNodes[0].toxml()
                #     else:
                #         website = childnode.toxml()

                # elif childnode.nodeName == 'lat':
                #     if childnode.hasChildNodes():
                #         lat = childnode.childNodes[0].toxml()
                #     else:
                #         lat = childnode.toxml()

                # elif childnode.nodeName == 'lon':
                #     if childnode.hasChildNodes():
                #         lon = childnode.childNodes[0].toxml()
                #     else:
                #         lon = childnode.toxml()

                # elif childnode.nodeName == 'overviewLink':
                #     if childnode.hasChildNodes():
                #         overviewLink = childnode.childNodes[0].toxml()
                #     else:
                #         overviewLink = childnode.toxml()

                # elif childnode.nodeName == 'ratingsLink':
                #     if childnode.hasChildNodes():
                #         ratingsLink = childnode.childNodes[0].toxml()
                #     else:
                #         ratingsLink = childnode.toxml()

                # elif childnode.nodeName == 'reviewsLink':
                #     if childnode.hasChildNodes():
                #         reviewsLink = childnode.childNodes[0].toxml()
                #     else:
                #         reviewsLink = childnode.toxml()

            #Create temporary School instance for each school and append it to a list

            # tempSchoolObject = School(gsid=gsid, name=name, schoolType=school_type,
            #                           gradeRange=gradeRange, 
            #                           city=city, state=state, address=address,
            #                           phone=phone, website=website,
            #                           latitude=lat, longitude=lon,
            #                           parentRating=parentRating,
            #                           overviewLink=overviewLink,
            #                           ratingsLink=ratingsLink, reviewsLink=reviewsLink)