import pathlib
import qrcode
from django.shortcuts import redirect
import qrcode.image.svg
from core.settings import QRCODE_ROOT
from .apps import APP_NAME
from django.http import Http404,HttpResponse,HttpResponseRedirect
import os


def generate_qrcode(content,file_name,file_path=None,file_address=None,method=None):
    if file_path is None:
        file_path=QRCODE_ROOT
    if file_address is None:
        file_address=os.path.join(file_path,file_name)
    if method is None:
        method='basic'
    if method == 'basic':
        # Simple factory, just a set of rects.
        factory = qrcode.image.svg.SvgImage
    elif method == 'fragment':
        # Fragment factory (also just a set of rects)
        factory = qrcode.image.svg.SvgFragmentImage
    else:
        # Combined path factory, fixes white space that may occur when zooming
        factory = qrcode.image.svg.SvgPathImage
    if not os.path.exists(file_path):
        pathlib.Path(file_path).mkdir(parents=True,exist_ok=True)
    img = qrcode.make(data=content, image_factory=factory)
    img.save(file_address)

