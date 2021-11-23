import os


# import subproces
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
    while True:
        try:
            print(bcolors.OKCYAN + bcolors.BOLD + main_menu + bcolors.ENDC)
            option = int(input("Enter your option "))
            if option == 1:
                os.system("ffmpeg -flags2 +export_mvs -i videos/cut.mp4 -vf codecview=mv=pf+bf+bb videos/output_motion_vec.mp4")
            if option == 2:
                cut_video_name = "videos/cut_1min.mp4"

                audio_acc_name = "acc_audio.aac"
                os.system("ffmpeg -ss "+"00:00:00"+" -i "+input_video+" -to "+"00:01:00"+" -c copy "+cut_video_name)
                os.system("ffmpeg -i "+cut_video_name+" -ac 1 -c copy -c:a aac "+audio_acc_name)

            if option == 0:
                print(
                    bcolors.HEADER + "It's been a pleasure, see you next time" + bcolors.ENDC)
                break
        except:
            print(
                bcolors.UNDERLINE + bcolors.FAIL + "Occur a error, please try again" + bcolors.ENDC)