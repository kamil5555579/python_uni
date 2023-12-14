import argparse
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import rich
from rich.progress import track
import time

parser = argparse.ArgumentParser(description="Ising model simulation")
parser.add_argument('--size', '-s', help="the size of the lattice", type=int, default=150)
parser.add_argument('-J', help="the coupling constant", type=float, default=1.0)
parser.add_argument('-B', help="the external magnetic field", type=float, default=0.0)
parser.add_argument('-beta', help="the inverse temperature", type=float, default=0.01)
parser.add_argument('-n', help="the number of iterations", type=int, default=100)
parser.add_argument('--up_percantage', '-u', help="the percentage of up spins", type=float, default=0.5)
parser.add_argument('--image', '-i', help="the name of the image file to save to", type=str)
parser.add_argument('--animation', '-a', help="the name of the animation file to save to", type=str, default="animation1")
parser.add_argument('--magnetization', '-m', help="the name of the file to save the magnetization to", type=str, default="magnetization1")

args = parser.parse_args()

class IsingModel:
    def __init__(self) -> None:
        self.lattice = np.random.choice([-1, 1], size=(args.size, args.size), p=[1 - args.up_percantage, args.up_percantage])
        self.J = args.J
        self.B = args.B
        self.beta = args.beta

    def change_spin(self, i, j):
        self.lattice[i, j] *= -1

    def get_energy(self, i, j):
        lat = self.lattice
        spins = lat[i, j] * (lat[(i+1)%args.size, j] + lat[i-1, j] + lat[i, (j+1)%args.size] + lat[i, j-1])
        h = -self.J * spins - self.B * lat[i, j]
        
        return h
    
    def check_energy(self, i, j):
        e0 = self.get_energy(i, j)
        self.change_spin(i, j)
        e1 = self.get_energy(i, j)

        delta_E = e1 - e0

        if delta_E > 0:
            p = np.exp(-self.beta * delta_E)
            r = np.random.random()
            if r < p:
                self.change_spin(i, j)

    def get_magnetization(self):
        return np.sum(self.lattice)/self.lattice.size
    
    def draw(self, step):
        image_size = 1000
        scale = image_size/args.size
        img = Image.new('RGB', (image_size, image_size), color='white')
        draw = ImageDraw.Draw(img)

        for i in range(args.size):
            for j in range(args.size):
                color = 255 if self.lattice[i, j] == 1 else 0
                draw.rectangle((i*scale, j*scale, (i+1)*scale, (j+1)*scale), fill=(color, color, color))

        if args.image:
            img.save(args.image+'_'+str(step)+'.png')

        return img
        

model = IsingModel()

def ising_generator(n):

    step = 0
    while step < n:
        for ministep in range(args.size**2):
            i = np.random.randint(args.size)
            j = np.random.randint(args.size)
            model.check_energy(i, j)

        yield model.draw(step), model.get_magnetization()

        step += 1

images=[]
magnetizations=[]

rich.print('[bold green]Starting simulation...[/bold green]')
start = time.time()

for image, magnetization in track(ising_generator(args.n), description="Processing..."):
    images.append(image)
    magnetizations.append(magnetization)

end = time.time()
rich.print('[bold green]Simulation finished...[/bold green]')
rich.print(f'[bold green]It took {end - start} seconds to execute[/bold green]')

if args.animation:
    images[0].save(args.animation+'.gif', save_all=True, append_images=images[1:], duration=100, loop=0)

if args.magnetization:
    plt.plot(magnetizations)
    plt.savefig(args.magnetization+'.png')
