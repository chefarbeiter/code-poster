import code
import config
import svgwrite
import util
from itertools import groupby
from optparse import OptionParser
from log import _log


def create(input_image, output_path):
    """Create an SVG from the input image."""
    _log.debug("create: input_image: {0}, output_path: {1}".format(input_image, output_path))
    conf = config.get()
    im = util.get_image(input_image)
    (width, height) = im.size
    pix = im.load()

    dwg = svgwrite.Drawing(output_path,
                           profile='full',
                           width=width,

                           height=height,
                           viewBox='0 0 {0} {1}'.format(width * conf['svg']['ratio'], height),
                           style='font-family:\'{0}\';font-weight:900;font-size:{1}'.format(conf['svg']['font_family'], conf['svg']['font_size']))
    dwg.attribs['xml:space'] = 'preserve'

    for h in range(0, height):
        _log.debug("create: Processing line h: {0} w: {1}".format(h, width))
        colors = []
        for w in range(0, width):
            try:
                colors.append(util.to_hex(pix[w, h]))
            except:
                colors.append('#FFFFFF')
                pass
        colors = [(len(list(g)), k) for k, g in groupby(colors)]
        x = 0
        for c in colors:
            t = ''
            for l in range(0, c[0]):
                t = t + code.get_char()
            text = dwg.text(t, fill='{0}'.format(c[1]))
            text.attribs['y'] = str(h)
            text.attribs['x'] = x * conf['svg']['ratio']
            dwg.add(text)
            x = x + len(t)
    dwg.save()


if __name__ == '__main__':
    parser = OptionParser(usage='usage: %prog -i <PATH TO INPUT FILE> -o <PATH TO OUTPUT FILE>')
    parser.add_option('-i', '--input',
                      help='The path to the input image file',)
    parser.add_option('-o', '--output',
                      help='The path to save the svg output file')

    (options, args) = parser.parse_args()
    if not options.input or not options.output:
        parser.error('Please provide both input and output parameters. ')

    create(options.input, options.output)
