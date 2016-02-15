# coding = utf-8

import types, os
from PIL import Image, ImageDraw

# 打开
def show(image_path=None):
    if image_path is None or len(image_path) == 0:
        return

    im = Image.open(image_path)
    im.show()

# 保存
def save(image=None, to_path=None):
    if image is None or to_path is None or len(to_path) == 0:
        return

    f, e = os.path.splitext(to_path)
    if e is None or len(e) == 0:
        image.save(to_path, "JPEG")
    else:
        image.save(to_path)

# 大小
def size(image=None):
    ret_size = (0, 0)

    im = image
    if type(image) is types.StringType:
        im = Image.open(image)

    if image is None:
        return ret_size

    return im.size()

# 拷贝
def copy(image=None):
    im = image
    if type(image) is types.StringType:
        im = Image.open(image)

    if im is None:
        return None

    return im.copy()

# 裁剪
def crop(image=None, box=None):
    if image is None or box is None:
        return None

    im = image
    if type(image) is types.StringType:
        im = Image.open(image)
        if im is None:
            return None

    return im.crop(box)

# 压缩
def get_thumb(image=None, ratio=0.6):
    if ratio > 1:
        return image
    if ratio <= 0:
        return None

    im = image
    if type(image) is types.StringType:
        im = Image.open(image)

    if im is None:
        return None

    w, h = im.size()

    return im.thumbnail((w * ratio, h * ratio))

# 粘贴
def paste(image=None, sub_image=None, box=None):
    if image is None or sub_image is None or box is None:
        return None

    im = image
    if type(image) is types.StringType:
        im = Image.open(image)
        if im is None:
            return None

    sub_im = sub_image
    if type(sub_image) is types.StringType:
        sub_im = Image.open(sub_image)
        if sub_im is None:
            return None

    return im.paste(sub_im, box)

# 添加文字
def draw_text(image=None, text=None, origin=(0, 0), font=None):
    if image is None or text is None or len(text) == 0:
        return None

    im = image
    if type(image) is types.StringType:
        im = Image.open(image)
        if im is None:
            return None

    context = ImageDraw.Draw(im)
    context.text(origin, text, font=font)
    return im

# 旋转
def rotate(image=None, rotate=0):
    im = image
    if type(image) is types.StringType:
        im = Image.open(image)

    if im is None:
        return None

    if rotate == 0:
        return im

    return im.rotate(rotate)

# 转换, mode: 'P'虚化,'L'或者'1'黑白,'LA'怀旧
def convert(image=None, mode='P'):
    im = image
    if type(image) is types.StringType:
        im = Image.open(image)

    if im is None:
        return None

    return im.convert(mode)
