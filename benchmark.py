import json
import functime

from tp_html import *

def test():
    template = TemplateParser(template_file='samples/basic_template.min.html')
    # template.save_template('samples/basic_template.min.html')
    parser = WebPageParser(template=template)
    data = parser.parse(page_file=r'samples/basic_sample.html')
    print(json.dumps(data, ensure_ascii=False))

    template = TemplateParser(template_file='samples/complex_template.html')
    # template.save_template('samples/basic_template.min.html')
    parser = WebPageParser(template=template)
    data = parser.parse(page_file=r'samples/complex_sample.html')
    print(json.dumps(data, ensure_ascii=False))

    template = TemplateParser(template_file='samples/pixiv_user_template.html')
    # template.save_template('samples/basic_template.min.html')
    parser = WebPageParser(template=template)
    data = parser.parse(page_file=r'samples/pixiv_user.html')
    print(json.dumps(data, ensure_ascii=False))

def benchmark():
    parser = WebPageParser(template_file='samples/basic_template.html')
    functime.func_time(TemplateParser, template_file='samples/basic_template.html')
    functime.func_time(parser.parse, page_file=r'samples/basic_sample.html')

    parser = WebPageParser(template_file='samples/complex_template.html')
    functime.func_time(TemplateParser, template_file='samples/complex_template.html')
    functime.func_time(parser.parse, page_file=r'samples/complex_sample.html')

    parser = WebPageParser(template_file='samples/pixiv_user_template.html')
    functime.func_time(TemplateParser, template_file='samples/pixiv_user_template.html')
    functime.func_time(parser.parse, page_file=r'samples/pixiv_user.html')

    parser = WebPageParser(template_file='samples/pixiv_user_template.min.html')
    functime.func_time(TemplateParser, template_file='samples/pixiv_user_template.min.html')
    functime.func_time(parser.parse, page_file=r'samples/pixiv_user.html')

if __name__ == '__main__':
    benchmark()
