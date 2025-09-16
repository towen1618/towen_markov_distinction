import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Transition Matrix to show probability of the next villain in the lineup given the last.
# A normal transition matrix would include an entry for each other possible villain, but in
# this case we assume any villain not listed has probability 0 of being next in line.
VILLAIN_RELATIONS = {
    'Green Goblin': {
        'Doctor Octopus': 0.4,
        'Venom': 0.3,
        'Kingpin': 0.2,
        'Carnage': 0.1
    },
    'Doctor Octopus': {
        'Green Goblin': 0.4,
        'Vulture': 0.3,
        'Sandman': 0.2,
        'Electro': 0.1
    },
    'Venom': {
        'Carnage': 0.4,
        'Green Goblin': 0.3,
        'Lizard': 0.2,
        'Scorpion': 0.1
    },
    'Sandman': {
        'Doctor Octopus': 0.4,
        'Vulture': 0.3,
        'Electro': 0.2,
        'Mysterio': 0.1
    },
    'Electro': {
        'Doctor Octopus': 0.4,
        'Sandman': 0.3,
        'Vulture': 0.2,
        'Shocker': 0.1
    },
    'Vulture': {
        'Doctor Octopus': 0.4,
        'Sandman': 0.3,
        'Electro': 0.2,
        'Mysterio': 0.1
    },
    'Mysterio': {
        'Doctor Octopus': 0.4,
        'Sandman': 0.3,
        'Vulture': 0.2,
        'Rhino': 0.1
    },
    'Rhino': {
        'Sandman': 0.4,
        'Electro': 0.3,
        'Mysterio': 0.2,
        'Scorpion': 0.1
    },
    'Lizard': {
        'Venom': 0.4,
        'Carnage': 0.3,
        'Scorpion': 0.2,
        'Morbius': 0.1
    },
    'Kraven the Hunter': {
        'Chameleon': 0.4,
        'Green Goblin': 0.3,
        'Vulture': 0.2,
        'Doctor Octopus': 0.1
    },
    'Kingpin': {
        'Green Goblin': 0.4,
        'Doctor Octopus': 0.3,
        'Hammerhead': 0.2,
        'Tombstone': 0.1
    },
    'Carnage': {
        'Venom': 0.4,
        'Green Goblin': 0.3,
        'Lizard': 0.2,
        'Scorpion': 0.1
    },
    'Scorpion': {
        'Venom': 0.4,
        'Carnage': 0.3,
        'Rhino': 0.2,
        'Shocker': 0.1
    },
    'Chameleon': {
        'Kraven the Hunter': 0.4,
        'Green Goblin': 0.3,
        'Doctor Octopus': 0.2,
        'Vulture': 0.1
    },
    'Shocker': {
        'Electro': 0.4,
        'Rhino': 0.3,
        'Scorpion': 0.2,
        'Sandman': 0.1
    },
    'Jackal': {
        'Green Goblin': 0.4,
        'Doctor Octopus': 0.3,
        'Carnage': 0.2,
        'Lizard': 0.1
    },
    'Morbius': {
        'Lizard': 0.4,
        'Venom': 0.3,
        'Carnage': 0.2,
        'Black Cat': 0.1
    },
    'Hammerhead': {
        'Kingpin': 0.4,
        'Tombstone': 0.3,
        'Doctor Octopus': 0.2,
        'Green Goblin': 0.1
    },
    'Tombstone': {
        'Kingpin': 0.4,
        'Hammerhead': 0.3,
        'Vulture': 0.2,
        'Rhino': 0.1
    },
    'Black Cat': {
        'Venom': 0.4,
        'Morbius': 0.3,
        'Kingpin': 0.2,
        'Green Goblin': 0.1
    }
}

# Dictionary of how to reach a villain's image given their name.
VILLAIN_TO_IMAGE = {
    'Green Goblin': 'green_goblin.jpeg',
    'Doctor Octopus': 'doctor_octopus.jpg',
    'Venom': 'venom.png',
    'Sandman': 'sandman.png',
    'Electro': 'electro.png',
    'Vulture': 'vulture.png',
    'Mysterio': 'mysterio.png',
    'Rhino': 'rhino.jpg',
    'Lizard': 'lizard.jpg',
    'Kraven the Hunter': 'kraven_the_hunter.webp',
    'Kingpin': 'kingpin.png',
    'Carnage': 'carnage.png',
    'Scorpion': 'scorpion.webp',
    'Chameleon': 'chameleon.webp',
    'Shocker': 'shocker.jpg',
    'Jackal': 'jackal.webp',
    'Morbius': 'morbius.jpg',
    'Hammerhead': 'hammerhead.png',
    'Tombstone': 'tombstone.png',
    'Black Cat': 'black_cat.jpg'
}

"""
A Sinister Six object takes an optional initial villain and builds a lineup of six villains using the
make_lineup function, as well as turns that lineup into an image with make_image.
"""
class SinisterSix:
    def __init__(self, villain1=None):
        self.transition_matrix = VILLAIN_RELATIONS
        if villain1 == None:
            # If no initial villain was input, pick a random one.
            self.curr_villain = np.random.choice(list(self.transition_matrix.keys()))
        else:
            self.curr_villain = villain1
    
    """
    Make a lineup of villains such that each new villain is associated with the previous.
    """
    def make_lineup(self):
        # Start with the input villain or randomly chosen one.
        lineup = [self.curr_villain]
        while len(lineup) < 6:
            # Pick the next villain using the transition matrix
            choices = list((self.transition_matrix[self.curr_villain]).keys())
            # If all related villains are already in the lineup, choose a random next villain.
            new_option = False
            # Check for a valid new villain
            for choice in choices:
                if choice not in lineup:
                    new_option = True
            # If there's none, keep picking random villains until a new one is chosen.
            while(new_option == False):
                self.curr_villain = np.random.choice(list(self.transition_matrix.keys()))
                if self.curr_villain not in lineup:
                    new_option = True
            else:
                # Keep picking randomly according to the probability distribution until a new villain is chosen.
                probabilities = list((self.transition_matrix[self.curr_villain]).values())
                while True:
                    new_villain = np.random.choice(choices, p=probabilities)
                    if new_villain not in lineup:
                        break
                self.curr_villain = new_villain
            lineup.append(self.curr_villain)
        return lineup
    
    """
    Take a lineup and output an image of the six villains in order
    """
    def make_image(self, lineup):
        for i in range(6):
            # Create a 1x6 template for the final image
            plt.subplot(1,6,i+1)
            # Find the associated image of a villain
            curr_image = Image.open('assets/' + VILLAIN_TO_IMAGE[lineup[i]])
            # Place it in the correct spot on the template
            plt.imshow(curr_image)
            plt.axis('off')
            plt.title(lineup[i], fontsize=8)
        plt.show()

def main():
    # Make a lineup, print it out, and show an image of it
    sinister_six = SinisterSix()
    my_lineup = sinister_six.make_lineup()
    print(my_lineup)
    sinister_six.make_image(my_lineup)

main()