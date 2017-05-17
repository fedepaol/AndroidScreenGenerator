import argparse
import svgwrite
import json
import os 

class ScreenshotGenerator:
    def __init__(self, args):
        self._args = args

    def generate_screen(self,
                        path,
                        screenshot_file,
                        language,
                        message):

        base=os.path.basename(screenshot_file)
        title = os.path.splitext(base)[0]
        dest = title + '.png'
        png_filename = os.path.join(path, dest)
        print png_filename
        svg_document = svgwrite.Drawing(filename = 'temp.svg',
                                            size = ("1080px", "1920px"))

        #Background
        svg_document.add(svg_document.rect(insert = (0, 0),
                                           size = ("1080px", "1920px"),
                                           stroke_width = "0",
                                           stroke = "black",
                                           fill = self._background_color))

        #note: x value is the same as inkscape svg.
        # y value is doc height - pic height - pic y inside inkscape editor
        svg_document.add(svg_document.image(insert = (338.64, 511),
                                        size = (669, 1368),
                                        href = "phonemock.png"))

        print screenshot_file
        svg_document.add(svg_document.image(insert = (368.28, 639.78),
                                        size = (612, 1088),
                                        href = screenshot_file))

        mytext = svgwrite.text.Text('', insert = (120, 220),
                                           style = "font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:40px;line-height:125%;font-family:Roboto;-inkscape-font-specification:Roboto;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1")
                                           

        myspan = svgwrite.text.TSpan(message,
                                           insert = (120, 220),
                                           style = "font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:80px;font-family:Roboto;-inkscape-font-specification:Roboto;fill:#ffffff;fill-opacity:1")
                                           
        mytext.add(myspan)
        svg_document.add(mytext)
        svg_document.save()
        ink_command = 'inkscape --export-area-page --export-png ' + png_filename +' temp.svg'
        print ink_command
        os.popen(ink_command)



    def generate_for_language(self,
                              language,
                              screenshots):
        path = os.path.join(self._args.output_folder, language)
        if not os.path.exists(path):
            os.makedirs(path)

        for screenshot in screenshots:
            filename = os.path.join(self._input_folder, language, screenshot['file'])

            if not os.path.exists(filename):
                print 'Screenshot file not found %s' % filename
                continue

            self.generate_screen(
                            path,
                            filename,
                            language,
                            screenshot['text'])

    def generate_input_tree(self):
        if not os.path.exists(self._input_folder):
            os.makedirs(self._input_folder)

        for l in self._languages:
            subpath = os.path.join(self._input_folder, l)
            if not os.path.exists(subpath):
                os.makedirs(subpath)



    def generate(self):
        if self._args.json_filename == None:
            print 'input file needed, exiting'
            return

        if not os.path.exists(self._args.json_filename):
            print '%s file not found, exiting' % self._args.json_filename
            return

        json_data = open(args.json_filename)
        self._data = json.load(json_data)
        self._languages = self._data['languages']
        self._background_color = self._data['background']
        self._input_folder = self._args.input_folder

        if self._args.generate_tree:
            self.generate_tree(data)
            return

        if not os.path.exists('output'):
            os.makedirs('output')

        for l in self._languages:
            self.generate_for_language(l, self._data['screenshots'])



def read_arguments():
    parser = argparse.ArgumentParser(description='This script expects the svg to be expressend in android dp. \
                    This means that the resolution given in the drawing will be used for mdpi resolution and scaled to \
                            generate the other resolutions')
    parser.add_argument('-I','--input_folder', dest='input_folder', help='path to input folder')
    parser.add_argument('-O','--output_folder', dest='output_folder', help='path to input folder')
    parser.add_argument('-g','--generate_input_tree', dest='generate_tree', action='store_true', help='generates_input tree')
    parser.add_argument('-f','--filename', dest='json_filename', help='the json describing the app')
    parser.set_defaults(generate_tree=False)
    args = parser.parse_args()
    return args

args = read_arguments()
generator = ScreenshotGenerator(args)
generator.generate()


