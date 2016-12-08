import numpy as np
import cv2
import os
from shutil import rmtree

def find_show(template, image, img_rgb, clef=None):
    # check to see if the image to analyze has been put in
    if img_rgb is None:
        if os.path.isdir('./app/tmp'):        
            rmtree('./app/tmp')
        exit(code="No image to analyze, or could not read image")
        
    # define the width and height of the template
    w, h = template.shape[::-1]

    # define a threshold and find where the template image matches above
    # that threshold (as a measure of error)
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

    # set the threshold based on clef
    ## NOTE: As of now, these two thresholds need to be calibrated based
    # on some unknown parameter, which I will hopefully ascertain
    # this also could hopefully be solved systematically
    # .198 and .35 
    if clef is not None:
        threshold = .198
    else:
        threshold = .35

    loc = np.where( res >= threshold )
    pt_list = zip(*loc[::-1])
    pt_list.sort(key=lambda (x, y): (y))

    # check that points were actually found
    if len(pt_list) > 0:
    
        # create a new point list for the future
        new_pt_list = list()
    
        # the program finds lots of duplicates, so we need to eliminate those
        # first step is to split the list up into sections, first by y axis
        # then by x axis
        # create two lists of x and y coordinates to separate things
        ylist = list()
        split_listy = list()
    
        for x in range(len(pt_list)):
            ylist.append(pt_list[x][1])

        # determine where the different y clusters are
        for x in range(len(pt_list)):
            if x > 0:
                if abs(ylist[x] - ylist[x - 1]) > 10:
                   split_listy.append(x - 1)

        # check if there is more than one y-coordinate cluster
        if split_listy != []:
            # iterate through each y coordinate cluster
            for j in range(len(split_listy)):
                # define the y coordinate as the last y coordinate before the split ##### COULD DO THIS AS AN AVERAGE LATER ####
                ycoor = (pt_list[split_listy[j]])[1]
                split_listx = list()
                xlist = list()

                if j == 0:
                    # create a x list that only counts the x coordinates that correspond to the given y coordinate
                    for x in range(split_listy[j] - 1):
                        xlist.append(pt_list[x][0])
                else:
                    # create the x list for this y coordinate
                    for x in range((split_listy[j - 1] + 1), (split_listy[j] - 1)):
                        xlist.append(pt_list[x][0])

                # sort the list we have created
                xlist.sort()
                # determine where the different x clusters are
                for x in range(len(xlist)):
                    if x > 0:
                        if abs(xlist[x] - xlist[x - 1]) > 20:
                            split_listx.append(x - 1)

                # iterate through the split list of x coordinates
                for k in range(len(split_listx)):
                    xcoor = (xlist[split_listx[k]])
                    new_pt_list.append((xcoor, ycoor))

                # add the last box in that x
                if xlist != []:
                    xcoor = xlist[len(xlist) - 1]
                    new_pt_list.append((xcoor, ycoor))
                           
            # we need to add the last x coordinate
            ycoor = (pt_list[len(pt_list) - 1])[1]
            for x in range((split_listy[len(split_listy) - 1] + 1), len(pt_list) - 1):
                xlist.append(pt_list[x][0])
                
            # sort the list we have created
            xlist.sort()

            # determine where the different y clusters are
            for x in range(len(xlist)):
                if x > 0:
                    if abs(xlist[x] - xlist[x - 1]) > 20:
                        split_listx.append(x - 1)
                    
            # iterate through the split list of y coordinates
            for k in range(len(split_listx)):
                xcoor = (xlist[split_listx[k]])
                new_pt_list.append((xcoor, ycoor))

            # add the last box in that x
            if xlist != []:
                xcoor = xlist[len(xlist) - 1]
                new_pt_list.append((xcoor, ycoor))
            
        # in the event that there is only one y cluster            
        else:
            split_listx = list()
            xlist = list()
        
            # create a separate list of y coordinates, which would be all of them in this case
            for x in range(len(pt_list)):
                xlist.append((pt_list[x][0]))
    
            # sort that list
            xlist.sort()

            # determine where the different y clusters are under this x coordinate
            for x in range(len(pt_list)):
                if x > 0:
                    if abs(xlist[x] - xlist[x - 1]) > 20:
                        split_listx.append(x - 1)

            # create an x coordinate that is the average of the x coordinates
            ycoor = int(np.mean(ylist, axis=0)[0])
            
            # find each y coordinate and add the now completed point to the new list
            for i in range(len(split_listx)):
                if i == 0:
                    new_pt_list.append((int(np.mean(xlist[0:split_listx[i]], axis=0)), ycoor))
                else:
                    new_pt_list.append((int(np.mean(ylist[split_listx[i - 1]:split_listx[i]], axis=0)), ycoor))

            # add the final point
            new_pt_list.append((int(np.mean(xlist[split_listx[(len(split_listx) - 1)]:(len(xlist) - 1)], axis=0)), ycoor))

        # define a counter to keep track of which picture we're on
        x = 1

        # define a list to contain y-coordinate boundary pairs
        clef_bounds = list()
        
        if clef is None:
            for pt in new_pt_list:
                    topleft = pt[0] - (5*w/16)
                    top = pt[1] - h
                    bottomright = pt[0] + (15*w/16)
                    bottom = pt[1] + 3*h
    
                    # add the now-defined top and bottom of each clef
                    clef_bounds.append((top, bottom))
        
        else:
            # maybe check to make sure that clef is of type list?

            # make a new list of lists that will contain the old pt_list in order
            ordered_pt_list = list()
            for i in range(len(clef)):
                ordered_pt_list.append([])

            # iterate through the boundaries in clef
            for boundary_set in clef:
                # iterate throught the unordered points
                for pt in new_pt_list:
                    # check if each point is within the y boundaries
                    if pt[1] >= boundary_set[0] and pt[1] <= boundary_set[1]:
                        # add the points to the appropriate list within the list
                        ordered_pt_list[clef.index(boundary_set)].append(pt)
        
            # we now need to iterate through the list of lists
            for sub_pt_list in ordered_pt_list:
                # and through that list, which needs to be sorted into x coordinate order
                sub_pt_list.sort()
                for pt in sub_pt_list:
                    # define the top as the upper clef bound
                    top = clef[ordered_pt_list.index(sub_pt_list)][1]

                    # similarly, define the bottom as the lower clef bound
                    bottom = clef[ordered_pt_list.index(sub_pt_list)][0]

                    # define the other corners somewhat arbitrarily
                    # these have been calibrated based on experience, but
                    # there is maybe a way to systematically do this
                    # systematically solving this would likely also solve the
                    # issue of sharps, naturals, and flats needing the bounds to
                    # be larger
                    topleft = pt[0] - (5*w/16)
                    bottomright = pt[0] + (18*w/16)

                    # create a sub image that is bounded and (ideally) represents a music note
                    im_piece = img_rgb[bottom:top, topleft:bottomright]
                
                    # get each sub image's size
                    height, width = im_piece.shape[:2]

                    # define our bounds
                    lower = np.array([200, 0, 0], dtype = "uint8")
                    upper = np.array([255, 0, 0], dtype = "uint8")

                    # create a NoneType array that represents a mask where the color
                    # blue is
                    isBlue = cv2.inRange(im_piece, lower, upper)

                    if (np.sum(isBlue) < 100):
                        if im_piece is not None:
                            if height != 0 and width != 0:
                                cv2.imwrite('./app/tmp/data/znote' + str(x) + '.jpg', im_piece)
                                x = x + 1
                
                        # for debugging purposes, draw a blue rectangle around the sub-image
                        # this actually turned out to be a good way of eliminating extra duplicates
                        cv2.rectangle(img_rgb, (topleft, top), (bottomright, bottom), (255, 0, 0), 3)

            # for debugging purposes, save the image with what we've outlined in blue rectangles
            cv2.imwrite('results.jpg', img_rgb)

    else:
        # remove the temporarily created directory and exit
        if os.path.isdir('./app/tmp'):
            rmtree('./app/tmp')
        exit(code="No points were found, please check your template")
        
    return clef_bounds
