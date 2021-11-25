
import os
#import subproces
#subprocess.call()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    MENU = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == '__main__':

    main_menu = """
    
    Please, choose the option you like:
    
    1) Cut the video 
    2) Add YUV histogram 
    3) Resize the video 
    4) Audio management
    0) Exit
    
    """
    print(bcolors.OKCYAN+bcolors.BOLD + "   Hi ^^ let's get start the tour of FFMPEG" + bcolors.ENDC)
    input_video = "BigBuckBunny_512kb.mp4"
    output_video = "cut.mp4"
    while True:
        try:
            print(bcolors.OKCYAN+bcolors.BOLD + main_menu + bcolors.ENDC)
            option = int(input("Enter your option "))
            if option == 1:
                #To know the duration of the video
                #os.system("ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "+input_video+" -sexagesimal")
                while True:
                    try:
                        start_end_times = input("Enter [START] and [END] times in HH:MM:SS (separate by space)\n").split()
                        start_times = start_end_times[0]; end_times = start_end_times[1]
                        # Check user enter values in the range
                        # we take directly the elements of the list
                        hour_i, min_i , sec_i = [int(i) for i in start_times.split(":")]
                        if 0>hour_i or hour_i>24 or 0>min_i or min_i>60 or 0>sec_i or sec_i>60:
                            print(bcolors.FAIL+bcolors.UNDERLINE+"Error of start time"+bcolors.ENDC)
                            raise"Error of user input of start time"
                        hour_f, min_f, sec_f = [int(i) for i in end_times.split(":")]
                        if 0>hour_f or hour_f>24 or 0>min_f or min_f>60 or 0>sec_f or sec_f>60:
                            print(bcolors.FAIL + bcolors.UNDERLINE + "Error of end time" + bcolors.ENDC)
                            raise"Error of user input of end time"

                        if (hour_i*3600 + min_i*60 + sec_i) > (hour_f*3600 + min_f*60 + sec_f) :
                            print(bcolors.FAIL + bcolors.UNDERLINE + "Start time must be less than end time" + bcolors.ENDC)
                            raise"Start time must be less than end time"

                        print(bcolors.HEADER + "Start time is :", start_times,
                              "End time is :", end_times + bcolors.ENDC)
                        break
                    except:
                        print(bcolors.FAIL+bcolors.UNDERLINE+"Please try again"+bcolors.ENDC)

                os.system("ffmpeg -ss "+start_times+" -i "+input_video+" -to "+end_times+" -c copy "+output_video)
                print(bcolors.HEADER+"  Great! You have done the cut video"+bcolors.ENDC)

            if option == 2:
                os.system("ffmpeg -i "+output_video+" -vf ""split=2[a][b],[b]histogram,scale=50:200,format=yuva444p[hh],[a][hh]overlay hist_overlay.mp4")
                print(bcolors.HEADER+"  Amazing! You have the YUV histogram added to the cut video"+bcolors.ENDC)
            if option == 3:
                flag_continue = True
                while flag_continue :
                    try:
                        print(bcolors.MENU+bcolors.BOLD+""""
                        Menu - resize options:
                            
                            1. 720p
                            2. 480p
                            3. 360x240
                            4. 160x120
                            0. exit
                            
                              """+bcolors.ENDC)
                        resize_type = int(input("Choose the type of resize you want: "))
                        if resize_type<0 or resize_type>4:
                            raise"Error of user input option"
                        if resize_type == 1:
                            scale = "1280:720"
                        elif resize_type == 2 :
                            scale = "640:480"
                        elif resize_type == 3 :
                            scale = "360:240"
                        elif resize_type == 4:
                            scale = "160x120"
                        elif resize_type == 0:
                            flag_continue = False
                            break
                        #else:
                        #    print("Please try again")
                        os.system("ffmpeg -i "+input_video+" -vf scale="+scale+" output_"+scale+".mp4")
                        print(bcolors.HEADER+"Yupii!! End the scale transformation of the video"+bcolors.ENDC)
                    except:
                        print(bcolors.UNDERLINE+bcolors.FAIL+"Enter value is invalid, please try again"+bcolors.ENDC)

            if option == 4:
                """change the audio into mono output and in a different audio codec """
                #mono output
                #os.system("ffmpeg -i "+input_video+" -ac 1 mono.mp4")
                #Change the audio codec
                while True:
                    try:
                        print(bcolors.MENU+bcolors.BOLD+""""
                            Menu - audio codec options:
                                
                                1. AAC
                                2. AC-3
                                3. MP2
                                4. MP3
                                0. exit
                                
                                  """+bcolors.ENDC)
                        codec_op = int(input("Please, choose your option: "))
                        #AAC, AC-3, MP2, MP3
                        if codec_op< 0 or codec_op > 4:
                            raise"Error of user input option"
                        if codec_op == 1:
                            os.system("ffmpeg -i "+input_video+" -ac 1 -c copy -c:a aac converted_audio_acc.aac")
                        elif codec_op == 2:
                            os.system("ffmpeg -i "+input_video+" -ac 1 -c copy -c:a ac3 converted_audio_ac3.ac3")
                        elif codec_op == 3:
                            os.system("ffmpeg -i "+input_video+" -ac 1 -c copy -acodec mp2 converted_audio_mp2.mp2")
                        elif codec_op ==4:
                            os.system("ffmpeg -i "+input_video+" -ac 1 -c copy -acodec mp3 converted_audio_mp3.mp3")
                        elif codec_op == 0:
                            break
                    except:
                        print(bcolors.UNDERLINE+bcolors.FAIL+"Occur a error, please try again"+bcolors.ENDC)

            if option == 0:
                print(bcolors.HEADER+"It's been a pleasure, see you next time"+bcolors.ENDC)
                break
        except:
            print(bcolors.UNDERLINE + bcolors.FAIL + "Occur a error, please try again" + bcolors.ENDC)