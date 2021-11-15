def run_length_encode_message(message):
    """
    :param message:
    :return:
    """
    final_list = []
    i = 0
    bool_zero = False
    encoded_int = 0
    while (i <= len(message) - 1):
        count = 1
        ch = message[i]
        j = i
        if ch == 0:
            bool_zero = True
            while (j < len(message) - 1):
                '''if the character at the current index is the same as the character at the next index. If the characters are the same, the count is incremented to 1'''
                if (message[j] == message[j + 1]):
                    count = count + 1
                    j = j + 1
                else:
                    break
        else:
            bool_zero = False
            count = 0
        '''the count and the character is concatenated to the encoded string'''
        if (bool_zero):
            final_list.append(0)

        encoded_int = count + ch
        final_list.append(encoded_int)
        i = j + 1

    return final_list
