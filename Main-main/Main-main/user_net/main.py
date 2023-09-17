
from network import Network




def main():
    run = True
    n = Network()

    while run:

        data = input("전송: ")
        n.send(data)

main()