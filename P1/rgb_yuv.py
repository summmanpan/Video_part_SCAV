
def YUVfromRGB( R, G, B):
    """
    :param R: a integer of channel R
    :param G: a integer of channel G
    :param B: a integer of channel B
    :return: 3 values of integers from RGB to YUV
    """
    Y = 0.257 * R + 0.504 * G + 0.098 * B + 16;
    U = -0.148 * R - 0.291 * G + 0.439 * B + 128; # also is the Cb
    V = 0.439 * R - 0.368 * G - 0.071 * B + 128; # also is the Cr

    return Y, U, V


def RGBfromYUV( Y ,U , V):
    """
    :param Y: a integer of channel Y
    :param U: a integer of channel U
    :param V: a integer of channel V
    :return: 3 values of integers from YUV to RGB
    """
    R = 1.164 * (Y-16) + 1.596 * (V-128);
    G = 1.164 * (Y-16) - 0.813 * (V-128) - 0.391 * (U-128);
    B = 1.164 * (Y-16) + 2.018 * (U-128);

    return round(R),round(G),round(B)


if __name__ == '__main__':

    # creating an empty list
    try:
        list = []
        listRGBString = ["R","G","B"]
        print("Give me three values (numbers) of R,G,B between [0,255] ")
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
    except:
        print("There is a error")
