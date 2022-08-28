from blockChain.BlockChain import Blockchain
from utils.generation import generate_nodes, selected_to_dict, choose_dataset
from utils.displays import display_author
from colorama import init, Fore
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
init(autoreset=True)

# TODO: Generating sphinx documentations.

# TODO: Transform data to IMBD dataset.

if __name__ == '__main__':
    display_author()  # * Display authors information

    blockChain = Blockchain()

    blockChain.create_genesis_block()

    print("{0}First Block Hash : {1} ".format(Fore.LIGHTRED_EX, blockChain.last_block.hash))

    # ! -------------------------------------------- Generation process ------------------------------------------------

    # ? Choose how many nodes you want to simulate.
    number_of_nodes = int(input("{0}How Many nodes do you want to simulate ?\n> ".format(Fore.LIGHTYELLOW_EX)))

    # ? Specify the percentage of choice of the participant clients.
    selection_percentage = int(input("{0}What percentage of participating clients do you want?\n> ".
                                     format(Fore.LIGHTYELLOW_EX))) / 100

    # ? Choosing the dataset ( 1 = MNIST, 2 = Fashion MNIST, 3 = CIFAR 100).
    dataset_id, train_dataset, test_dataset = choose_dataset()

    # ? Generate the number chosen of nodes.
    clients = generate_nodes(number_of_nodes=number_of_nodes, data=train_dataset)