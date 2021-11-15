
def run_length_encoding_numb(bytes):
    """
    :param bytes: a list of series of bytes of numbers
    :return: run-length encoded
    """
    #count = 0;
    #for i in range(len(bytes)):

    #    if (bytes[i]==0):
    #        count +=1;
    #    else
    #        bytes[i-count] # 3,4,5

def encode_message(message):
    encoded_string = ""
    i = 0
    while (i <= len(message) - 1):
        count = 1
        ch = message[i]
        j = i
        while (j < len(message) - 1):
            '''if the character at the current index is the same as the character at the next index. If the characters are the same, the count is incremented to 1'''
        if (message[j] == message[j + 1]):
            count = count + 1
            j = j + 1
        else:
            break
    '''the count and the character is concatenated to the encoded string'''
    encoded_string = encoded_string + str(count) + ch
    i = j + 1

    return encoded_string

