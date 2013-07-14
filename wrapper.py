# -*- coding: utf-8 -*-
from PIL import ImageDraw
from PIL import ImageEnhance
from PIL import Image
from PIL import ImageOps
from PIL import ImageChops
from PIL import ImageFilter
from ast import literal_eval


DEFAULT_LOAD_PATH = 'tmp/'
DEFAULT_SAVE_PATH = 'static/'
DEFAULT_IMAGE_NAME = 'default.png'
DEFAULT_IMAGE_FORMAT = 'PNG'
COLOR_FORMAT = 'RGB'
ACTION_NAME_ATTR = 'name'
ACTION_OPTIONS_ATTR = 'options'


class imgProcessingWrapperPIL(object):
    """
    PIL wrapper with vector actions processing
    Usage:
    processor = imgProcessingWrapperPIL('cart.png')
    acts = [{'name':'grayscale',  'options':[]}, 
                {'name':'rotate',  'options':[90]}, 
                {'name':'mirror',  'options':[]}, 
                {'name':'filter',  'options':['find_edges']}, 
                {'name':'save',  'options':['test_json.png']}, 
    ]
    processor.process_actions(acts)
    """
    def __init__(self,  img_path,  save_path=DEFAULT_SAVE_PATH,  load_path=DEFAULT_LOAD_PATH,
                 color_format=COLOR_FORMAT):
        self._save_path = save_path
        self._load_path = load_path
        self._color_format = color_format
        self._img_path = img_path

        self._filters_list = {'blur': ImageFilter.BLUR, 
                              'contour': ImageFilter.CONTOUR,
                              'detail': ImageFilter.DETAIL,
                              'edge_enhance': ImageFilter.EDGE_ENHANCE,
                              'edge_enhance_more': ImageFilter.EDGE_ENHANCE_MORE,
                              'emboss': ImageFilter.EMBOSS,
                              'find_edges': ImageFilter.FIND_EDGES,
                              'smooth': ImageFilter.SMOOTH,
                              'smooth_more': ImageFilter.SMOOTH_MORE,
                              'sharpen': ImageFilter.SHARPEN,
                              'min': ImageFilter.MinFilter(),
                              'median': ImageFilter.MedianFilter(),
                              'max': ImageFilter.MaxFilter(),
                              'mode': ImageFilter.ModeFilter()}

    def process_actions(self,  actions, callback=None, *args, **kwargs):
        image = self._open_img(self._img_path)
        for action in actions:
            image = self._process_command(image,  action[ACTION_NAME_ATTR],  action[ACTION_OPTIONS_ATTR])
        if callback is not None:
            callback(*args, **kwargs)

    def _process_command(self,  img,  name,  options=None):
        color_enhancer = ImageEnhance.Color(img.convert(self._color_format))
        brightness_enhancer = ImageEnhance.Brightness(img.convert(self._color_format))
        contrast_enhancer = ImageEnhance.Contrast(img.convert(self._color_format))
        sharpness_enhancer = ImageEnhance.Sharpness(img.convert(self._color_format))
        operators = {'crop': self._crop_wrap(img), 
                     'filter': self._filter_wrap(img), 
                     'resize': self._resize_wrap(img.resize), 
                     'rotate': self._rotate_wrap(img.rotate), 
                     'text': self._text_wrap(img), 
                     'invert': self._invert_wrap(img),
                     'colorbalance': color_enhancer.enhance, 
                     'brightnessbalance': brightness_enhancer.enhance, 
                     'contrastbalance': contrast_enhancer.enhance, 
                     'sharpnessbalance': sharpness_enhancer.enhance, 
                     'addborder': self._addBorder_wrap(img), 
                     'flip': self._flip_wrap(img), 
                     'grayscale': self._grayscale_wrap(img), 
                     'mirror': self._mirror_wrap(img), 
                     'posterize': self._posterize_wrap(img), 
                     'solarize': self._solarize_wrap(img), 
                     'save': self._save_img(img), 
                     'paste': self._paste_wrap(img)}
        if name in operators.keys():
            if options is None or not len(options):
                return operators[name]()
            return operators[name](*options)
        return img

    def _resize_wrap(self, func):
        def result(argue):
            return func(argue, Image.ANTIALIAS)
        return result

    def _rotate_wrap(self, func):
        def result(argue):
            return func(argue, Image.BICUBIC, True)
        return result

    def _invert_wrap(self, img):
        def result():
            return ImageChops.invert(img)
        return result

    def _filter_wrap(self, img):
        def result(filter_name):
            return img.filter(self._filters_list[filter_name])
        return result

    def _addBorder_wrap(self, img):
        def result(border, color):
            return ImageOps.expand(img,  border,  color)
        return result

    def _flip_wrap(self, img):
        def result():
            return ImageOps.flip(img)
        return result

    def _grayscale_wrap(self, img):
        def result():
            return ImageOps.grayscale(img)
        return result

    def _mirror_wrap(self, img):
        def result():
            return ImageOps.mirror(img)
        return result

    def _posterize_wrap(self, img):
        def result(bits):
            return ImageOps.posterize(img, bits)
        return result

    def _solarize_wrap(self, img):
        def result(treshold):
            return ImageOps.solarize(img, treshold)
        return result

    def _paste_wrap(self, img):
        def result(nimg, args):
            watermark = self._open_img(nimg)
            box = literal_eval(args)
            img.paste(watermark, box, watermark)
            return img
        return result

    def _crop_wrap(self, img):
        def result(args):
            box = literal_eval(args)
            img.crop(box)
            return img
        return result

    def _text_wrap(self, img):
        def result(args, string, color):
            draw = ImageDraw.Draw(img)
            box = literal_eval(args)
            draw.text(box, string, color)
            return img
        return result

    def _open_img(self, name):
        return Image.open(self._load_path+name)

    def _save_img(self, im):
        def result(name=DEFAULT_IMAGE_NAME,  img_format=DEFAULT_IMAGE_FORMAT):
            im.save(DEFAULT_SAVE_PATH+name,  img_format)
        return result
