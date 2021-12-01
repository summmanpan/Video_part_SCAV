
#import libraries
import os
import subprocess


#class to set colors the strings in the terminal
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

class FFMpeg_S2:
    def __init__(self, input_v):
        self.input = input_v

    def ex1(self,input="videos/cut_1min.mp4"):
        # Output a video that show the macroblocks and the motion vectors

        os.system(
            "ffmpeg -flags2 +export_mvs -i "+self.input+" -vf "
            "codecview=mv=pf+bf+bb videos/output_motion_vec.mp4")

    def ex2(self,
            v_track = "tracks/h264_video.mp4",
            a_mp3_track = "tracks/mp3_audio.mp3",
            a_acc_track = "tracks/acc_audio.aac"):

        # cut the video and remove the audio using -an
        os.system(
            "ffmpeg -ss " + "00:00:00" + " -i " + self.input + " -to " + "00:01:00"
            + " -c copy -an " + v_track)
        os.system(
            "ffmpeg -ss " + "00:00:00" + " -i " + self.input + " -to " + "00:01:00"
            + " -c:a libmp3lame " + a_mp3_track)
        os.system(
            "ffmpeg -ss " + "00:00:00" + " -i " + self.input + " -to " + "00:01:00"
            + " -c:a aac -b:a 64k " + a_acc_track)
        # since for acc acodec use 128kbps bitrate by default. we can use for
        # this case the half one, namely 64k.

        # merge Audio and video in the same container
        os.system(
            "ffmpeg -i " + v_track + " -i " + a_mp3_track +
            " -i " + a_acc_track + " -c:v copy -c:a copy -c:a copy -map 0:v "
                                      "-map 1:a -map 2:a BBB_container.mp4")

        #remove the previous tracks files
        #os.system("rm -d tracks")

    def ex3(self, container_name = "BBB_container.mp4"):

        # 1)First we will count the numbers of video and audio streams / tracks:

        # Numbers of video tracks:
        # We sending output to a PIPE (shell equiv.: ls -l | ... )
        pos_v_tracks = subprocess.Popen(("ffprobe -v error -select_streams v -show_entries stream=index -of csv=p=0 " + container_name).split(),
                                        stdout=subprocess.PIPE)
        # Read output from 'pos_v_tracks' as input to 'num_v_tracks' (shell equiv.: ... | wc -l)
        num_v_tracks = subprocess.Popen('wc -l'.split(),
                                        stdin=pos_v_tracks.stdout,
                                        stdout=subprocess.PIPE)
        out_video, _ = num_v_tracks.communicate()  # assign one to _,
        # which means ignore by convention

        # communicate() method used here will return a byte object instead of a string.
        # So, we need to convert the output to a string using decode()

        num_v_tracks = out_video.strip().decode()  # num of video tracks
        print("The numbers of video tracks :", num_v_tracks)

        # Numbers of audio tracks:
        pos_a_tracks = subprocess.Popen(("ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 " + container_name).split(),
                                        stdout=subprocess.PIPE)
        # Read output from 'ls' as input to 'num_v_tracks' (shell equiv.: ... | wc -l)
        num_a_tracks = subprocess.Popen('wc -l'.split(),
                                        stdin=pos_a_tracks.stdout,
                                        stdout=subprocess.PIPE)
        out_audio, err_audio = num_a_tracks.communicate()
        num_a_tracks = out_audio.strip().decode()
        print("The numbers of audio tracks :", num_a_tracks)

        # 2) Find the codec name of each tracks we found before
        list_vcodec = [];
        list_acodec = [];

        # num_v_tracks = len(list_vcodec);
        # num_a_tracks = len(list_acodec);
        for i in range(int(num_v_tracks)):
            vcodec = subprocess.Popen(("ffprobe -v error -select_streams v:" + str(i) + " -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 " + container_name).split(),
                                      stdout=subprocess.PIPE)
            vcodec = vcodec.communicate()[0].decode("utf-8").replace("\n", "")
            list_vcodec.append(vcodec)
            print("The video codec name for", i, "track is", vcodec)
        for i in range(int(num_a_tracks)):
            acodec = subprocess.Popen(("ffprobe -v error -select_streams a:" + str(i) + " -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 " + container_name).split(),
                                      stdout=subprocess.PIPE)
            acodec = acodec.communicate()[0].decode("utf-8").replace("\n", "")
            list_acodec.append(acodec)
            print("The audio codec name for", i, "track is", acodec)

        # 3) Check the broadcasting standard that would fit

        # Test:
        # list_vcodec = ["h264"]
        # list_acodec = ["aac", "mp3"];

        DVD_v = ["mpeg2video", "h264"];
        DVD_a = ["aac", "ac3", "mp3"];
        ISDB_v = ["mpeg2video", "h264"];
        ISDB_a = ["aac"];
        ATSC_v = ["mpeg2video", "h264"];
        ATSC_a = ["ac3"];
        DTMB_v = ["avs", "avs+", "mpeg2video", "h264"];
        DTMB_a = ["dra", "aac", "ac3", "mp2", "mp3"];

        BC_v_standard = [DVD_v] + [ISDB_v] + [ATSC_v] + [DTMB_v]
        BC_a_standard = [DVD_a] + [ISDB_a] + [ATSC_a] + [DTMB_a]
        BC_type_v = []
        for i in range(len(BC_v_standard)):
            # If any element in the received vcodec list is in the BC
            # standard types, we get True boolean
            bool_v_flag = any(
                item in list_vcodec for item in BC_v_standard[i])
            if bool_v_flag:
                BC_type_v.append(i)  # add the position of the type of
                # BC Standards

        BC_type_a = []
        # same idea but with the audio now
        for i in range(len(BC_a_standard)):
            aa = BC_a_standard[i]
            bool_a_flag = any(
                item in list_acodec for item in BC_a_standard[i])
            if bool_a_flag:
                BC_type_a.append(i)  # add the position of the type of BC Standards

        # Find the common elements in both the lists
        if (set(BC_type_v) and set(BC_type_a)):
            BC_type = set(BC_type_v) and set(BC_type_a)
            BC_type_list = list(BC_type);  # convert it to a list

        BC_Standard_Names = ["DVD", "ISDB", "ATSC", "DTMB"]
        # Print the corresponds Broadcast, if the list before is 0,
        # means that it does not fit for any
        if (len(BC_type_list) > 0):
            for i in BC_type_list:
                print("It fits for following broadcasting standard:",
                      BC_Standard_Names[i])
        else:
            print("Error it does not fit for any broadcasting standard")

    def ex4(self, track_sub = "subtitle/tk_sub.mp4",
            video_sub = "subtitile/video_sub.mp4"):
        #Download the subtitle using curl
        os.system(
            "curl -O https://drive.google.com/file/d/12C5ZDuH4BoKfWTJbn1kd5EtUgnbGlBoQ/view?usp=sharing/subtitle.srt")
        #put subtitle track on the video
        os.system(
            "ffmpeg -i " + self.input + " -i subtitle.srt -c:v copy -c:a copy -c:s mov_text -map 0 -map 1 "+track_sub)
        #Integrate the subtitle to the video
        os.system(
            "ffmpeg -i " + self.input + " -vf subtitles=subtitle.srt "
                                        ""+video_sub)


