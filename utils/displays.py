from colorama import Fore


def displayAuthor():
    print("""{}
     ______ _                  _____ _                 _       _   _             
    |  ____| |                / ____(_)               | |     | | (_)            
    | |__  | |       ______  | (___  _ _ __ ___  _   _| | __ _| |_ _  ___  _ __  
    |  __| | |      |______|  \___ \| | '_ ` _ \| | | | |/ _` | __| |/ _ \| '_ \ 
    | |    | |____            ____) | | | | | | | |_| | | (_| | |_| | (_) | | | |
    |_|    |______|          |_____/|_|_| |_| |_|\__,_|_|\__,_|\__|_|\___/|_| |_|
                                                                                 """.format(Fore.CYAN))
    print("{}🤖 {}By AICHE Mohamed".format(Fore.YELLOW, Fore.MAGENTA))

    print(Fore.MAGENTA + "-" * 20)
