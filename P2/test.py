if __name__ == '__main__':



    while True:

            start_end_times = input("fff").split()
            start_times = start_end_times[0];
            end_times = start_end_times[1]
            print("Start time is :", start_times, "End time is :", end_times)

            # we take directly the elements of the list
            hour, min, sec = [int(i) for i in start_times.split(":")]
            if 0 > hour or hour > 24 or 0 > min or min > 60 or 0 > sec or sec > 60:
                raise "Error of user input"
            break
            hour, min, sec = [int(i) for i in end_times.split(":")]



    
    for time in start_end_times:
        # we take directly the elements of the list
        print(time)
        hour, min, sec = [int(i) for i in time.split(":")]
        print(hour, min, sec)
        #if 0 < hour < 24 and 0 < min < 60 and 0 < sec < 60:

    for time in end_times:
        # we take directly the elements of the list

        hour, min, sec = [int(i) for i in end_times.split(":")]

        #if 0 < hour < 24 and 0 < min < 60 and 0 < sec < 60:
    print(hour, min, sec)
