import torch
import torch.nn as nn
import torchvision.transforms as T
from utils import Player, WINDOW_WIDTH
from PIL import Image, ImageDraw


player = Player()
    #Initializing a Player object with a random start position on a randomly generated Maze



def strategy(snapshot, map, draw = False):
    conv = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=51)
    conv.weight = nn.Parameter(snapshot)
    prob = conv(map)
    a = torch.argmax(prob.squeeze(0).squeeze(0))
    y, x = int(a/prob.squeeze(0).squeeze(0).shape[0]), int(a%prob.squeeze(0).squeeze(0).shape[0])
    coordinates = x + WINDOW_WIDTH/2 + 1, y + WINDOW_WIDTH/2 + 1
    if draw:
        map_pho = (T.ToPILImage()(map_T.squeeze(0).squeeze(0)))
        rgbimg = Image.new("RGBA", map_pho.size)
        rgbimg.paste(map_pho)
        draw = ImageDraw.Draw(rgbimg)
        draw.rectangle([(coordinates[0] - (WINDOW_WIDTH/2), coordinates[1] - (WINDOW_WIDTH/2)), (coordinates[0] + (WINDOW_WIDTH/2), coordinates[1] + (WINDOW_WIDTH/2))], outline="red", width = 1)
        draw.point(coordinates, fill='red')
        map_pho.save('output/map.png')
        (T.ToPILImage()(snapshot.squeeze(0).squeeze(0))).save("output/snap.png")
        rgbimg.save('output/map_with_loc.png')
    return coordinates

if __name__ == "__main__":
    snapshot = T.ToTensor()(player.getSnapShot()).unsqueeze(0)
    map_T = T.ToTensor()(player.getMap()).unsqueeze(0)
    coordinates = strategy(snapshot, map_T, True)
    
    # rgbimg.show()
    print("The UAV is at: ", coordinates)

