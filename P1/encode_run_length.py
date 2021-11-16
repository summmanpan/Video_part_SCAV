
# Encode the message for strings
def encode_message(message):
    encoded_string = ""
    i = 0
    print("hello")
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

def run_length_encode_message(message):
    """
    :param message: series of bytes as integers within a list
    :return: a list with the encoded message using run length algorithm
    """
    final_list = []
    i = 0; bool_zero = False; encoded_int = 0
    while (i <= len(message) - 1):
        count = 1
        ch = message[i]
        j = i
        if ch == 0:
            bool_zero = True
            while (j < len(message) - 1):
                '''if the character at the current index is the same as the 
                character at the next index. If the characters are the same, 
                the count is incremented to 1'''
                if (message[j] == message[j + 1]):
                    count = count + 1
                    j = j + 1
                else:
                    break
        else:
            bool_zero = False
            count = 0

        if (bool_zero):
            final_list.append(0)
        '''the count and the character is concatenated to the encoded_int'''
        encoded_int = count + ch
        final_list.append(encoded_int)
        i = j + 1

    return final_list

if __name__ == '__main__':
    print("Lets see a example of Run length encoding")
    original_data_stream = [2, 0, 0, 4, 0, 0, 7, 0, 0, 0, 0, 5,
                            0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 1]
    print("The original data stream is :\n",original_data_stream)
    encoded_mes = run_length_encode_message(original_data_stream)
    print("After, run length encoding the message is :\n", encoded_mes)
    print("\t")
    print("Now ,try to introduce your own data stream ")
    print("If you want to exit the program, please enter e to exit ")
    finish_flag = True
    while (finish_flag):
        try:
            input_bytes = input("Enter series of byes (numbers) that you want to"
                                    " encode (separated by space):\n")
            if input_bytes=="e":
                finish_flag = False
                break

            user_list = input_bytes.split()
            print('list: ', user_list)
            # convert each item to int type
            for i in range(len(user_list)):
                # convert each item to int type
                user_list[i] = int(user_list[i])
            encoded_mes_user = run_length_encode_message(user_list)
            print("The run length encoded message from user :\n", encoded_mes_user)
        except:
            print("Error! try again!")