if __name__ == '__main__':

    main_menu = """

    Please, choose the option you like:

    1) Create a video with macroblocks and the motion vectors
    2) Create new container 
    3) Search the broadcasting standard type of the MP4 container
    4) Download, integrate subtitles for the video
    0) Exit

    """
    print(
        bcolors.OKCYAN + bcolors.BOLD + "   Hi ^^ let's get start the tour of FFMPEG" + bcolors.ENDC)

    while True:
        try:
            input_v = input("Enter your video name, if not, enter d for "
                            "default :")
            if input_v == "d":
                input_v = "videos/BigBuckBunny_512kb.mp4"
            print(bcolors.OKCYAN + bcolors.BOLD + main_menu + bcolors.ENDC)
            option = int(input("Enter your option "))
            #Create the FFMPEG class
            ffmpeg_s2 = FFMpeg_S2(input_v)

            if option == 1:
                ffmpeg_s2.ex1()
            if option == 2:
                ffmpeg_s2.ex2()
            if option == 3:
                ffmpeg_s2.ex3()
            if option == 4:
                ffmpeg_s2.ex4()
                #Ask if is normal that the the download version has larger size!
            if option == 0:
                print(
                    bcolors.HEADER + "It's been a pleasure, see you next time" + bcolors.ENDC)
                break
            if option>4 and option < 0:
                raise "Error of user input"
        except:
            print(
                bcolors.UNDERLINE + bcolors.FAIL + "Occur a error, please try again" + bcolors.ENDC)