import torch
import torch.nn as nn
import torchvision.transforms as T
from utils import Player, WINDOW_WIDTH
from PIL import Image, ImageDraw


player = Player()



def strategy(player: Player, draw = False):
    snapshot = T.ToTensor()(player.getSnapShot()).unsqueeze(0)
    map = T.ToTensor()(player.getMap()).unsqueeze(0)
    Image.fromarray(player.getSnapShot()).convert('L').save('output/snapshot.png')
    conv = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=51)
    conv.weight = nn.Parameter(snapshot)
    
    prob = conv(map)
    prob = prob/torch.sum(prob)
    idx = [x for x in range(564)]
    coordinates = map.shape[0]/2, map.shape[1]/2  

    while torch.max(prob) < 0.3:
        player.move_horizontal(1)
        player.move_vertical(1)
        snapshot = T.ToTensor()(player.getSnapShot()).unsqueeze(0)
        conv.weight = nn.Parameter(snapshot)
        prob_ = conv(map)
        prob *= prob_[idx.insert(idx.pop(0), len(idx)-1)][idx.insert(idx.pop(0), len(idx)-1)].squeeze(0).squeeze(0)
        prob = prob/torch.sum(prob)

    a = torch.argmax(prob.squeeze(0).squeeze(0))
    y, x = int(a/prob.squeeze(0).squeeze(0).shape[0]), int(a%prob.squeeze(0).squeeze(0).shape[0])
    coordinates = x + WINDOW_WIDTH/2 + 1, y + WINDOW_WIDTH/2 + 1
    if draw:
        map_pho = (T.ToPILImage()(map_T.squeeze(0).squeeze(0)))
        rgbimg = Image.new("RGBA", map_pho.size)
        rgbimg.paste(map_pho)
        draw = ImageDraw.Draw(rgbimg)
        draw.rectangle((coordinates[0] - (WINDOW_WIDTH/2), coordinates[1] - (WINDOW_WIDTH/2), coordinates[0] + (WINDOW_WIDTH/2), coordinates[1] + (WINDOW_WIDTH/2)), outline="red", width = 2)
        draw.ellipse((coordinates[0] - 0.5, coordinates[1] - 0.5, coordinates[0] + 0.5, coordinates[1] + 0.5), fill='red')
        map_pho.save('output/map.png')
        rgbimg.save('output/map_with_loc.png')
    return coordinates

if __name__ == "__main__":
    snapshot = T.ToTensor()(player.getSnapShot()).unsqueeze(0)
    map_T = T.ToTensor()(player.getMap()).unsqueeze(0)
    coordinates = strategy(player, True)
    
    # rgbimg.show()
    print("The UAV is at: ", coordinates)

