# pylint: disable = C0114, C0115, C0116, C0103

from colorama import Fore


def display_author():
    print(f"""{Fore.CYAN}
     ______ _                  _____ _                 _       _   _             
    |  ____| |                / ____(_)               | |     | | (_)            
    | |__  | |       ______  | (___  _ _ __ ___  _   _| | __ _| |_ _  ___  _ __  
    |  __| | |      |______|  \___ \| | '_ ` _ \| | | | |/ _` | __| |/ _ \| '_ \ 
    | |    | |____            ____) | | | | | | | |_| | | (_| | |_| | (_) | | | |
    |_|    |______|          |_____/|_|_| |_| |_|\__,_|_|\__,_|\__|_|\___/|_| |_|
                                                                                 """)
    print(f"{Fore.YELLOW}🤖 {Fore.MAGENTA}By AICHE Mohamed")

    print(Fore.MAGENTA + "-" * 20)
