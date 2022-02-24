from PIL import Image, ImageFont, ImageDraw

image = Image.open("assets/sudoku-blankgrid.png")

image_editable = ImageDraw.Draw(image)

image_font = ImageFont.truetype("arial.ttf", 15)

output = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

def parseOutput(arr):
    for row in range(len(arr)):
        for index in range(len(arr[row])):
            horizontal_section = index // 3
            vertical_section = row // 3
            image_editable.text((8+47*(index+1/2)-15/2+4*horizontal_section, 8+45*(row+1/2)-15/2+4*vertical_section), str(arr[row][index]), (0, 0, 0), font=image_font)
    image.save("result.png")

parseOutput(output)