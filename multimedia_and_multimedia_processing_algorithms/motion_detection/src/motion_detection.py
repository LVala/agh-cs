from argparse import ArgumentParser
import numpy as np
import datetime
import time
import os
import cv2

def main():
    # parse command line arguments
    parser = ArgumentParser(prog="detmot", description="Detect motion in a video")
    parser.add_argument("source", help="Source of video")
    parser.add_argument("-d", "--debug", action="store_true", help="Debugging mode")
    parser.add_argument("-m", "--mask", action="store_true", help="Custom area (mask), where motion will be detected")
    parser.add_argument("-t", "--time", action="store_true", help="Print current date and time on the video")
    parser.add_argument("-f", "--framebyframe", action="store_true", help="Use difference of next 2 frames instead of current and reference frame")
    parser.add_argument("-a", "--area", type=int, default=100, help="Initial minimal object area (0-2000)")
    parser.add_argument("-o", "--output", help="Write video with highlited motion to specified file")
    parser.add_argument("-s", "--device", action="store_true", help="Use device instead of file")

    args = parser.parse_args()

    CONT_AREA = args.area
    DEBUG = args.debug
    TIME = args.time
    USE_CUSTOM_AREA = args.mask
    FRAME_BY_FRAME = args.framebyframe
    TO_FILE = args.output is not None
    DEVICE = args.device

    if not DEVICE: 
        cap = cv2.VideoCapture(args.source)
    else: 
        cap = cv2.VideoCapture(int(args.source))
        time.sleep(1)
        if not cap.isOpened():
            print("detmot: error: device cannot be opened")
            exit(1)

    if DEVICE: waitTime = 10
    else: waitTime = 40

    # output file
    if TO_FILE:
        width = int(cap.get(3))
        height = int(cap.get(4))
        size = (width, height)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(f"{args.output}.avi", fourcc, 20.0, size)
    
    # create main window
    root_wind = "Motion detector"
    cv2.namedWindow(root_wind)
    cv2.createTrackbar("Minimal object area", root_wind, 5, 2000, lambda x: x)
    cv2.setTrackbarPos("Minimal object area", root_wind, CONT_AREA)

    # initial (reference) frame
    ret, frame1 = cap.read()
    if not ret:
        print("detmot: error: cannot recieve frame")
        exit(1)
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur1 = cv2.GaussianBlur(gray1, (21, 21), 0)

    # select area of interest
    if USE_CUSTOM_AREA:
        rois = cv2.selectROIs(root_wind, frame1)
        black = np.zeros((frame1.shape[0], frame1.shape[1], 3), np.uint8)
        for roi in rois:
            cv2.rectangle(black, (roi[0], roi[1]),(roi[0]+roi[2], roi[1]+roi[3]),(255, 255, 255), -1)
        gray = cv2.cvtColor(black,cv2.COLOR_BGR2GRAY)
        b_mask = cv2.threshold(gray,127,255, cv2.THRESH_BINARY)[1]

        cv2.imshow(root_wind, b_mask)
        cv2.waitKey(10000000)

    i = 0 
    while cap.isOpened():
        CONT_AREA = cv2.getTrackbarPos("Minimal object area", root_wind)  # get sensitivity from the trackbar

        ret, frame2 = cap.read()
        if not ret:
            print("detmot: error: cannot recieve frame")
            exit(1)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        blur2 = cv2.GaussianBlur(gray2, (21, 21), 0)

        frame_diff = cv2.absdiff(blur1, blur2)
        thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
        if USE_CUSTOM_AREA: thresh = cv2.bitwise_and(thresh, thresh, mask=b_mask)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        text = "No motion detected"
        for contour in contours:
            if cv2.contourArea(contour) < CONT_AREA:
                continue
            
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 0, 255), 2)
            text = "Motion detected"

        if TO_FILE: out.write(frame2)
        cv2.putText(frame2, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        if TIME: cv2.putText(frame2, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame2.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        if DEBUG:
            cv2.imshow(root_wind, gray2)
            if cv2.waitKey(400) == ord('q'):
                break
            cv2.imshow(root_wind, blur2)
            if cv2.waitKey(400) == ord('q'):
                break
            cv2.imshow(root_wind, frame_diff)
            if cv2.waitKey(400) == ord('q'):
                break
            cv2.imshow(root_wind, thresh)
            if cv2.waitKey(400) == ord('q'):
                break
            cv2.imshow(root_wind, dilated)


        cv2.imshow(root_wind, frame2)
        if cv2.waitKey(waitTime) == ord('q'):
            break

        if FRAME_BY_FRAME:
            if len(contours) == 0:
                blur1 = blur2

            # i += 1
            # if i % 5 == 0:
            #     blur1 = blur2

    cv2.destroyAllWindows()
    cap.release()
    if TO_FILE: out.release()
