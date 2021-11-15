# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def YUVfromRGB( R, G, B):
    Y = 0.257 * R + 0.504 * G + 0.098 * B + 16;
    U = -0.148 * R - 0.291 * G + 0.439 * B + 128; # also is the Cb
    V = 0.439 * R - 0.368 * G - 0.071 * B + 128; # also is the Cr

    return Y, U, V


def RGBfromYUV( Y ,U , V):

    R = 1.164 * (Y-16) + 2.018 * (U-128);
    G = 1.164 * (Y-16) - 0.813 * (V-128) - 0.391 * (U-128);
    B = 1.164 * (Y-16) + 1.596 * (V-128);

    return round(R),round(G),round(B)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #from os import sys, path
    #sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    #from ex_4 import run_length_encoding_numb

    """
    #Ex 1
    # creating an empty list
    list = []
    listRGBString = ["R","G","B"]
    print("Give me three values of R,G,B between [0,255] ")
    for i in range(0, 3):
        print("Values of",listRGBString[i])
        ele = int(input())
        list.append(ele)  # adding the element
    print(list)

    Y,U,V = YUVfromRGB(list[0], list[1], list[2])
    print("The value transform to YUV is: ", Y,U,V)
    R,G,B = RGBfromYUV(Y, U, V)
    print("Also we can check the function of YUVtoRGB give us the same values as the input values")
    print("RGB obtained from the own tranform function is: ",R,G,B);
    """

    bytes = [2,2,2,2,0,0,0,3];
    run_length_encoding_numb(bytes)



