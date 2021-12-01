
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


if __name__ == '__main__':

    main_menu = """

    Please, choose the option you like:

    1) 
    0) Exit

    """
    print(
        bcolors.OKCYAN + bcolors.BOLD + "   Hi ^^ let's get start the tour of FFMPEG" + bcolors.ENDC)
    input_video = "videos/BigBuckBunny_512kb.mp4"
    output_video = "videos/cut.mp4"
    container_name = "BBB_container.mp4"
    while True:
        try:
            print(bcolors.OKCYAN + bcolors.BOLD + main_menu + bcolors.ENDC)
            option = int(input("Enter your option "))
            if option == 1:
                os.system("ffmpeg -flags2 +export_mvs -i videos/cut.mp4 -vf codecview=mv=pf+bf+bb videos/output_motion_vec.mp4")
            if option == 2:
                cut_only_video_name = "videos/only_video_cut_1min.mp4"
                audio_mp3_name = "mp3_audio_1.mp3"
                audio_acc_name = "acc_audio.aac"

                # cut the video and remove the audio using -an
                os.system("ffmpeg -ss "+"00:00:00"+" -i "+input_video+" -to "+"00:01:00"+" -c copy -an "+cut_only_video_name)
                os.system("ffmpeg -ss "+"00:00:00"+" -i "+input_video+" -to "+"00:01:00"+" -c:a libmp3lame "+audio_mp3_name)
                os.system("ffmpeg -ss "+"00:00:00"+" -i "+input_video+" -to "+"00:01:00"+" -c:a aac -b:a 64k "+audio_acc_name)
                #since for acc acodec use 128kbps bitrate by default. we can use for this case the half one.

                os.system("ffmpeg -i "+cut_only_video_name+" -i "+audio_mp3_name+" -i "+audio_acc_name+" -c:v copy -c:a copy -c:a copy -map 0:v -map 1:a -map 2:a BBB_container.mp4")

                #merge audio and video
                # borrar los outputs de las dos primeras? esta mal hecho, ahay que volver mirar el mp3...

            if option == 3:

                # 1)First we will use ffprobe to count the numbers of video and
                # audio streams / tracks:

                # Numbers of video tracks:
                # We sending output to a PIPE (shell equiv.: ls -l | ... )
                pos_v_tracks = subprocess.Popen(("ffprobe -v error -select_streams v -show_entries stream=index -of csv=p=0 " + container_name).split(),stdout=subprocess.PIPE)
                # Read output from 'pos_v_tracks' as input to 'num_v_tracks' (shell equiv.: ... | wc -l)
                num_v_tracks = subprocess.Popen('wc -l'.split(), stdin=pos_v_tracks.stdout, stdout=subprocess.PIPE)
                out_video, _  = num_v_tracks.communicate() # assign one to _,
                # which means ignore by convention

                #communicate() method used here will return a byte object instead of a string.
                #So, we will need to convert the output to a string using
                # decode()

                num_v_tracks = out_video.strip().decode()#num of video tracks
                print("The numbers of video tracks :", num_v_tracks)

                # Numbers of audio tracks:
                pos_a_tracks = subprocess.Popen(("ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 " + container_name).split(),stdout=subprocess.PIPE)
                # Read output from 'ls' as input to 'num_v_tracks' (shell equiv.: ... | wc -l)
                num_a_tracks = subprocess.Popen('wc -l'.split(), stdin=pos_a_tracks.stdout, stdout=subprocess.PIPE)
                out_audio, err_audio = num_a_tracks.communicate()
                num_a_tracks = out_audio.strip().decode()
                print("The numbers of audio tracks :", num_a_tracks)

                
                # 2) Find the codec name of each tracks we found before
                list_vcodec = [];list_acodec = [];
                
                
                #num_v_tracks = len(list_vcodec);
                #num_a_tracks = len(list_acodec);
                for i in range(int(num_v_tracks)):
                    vcodec = subprocess.Popen(("ffprobe -v error -select_streams v:"+str(i)+" -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "+container_name).split(),stdout=subprocess.PIPE)
                    vcodec = vcodec.communicate()[0].decode("utf-8").replace("\n","")
                    list_vcodec.append(vcodec)
                    print("The video codec name for",i,"track is",vcodec)
                for i in range(int(num_a_tracks)):
                    acodec = subprocess.Popen(("ffprobe -v error -select_streams a:"+str(i)+" -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "+container_name).split(),stdout=subprocess.PIPE)
                    acodec = acodec.communicate()[0].decode("utf-8").replace("\n","")
                    list_acodec.append(acodec)
                    print("The audio codec name for",i,"track is",acodec)

                # 3) Check the broadcasting standard that would fit
                #print("List",list_acodec,list_vcodec)
                #list_codec = set(list_vcodec + list_acodec)

                # Test:
                #list_vcodec = ["h264"]
                #list_acodec = ["aac", "mp3"];

                DVD_v = ["mpeg2video","h264"]; DVD_a = ["aac","ac3","mp3"];
                ISDB_v = ["mpeg2video","h264"]; ISDB_a = ["aac"];
                ATSC_v = ["mpeg2video","h264"]; ATSC_a = ["ac3"];
                DTMB_v = ["avs","avs+","mpeg2video","h264"]; DTMB_a = ["dra","aac","ac3","mp2","mp3"];

                BC_v_standard = [DVD_v]+[ISDB_v]+[ATSC_v]+[DTMB_v]
                BC_a_standard = [DVD_a]+[ISDB_a]+[ATSC_a]+[DTMB_a]
                BC_type_v = []
                for i in range(len(BC_v_standard)):
                    #If any element in the received vcodec list is in the BC
                    # standard types, we get True boolean
                    bool_v_flag = any(
                        item in list_vcodec for item in BC_v_standard[i])
                    if bool_v_flag:
                        BC_type_v.append(i) #add the position of the type of
                        # BC Standards

                BC_type_a = []
                # same idea but with the audio now
                for i in range(len(BC_a_standard)):
                    aa = BC_a_standard[i]
                    bool_a_flag = any(
                        item in list_acodec for item in BC_a_standard[i])
                    if bool_a_flag:
                        BC_type_a.append(
                            i)  # add the position of the type of BC Standards

                #Find the common elements in both the lists
                if (set(BC_type_v) and set(BC_type_a)):
                    BC_type = set(BC_type_v) and set(BC_type_a)
                    BC_type_list = list(BC_type); #convert it to a list

                BC_Standard_Names = ["DVD","ISDB","ATSC","DTMB"]
                #Print the corresponds Broadcast, if the list before is 0,
                # means that it does not fit for any
                if(len(BC_type_list)>0):
                    for i in BC_type_list:
                        print("It fits for following broadcasting standard:",
                              BC_Standard_Names[i])
                else:
                    print("Error it does not fit for any broadcasting standard")

            if option == 4:
                os.system("ffmpeg -i "+container_name+" -i subtitle.srt -c:v copy -c:a copy -c:s mov_text -map 0 -map 1 video_subtitle.mp4")
                os.system("ffmpeg -i "+input_video+" -vf subtitles=subtitle.srt video_with_subtitle.mp4")
                os.system("curl -O https://drive.google.com/file/d/12C5ZDuH4BoKfWTJbn1kd5EtUgnbGlBoQ/view?usp=sharing/subtitle_download.srt")
                #Ask if is normal that the the download version has larger size!

            # integrate everthing inside a class!!->Ej5

            if option == 0:
                print(
                    bcolors.HEADER + "It's been a pleasure, see you next time" + bcolors.ENDC)
                break

        except:
            print(
                bcolors.UNDERLINE + bcolors.FAIL + "Occur a error, please try again" + bcolors.ENDC)