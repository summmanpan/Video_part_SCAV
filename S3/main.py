
#import libraries
import os
import ipaddress

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

class FFMpeg_S3:
    def __init__(self, input_v):
        self.input = input_v

class codecVideo_class:
    def __init__(self):
        self.diff_reso_videos = ["1280x720", "640x480", "360x240", "160x120"]
        self.diff_codec = ["VP8","VP9","h265","av1"]
        self.dir_name = "converted_videos/"

    def converted_video_auto(self):
        os.system("mkdir -p "+self.dir_name)
        input_v = "v_scales/output_"
        for i in range(len(self.diff_reso_videos)):
            os.system("ffmpeg -i " + input_v + self.diff_reso_videos[i]+ ".mp4 -c:v "
            "libvpx -b:v 1M -c:a libvorbis "+self.dir_name+"v_VP8_"+self.diff_reso_videos[
                i]+".webm")
            os.system("ffmpeg -i " + input_v + self.diff_reso_videos[i]+".mp4 -c:v "
            "libvpx-vp9 -c:a libopus "+self.dir_name+"v_VP9_"+self.diff_reso_videos[
                i]+".webm")
            os.system("ffmpeg -i " + input_v + self.diff_reso_videos[i] +".mp4 -c:v"
            " libx265 -crf 26 -preset fast -c:a aac -b:a 128k "+self.dir_name+""
            "v_h265_"+self.diff_reso_videos[i]+".mp4")
            os.system("ffmpeg -i " + input_v + self.diff_reso_videos[i]+".mp4 -c:v "
            "libaom-av1 -crf 30 -b:v 0 "+self.dir_name+"v_av1_"+self.diff_reso_videos[
                i]+".mkv")

##########################
##########################

if __name__ == '__main__':

    main_menu = """

    Please, choose the option you like:

    1) Convert videos into VP8, VP9, h265 & AV1
    2) Export 2 video comparison
    3) Create a live streaming of the BBB video
    4) Choose the IP to broadcast the previous video
    0) Exit

    """
    print(
        bcolors.OKCYAN + bcolors.BOLD + "   Hi ^^ let's get start the tour of FFMPEG" + bcolors.ENDC)
    input_v = input("Enter your video name, if not, enter d for "
                    "default :")
    if input_v == "d":
        input_v = "videos/BigBuckBunny_512kb.mp4"
    CodecVideo = codecVideo_class()
    while True:
        try:

            print(bcolors.OKCYAN + bcolors.BOLD + main_menu + bcolors.ENDC)
            option = int(input("Enter your option "))
            if option == 1:
                #We automatize all these tasks inside a new class
                CodecVideo.converted_video_auto()
            if option == 2:
                #To archive this task we will follow this link:
                """https://stackoverflow.com/questions/11552565/vertically-or-horizontally-stack-mosaic-several-videos-using-ffmpeg"""
                while True:
                    user_stack_type = int(input(bcolors.MENU + bcolors.BOLD +
                        """
                    Enter the option you want :
                    1) Vertical stack
                    2) Horizontal stack
                    3) Visual comparison With the blend filter
                    0) Exit
                    """+ bcolors.ENDC)) #3) 2x2 Stack with all codecs types
                    input0 = CodecVideo.dir_name + "v_VP8_1280x720.webm"
                    input1 = CodecVideo.dir_name + "v_VP9_1280x720.webm"
                    input2 = CodecVideo.dir_name + "v_h265_1280x720.mp4"
                    input3 = CodecVideo.dir_name + "v_av1_1280x720.mkv"
                    stacktype = ["vstack", "hstack"]
                    if user_stack_type == 1:
                        os.system(
                            "ffmpeg -i "+input0+" -i "+input1+" -filter_complex "
                            ""+stacktype[0]+"=inputs=2 output_stack_vertical.mp4")
                    elif user_stack_type == 2:
                        os.system(
                            "ffmpeg -i " + input0 + " -i " + input1 + " -filter_complex "
                            ""+stacktype[1] + "=inputs=2 "
                                              "output_stack_horizontal.mp4")
                    elif user_stack_type == 3:
                        os.system("ffmpeg -i "+input0+" -i "+input1+" "
                                  "-filter_complex blend=all_mode=difference " 
                        "-c:v libx264 -crf 18 -c:a copy output_blend_diff.mkv")
                    elif user_stack_type == 0:
                        break
            if option == 3:
                os.system("ffmpeg -i "+input_v+" -v 0 -vcodec mpeg4 -f mpegts "
                                       "udp://127.0.0.1:23000")
                # Where the[output-stream-URI] is locahost:port
                # Since the IP address 127.0. 0.1 is called a loopback address,
                # and it refers to local equipment, therefore is exactly the one
                # we are looking for.

            if option == 4:

                while True:
                    try:
                        ip_address = input("Enter the ip address you want to "
                                           "broadcast the video: ")
                        ip = ipaddress.ip_address(ip_address)
                        print(f'{ip} is correct. Version: IPv{ip.version}')
                        break
                    except ValueError:
                        print(bcolors.UNDERLINE + bcolors.FAIL +'Adress is invalid, please try again'+ bcolors.ENDC)

                user_port = input("Enter the port: ")

                if int(user_port)<1 or int(user_port)>65535:
                    raise "Error port number"
                os.system(
                    "ffmpeg -i " + input_v + " -v 0 -vcodec mpeg4 -f mpegts "
                                             "udp://"+ip_address+":"+user_port)

            if option == 0:
                print(
                    bcolors.HEADER + "It's been a pleasure, see you next time" + bcolors.ENDC)
                break
            if option>4 and option < 0:
                raise "Error of user input"
        except:
            print(
                bcolors.UNDERLINE + bcolors.FAIL + "Occur a error, please try again" + bcolors.ENDC)