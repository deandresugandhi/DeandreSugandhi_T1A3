from termcolor import colored
import colorama

colorama.init(autoreset=True)

loun = colored("LOUNGE", "blue")
mat = colored("MATCH", "green")
ex = colored("EXIT", "red")

print(fr'''
        \_                                                _/
          \_                                            _/
            \                                      ____/
            |                                     |
            |______                         ______|
            |      |\ ___________________ /|      |      
            |      | |     _________     | |      |
            |      | |    |    |    |    | |      |
            |{loun}| |    |    |    |    | | {ex} |
            | <--- | |    |   o|o   |    | | ---> |       
            |      | |    |    |    |    | |      |
            |      | |____|____|____|____| |      |
            |______|/        {mat}        \|______|
            |                  .                  |
        ____|                 / \                 |___
      _/                     / | \                    \_
     /                         |                        \
                               |                               
    ''')



