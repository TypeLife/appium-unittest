from PIL import Image


def calculate(image1, image2):
    g = image1.histogram()
    s = image2.histogram()
    assert len(g) == len(s), "error"

    data = []

    for index in range(0, len(g)):
        if g[index] != s[index]:
            data.append(1 - abs(g[index] - s[index]) / max(g[index], s[index]))
        else:
            data.append(1)

    return sum(data) / len(g)


def split_image(image, part_size):
    pw, ph = part_size
    w, h = image.size

    sub_image_list = []

    assert w % pw == h % ph == 0, "error"

    for i in range(0, w, pw):
        for j in range(0, h, ph):
            sub_image = image.crop((i, j, i + pw, j + ph)).copy()
            sub_image_list.append(sub_image)

    return sub_image_list


def classfiy_histogram_with_split(image1, image2, size=(256, 256), part_size=(64, 64)):
    ''' 'image1' and 'image2' is a Image Object.
    You can build it by 'Image.open(path)'.
    'Size' is parameter what the image will resize to it.It's 256 * 256 when it default.
    'part_size' is size of piece what the image will be divided.It's 64*64 when it default.
    This function return the similarity rate betweene 'image1' and 'image2'
    '''
    image1 = image1.resize(size).convert("RGB")
    sub_image1 = split_image(image1, part_size)

    image2 = image2.resize(size).convert("RGB")
    sub_image2 = split_image(image2, part_size)

    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)

    x = size[0] / part_size[0]
    y = size[1] / part_size[1]

    pre = round((sub_data / (x * y)), 3)
    return pre


__all__ = [
    classfiy_histogram_with_split
]


def get_similar_degree(fp1, fp2):
    img1 = Image.open(fp1)
    img2 = Image.open(fp2)
    result = classfiy_histogram_with_split(img1, img2)
    return result


def get_pixel_point_color(fp, x, y, by_percent=False, mode='RGBA'):
    """
    获取图片某一像素点的颜色
    :param mode: RGB \ RGBA
    :param by_percent: 是否使用百分比
    :param fp: 图片文件路径
    :param x: X轴坐标
    :param y: Y轴坐标
    :return: RGBA
    """
    from PIL import Image

    with Image.open(fp) as img:
        img_src = img.convert(mode)
        pixel_data = img_src.load()
        if by_percent:
            x = img.width * (x / 100)
            y = img.height * (y / 100)
        data = pixel_data[x, y]
        return data
