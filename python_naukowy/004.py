import argparse
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import rich
import time
import numba

parser = argparse.ArgumentParser(description="Ising model simulation")
parser.add_argument('--size', '-s', help="the size of the lattice", type=int, default=150)
parser.add_argument('-J', help="the coupling constant", type=float, default=1.0)
parser.add_argument('-B', help="the external magnetic field", type=float, default=0.0)
parser.add_argument('-beta', help="the inverse temperature", type=float, default=0.01)
parser.add_argument('-n', help="the number of iterations", type=int, default=200)
parser.add_argument('--up_percantage', '-u', help="the percentage of up spins", type=float, default=0.5)
parser.add_argument('--image', '-i', help="the name of the image file to save to", type=str)
parser.add_argument('--animation', '-a', help="the name of the animation file to save to", type=str, default="animation2")
parser.add_argument('--magnetization', '-m', help="the name of the file to save the magnetization to", type=str, default="magnetization2")

args = parser.parse_args()

lattice = np.random.choice([-1, 1], size=(args.size, args.size), p=[1 - args.up_percantage, args.up_percantage])
J = args.J
B = args.B
beta = args.beta
size = args.size
n = args.n

states = []
images = []
magnetizations = []

@numba.njit()
def change_spin(lattice, i, j):
    lattice[i, j] *= -1
    return lattice

@numba.njit()
def get_energy(lat, i, j, J, B, size):
    spins = lat[i, j] * (lat[(i+1)%size, j] + lat[i-1, j] + lat[i, (j+1)%size] + lat[i, j-1])
    h = -J * spins - B * lat[i, j]
    return h

@numba.njit()
def check_energy(lat, i, j, J, B, beta):
    e0 = get_energy(lat, i, j, J, B, size)
    lat = change_spin(lat, i, j)
    e1 = get_energy(lat, i, j, J, B, size)

    delta_E = e1 - e0

    if delta_E > 0:
        p = np.exp(beta * delta_E)
        r = np.random.random()
        if r < p:
            lat = change_spin(lat, i, j)
    
    return lat

def get_magnetization(lattice):
    return np.sum(lattice)/lattice.size

def draw(lattice, step):
        image_size = 1000
        scale = image_size/args.size
        img = Image.new('RGB', (image_size, image_size), color='white')
        draw = ImageDraw.Draw(img)

        for i in range(args.size):
            for j in range(args.size):
                color = 255 if lattice[i, j] == 1 else 0
                draw.rectangle((i*scale, j*scale, (i+1)*scale, (j+1)*scale), fill=(color, color, color))

        if args.image:
            img.save(args.image+'_'+str(step)+'.png')

        return img

@numba.njit()
def simulation(lattice, J, B, beta, size, n):
    states = []
    states.append(lattice.copy())
    for step in range(n):
        for ministep in range(size**2):
            i = np.random.randint(size)
            j = np.random.randint(size)
            lattice = check_energy(lattice, i, j, J, B, beta)
        
        state = lattice.copy()
        states.append(state)
    return states

def draw_simulation(states, n):
    for step in range(n):
        image = draw(states[step], step)
        magnetization = get_magnetization(states[step])
        images.append(image)
        magnetizations.append(magnetization)


rich.print('[bold green]Starting simulation...[/bold green]')

start = time.time()

states = simulation(lattice, J, B, beta, size, n)

end = time.time()
rich.print('[bold green]Simulation finished![/bold green]')
rich.print(f'[bold green]It took {end - start} seconds to execute[/bold green] with numba')

draw_simulation(states, n)

if args.animation:
    images[0].save(args.animation+'.gif', save_all=True, append_images=images[1:], duration=100, loop=0)
    print('Animation saved!')

if args.magnetization:
    plt.plot(magnetizations)
    plt.savefig(args.magnetization+'.png')
    print('Magnetization saved!')

