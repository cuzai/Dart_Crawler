import datetime


def write_log(msg):
    with open("./log.txt", "a") as w:
        w.write("{} - {}\n".format(datetime.datetime.today(), msg))


if __name__ == "__main__":
    write_log("hello")
