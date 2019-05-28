
import cv2, time, os, sys, subprocess, shlex, re
import datetime as dt
from subprocess import call
import os

os.sys.path.append("/mnt/NewDrive/saurabhh/scripts")
import notification as noti

def creation_time(filename):
    import os, sys, subprocess, shlex, re
    from subprocess import call

    cmnd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', filename]
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err =  p.communicate()
    print ("==========output==========")
    print (out)
    if err:
        print ("========= error ========")
        print (err)
    t = out.splitlines()
    time = str(t[14][18:37])
    return time

#Directory which contains the video files.
#-------update----------------------------------------------------------
indir = "/media/usb/NDS/AFTER/Bradenton 02_06_2019/Angle1/" #"/media/usb/NDS/AFTER/Miami/Angle2/"
result_dir = "/mnt/NewDrive/cvuser/NDS/"

#Filewalker function
for root, dirs, filenames in os.walk(indir):
    for f in filenames:
        if f[-4:] == '.MP4':

            f = os.path.join(root,f)
            #'''
            cpp = f + "_fixed"
            cmnd = ["ffmpeg", "-err_detect", "ignore_err",  "-i" , f, "-c", "copy", cpp]
            p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err =  p.communicate()
            cmnd = ["exiftool", "-TagsFromFile", f, cpp]
            p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err =  p.communicate()
            cmnd = ["mv", cpp, f]
            p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err =  p.communicate()
            #'''


            print("Fixing the file")
        
            print('Starting to timestamp: ' + str(f))

            video_filename = f

            #Opens the video import and sets parameters
            print("here")
            video = cv2.VideoCapture(video_filename)
            print("here22")

            #Checks to see if a the video was properly imported
            status = video.isOpened()

            if status == True: 
                FPS = video.get(cv2.CAP_PROP_FPS)
                width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
                size = (int(width), int(height))
                total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
                #frame_lapse = (1/FPS)*1000

                #Initializes the export video file
                codec = cv2.VideoWriter_fourcc(*'X264')
                t = creation_time(video_filename)
                
                offset = dt.timedelta(microseconds = 3.193e+9)

                ff = dt.datetime.strptime(t.split("'")[1], "%Y-%m-%d %H:%M:%S") - offset
                
                complete = str(ff).split(" ")
                print (complete)
                print (str(ff))
                Date = complete[0].split("-")
                Time =  complete[1].split(":")

                print (Date)
                print(Time)

                ff = Date[1]+ "-" + Date[2] + "_" + Time[0] + "-" + Time[1] 

                #-------update----------------------------------------------------------
                ff2 = "D1_Bradenton_after_day1_angle1_corrected_" + ff + ".MP4"
                result_name = os.path.join(result_dir, ff2)


                video_out = cv2.VideoWriter(result_name, 0x00000021, FPS, size, 1)

                #Initializes time origin of the video
                
                initial = dt.datetime.strptime(t.split("'")[1], "%Y-%m-%d %H:%M:%S") - offset	#--update----------------
                timestamp = initial

                #Initializes the frame counter
                current_frame = 0

                start = time.time()

                #iterates through each frame and adds the timestamp before sending
                #the frame to the output file.
                while current_frame < total_frames:
                    success, image = video.read()
                    elapsed_time = video.get(cv2.CAP_PROP_POS_MSEC)
                    current_frame = video.get(cv2.CAP_PROP_POS_FRAMES)
                    timestamp = initial + dt.timedelta(microseconds = elapsed_time*1000)
                    t = timestamp + dt.timedelta(microseconds = -timestamp.microsecond)
                    cv2.putText(image, 'Date: ' + str(timestamp)[0:10], (50,int(height-150)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255, 255, 255), 3)
                    cv2.putText(image, 'Time: ' + str(timestamp)[11:-4], (50,int(height-100)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255, 255, 255), 3)
                    video_out.write(image)

    
                video.release()
                video_out.release()
                #cv2.destroyAllWindows()

                duration = (time.time()-float(start))/60

                print("Video has been timestamped")
                print('This video took:' + str(duration) + ' minutes')
            else:
                print('Error: Video failed to load')
            #sys.exit(1)
    #break

noti.sendemail("zwang9@cutr.usf.edu")
