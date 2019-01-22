from PIL import ImageColor, Image, ImageOps

from ..gui import font
from ..gui.const import DEF_MAP_SIZE
from .tiles import BIOMES


class Map:
    """ Base class for a map object

    A map is a 2D array (list of lists) that contain pointers to tile/biome
    data.
    
    Maps can be parsed from an image where each pixel uses a pre-defined
    RGB value to represent a specific tile or biome
    
    Returns:
        [type] -- [description]
    """


    def __init__(self, filename, tileset=BIOMES):
        self.tileset = tileset
        self.map_key = self.get_map_key(tileset=self.tileset)
        self.cols, self.rows = self.size = (0, 0)
        self.map = self._load_map(filename)


    def get_map_key(self, tileset=BIOMES):
        """ Builds color : tile map key
        
        Keyword Arguments:
            tileset {[type]} -- [description] (default: {BIOMES})
        """

        return{ v['img_color'] : k for k, v in tileset.items() }


    def _load_map(self, filename):
        """ Loads an image file and parses it into a map
        
        Arguments:
            filename {[type]} -- [description]
        
        Keyword Arguments:
            mirror {bool} -- [description] (default: {True})
            rotate {int} -- [description] (default: {90})
        
        Returns:
            [type] -- [description]
        """
        
        image = Image.open(filename)

        # update map size based on loaded image
        self.cols, self.rows = self.size = image.size

        # generate color key used to parse map image into a 2D array of tile dicts
        map_key = self.get_map_key()

        # image data is collected row by row, so pixels end up being stored in
        pixels = [x for x in list(image.getdata())]

        tiles = []
        for rgb in pixels:
            if rgb not in self.map_key:
                print(f'{rgb} not in map key!')
                tiles.append(None)
            else:
                tile_key = self.map_key[rgb]
                tiles.append(self.tileset[tile_key])            

        # tiles = [self.tileset[self.map_key[rgb]] for rgb in pixels]

        # converts long list of tiles into 2D array (list of lists)
        _map = [tiles[i:(i + self.cols)] for i in range(0, len(tiles), self.cols)]
        # mirrors array
        _map = _map[::-1]
        # rotates array by 90 degrees CCW
        _map = list(zip(*_map[::-1]))

        return _map


    def get_map_segment(self, size, offset=(0,0)):
        """ Gets a portion of the map array

        Gets a portion of the map array so it can be displayed in the game window

        Arguments:
            map_array {list} -- 2D list of lists that holds tile data for map
            size {tuple} -- number of (rows, cols) of the map to return
            offset {tuple} -- starting (row,col) of the segment

        Notes:
            Need to account for the window being positioned in a way that attempts
            to get out of range data
        """

        pass


    def show(self):
        """ Prints the map array """
        for row in range(self.rows):
            line = ''
            for col in range(self.cols):
                try:
                    tile = self.map[col][row]
                    if tile is not None:
                        char = tile['symbol']
                        char = font.add_escape(char, **tile['format'])
                        # print(char)
                        line = line + char
                    else:
                        line = line + ' '                    
                except IndexError:
                    pass
                    # print(f'tile = self.map[{col}][{row}]')

            print(line)