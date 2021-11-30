import os
import subprocess

# subprocess.call()

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
                # 1)First we will use ffprobe to count video and audio streams / tracks:
                # Numbers of video:
                # Run 'ls', sending output to a PIPE (shell equiv.: ls -l | ... )
                pos_v_tracks = subprocess.Popen(("ffprobe -v error -select_streams v -show_entries stream=index -of csv=p=0 " + container_name).split(),stdout=subprocess.PIPE)
                # Read output from 'ls' as input to 'num_v_tracks' (shell equiv.: ... | wc -l)
                num_v_tracks = subprocess.Popen('wc -l'.split(), stdin=pos_v_tracks.stdout, stdout=subprocess.PIPE)
                out_video, err_video = num_v_tracks.communicate() # Trap stdout and stderr from 'num_v_tracks'

                #communicate() method used here will return a byte object instead of a string.
                #then we will need to convert the output to a string using decode()
                if err_video:
                    num_v_tracks = err_video.strip().decode(); print(num_v_tracks)
                if out_video:
                    num_v_tracks = out_video.strip().decode()
                    print("The numbers of video tracks :", num_v_tracks)

                # Numbers of audio:
                pos_a_tracks = subprocess.Popen(("ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 " + container_name).split(),stdout=subprocess.PIPE)
                # Read output from 'ls' as input to 'num_v_tracks' (shell equiv.: ... | wc -l)
                num_a_tracks = subprocess.Popen('wc -l'.split(), stdin=pos_a_tracks.stdout, stdout=subprocess.PIPE)
                out_audio, err_audio = num_a_tracks.communicate()
                num_a_tracks = out_audio.strip().decode() # convert to int
                print("The numbers of audio tracks :", num_a_tracks)

                #Find the codec name selecting the specific track
                list_vcodec = [];list_acodec = [];
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

                # Check the broadcasting standard
                #print("List",list_acodec,list_vcodec)
                #list_codec = set(list_vcodec + list_acodec)

                """DVD_v = set(["mpeg2video","h264"]);DVD_a = set(["aac","ac3","mp3"]);
                ISDB_v = set(["mpeg2video","h264"]);ISDB_a = set(["aac"]);
                ATSC_v = set(["mpeg2video","h264"]);ATSC_a = set(["ac3"]);
                DTMB_v = set(["avs","avs+","mpeg2video","h264"]);DTMB_a = set(["dra","aac","ac3","mp2","mp3"]);

                bool_v_DVD = set(list_vcodec).issubset(DVD_v)
                bool_a_DVD = set(list_acodec).issubset(DVD_a)"""

                DVD_v = ["mpeg2video","h264"]; DVD_a = ["aac","ac3","mp3"];
                ISDB_v = ["mpeg2video","h264"]; ISDB_a = ["aac"];
                ATSC_v = ["mpeg2video","h264"]; ATSC_a = ["ac3"];
                DTMB_v = ["avs","avs+","mpeg2video","h264"]; DTMB_a = ["dra","aac","ac3","mp2","mp3"];

                BC_v_standard = [DVD_v]+[ISDB_v]+[ATSC_v]+[DTMB_v]
                BC_a_standard = [DVD_a]+[ISDB_a]+[ATSC_a]+[DTMB_a]
                BC_type = []
                for i in range(len(BC_v_standard)):
                    #for j in range(len(BC_v_standard[i])):
                        #If any element in the received vcodec list is in the BC standard type, we get True boolean
                    bool_v_flag = any(item in list_vcodec for item in BC_v_standard[i])
                    if bool_v_flag:
                        BC_type.append(i) #add the position of the type of BC Standards

                BC_Standard_Names = ["DVD","ISDB","ATSC","DTMB"]
                # Faltaria acceder con las posiciones que he encontrado de BC_type, pintear con los tipos correspondientes


                #bool_DVD = list_codec.issubset(ISDB)
                #bool_DVD = list_codec.issubset(ATSC)
                #bool_DVD = list_codec.issubset(DTMB)

            if option == 0:
                print(
                    bcolors.HEADER + "It's been a pleasure, see you next time" + bcolors.ENDC)
                break
        except:
            print(
                bcolors.UNDERLINE + bcolors.FAIL + "Occur a error, please try again" + bcolors.ENDC)