import json
from html.parser import HTMLParser
import logging

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

class PNode(object):
    def __init__(self, tag, _class=None, id=None, is_data=False, data_type=None, data_items=None, data_names=None,
                 data_defaults=None):
        self.tag = tag
        self._class = _class
        self.id = id
        self.selector = self._get_selector()
        self.is_data = is_data
        self.data_type = data_type
        self.data_items = data_items
        self.data_names = data_names
        self.data_defaults = data_defaults
        self.children = []

    def _get_selector(self):
        id = ('#' + self.id) if self.id else ''
        cls = ('.' + '.'.join([item for item in self._class.split(' ') if item])) if self._class else ''
        return self.tag + id + cls

    def is_data_node(self):
        return self.is_data

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def append_children(self, children):
        self.children.extend(children)

    def __str__(self):
        return '{}, data_node:{}, data_type:{}'.format(self.selector, self.is_data, self.data_type)

    def __repr__(self):
        return self.__str__()


class PTree(object):
    def __init__(self, root=None):
        self.root = root

    def pre_travel(self, root=None, action=print, *args, **kwargs):
        if not root:
            root = self.root
        if not root:
            return
        action(root, *args, **kwargs)
        for child in root.children:
            self.pre_travel(child, action=action, *args, **kwargs)


class TemplateParser(HTMLParser):
    ignore_tags = ['area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input',
                   'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']

    def __init__(self, template_file=None, template_text=None, encoding='utf-8'):
        HTMLParser.__init__(self)
        self._stack = []
        self.tree = None
        self.root = None
        self.template_file = template_file
        self.template_text = template_text
        self.encoding = encoding
        self.parser_tree()
        self.remove_non_data()
        self.minimize_tree()

    def parser_tree(self):
        if self.template_file:
            f = open(self.template_file, 'r', encoding=self.encoding)
            self.template_text = f.read()
            f.close()
        if self.template_text:
            self.feed(self.template_text)
            self.tree = PTree(root=self.root)
        return self.tree

    def handle_starttag(self, tag, attrs):
        node = self._make_node(attrs, tag)
        if self._stack:
            self._stack[-1].add_child(node)
        if not self.root:
            self.root = node
        if tag not in self.ignore_tags:
            self._stack.append(node)

    def _make_node(self, attrs, tag):
        attrs_dict = dict(attrs)
        id = attrs_dict.get('id', None)
        cls = attrs_dict.get('class', None)
        is_data = True if attrs_dict.get('p-value', None) == 'true' else False
        data_type = attrs_dict.get('p-type', None)
        data_items = attrs_dict.get('p-item', '')
        data_items = data_items.split(' ') if data_items else []
        data_names = attrs_dict.get('p-name', '')
        data_names = data_names.split(' ') if data_names else []
        data_defaults = attrs_dict.get('p-default', '')
        data_defaults = data_defaults.split(' ') if data_defaults else []
        node = PNode(tag, _class=cls, id=id, is_data=is_data, data_type=data_type, data_items=data_items,
                     data_names=data_names,
                     data_defaults=data_defaults)
        return node

    def handle_endtag(self, tag):
        if tag in self.ignore_tags:
            return
        if self._stack:
            if self._stack[-1].tag == tag:
                self._stack.pop()
            else:
                has_start = False
                for node in self._stack[-6:-1]:
                    if node.tag == tag:
                        has_start = True
                        break
                if has_start:
                    top_tag = self._stack.pop().tag
                    while top_tag != tag and self._stack:
                        logger.warning('invalid start tag <{}> above line {}'.format(top_tag, self.getpos()[0]))
                        top_tag = self._stack.pop().tag
                else:
                    logger.warning('invalid end tag <{}> on line {}'.format(tag, self.getpos()[0]))
        else:
            logger.warning('invalid end tag <{}> on line {}'.format(tag, self.getpos()[0]))

    def remove_non_data(self):
        self._remove_non_data(self.root)

    def _remove_non_data(self, root=None):
        if not root:
            return False
        is_data = root.is_data
        for child in list(root.children):
            if self._remove_non_data(child):
                is_data = True
            else:
                root.remove_child(child)
        return is_data

    def minimize_tree(self):
        self._minimize_tree(self.root)

    def _minimize_tree(self, root=None):
        if not root:
            return
        while len(root.children) == 1 and not root.is_data:
            self.merge_with_child(root)
        for child in root.children:
            self._minimize_tree(child)

    def merge_with_child(self, root:PNode):
        child = root.children[0]
        root.selector += ' > ' + child.selector
        root.children = child.children
        root.tag = child.tag
        root.id = child.id
        root._class = child._class
        root.is_data = child.is_data
        root.data_defaults = child.data_defaults
        root.data_names = child.data_names
        root.data_items = child.data_items
        root.data_type = child.data_type

    # def dict_structure(self):


class WebPageParser(object):
    def __init__(self, template=None, template_file=None, template_text=None):
        self.template = template or TemplateParser(template_file=template_file, template_text=template_text)

    def parser(self, page_url=None, page_file=None, page_text=None, encoding='utf-8'):
        if page_url:
            page_text = requests.get(page_url).text
        elif page_file:
            with open(page_file, 'r', encoding=encoding) as f:
                page_text = f.read()
        elif page_text:
            pass
        else:
            return
        soup = BeautifulSoup(page_text, 'html.parser')
        data = self._parser(soup, self.template.root)
        return data

    def _get_select(self, soup, node:PNode):
        selector = node.selector
        select = soup.select(selector)
        if select:
            if len(select) > 1:
                logger.warning('more than one data block matched for <{}>, use the first one'.format(node))
            return select[0]
        else:
            logger.warning('data not found from <{}>'.format(node))
            return None


    def _parser(self, soup, node:PNode):
        data = None
        if node.is_data:
            if node.data_type == 'list':
                data = self._parser_list(soup, node)
            elif node.data_type == 'dict':
                data = self._parser_dict(soup, node)
            else:
                data = self._parser_data(soup, node)
        else:
            data = dict()
            for child_node in node.children:
                child_soup = self._get_select(soup, child_node)
                if child_soup:
                    data.update(self._parser(child_soup, child_node))
        return data

    def _parser_list(self, soup, node):
        data = []
        if len(node.children) != 1:
            logger.warning('invalid template format under node <{}>, require and need just one child'.format(node))
            return data
        child_node = node.children[0]
        selector = child_node.selector
        item_soups = soup.select(selector)
        for item in item_soups:
            data.append(self._parser(item, child_node))
        if node.data_names:
            return {node.data_names[0]: data}
        else:
            return data

    def _parser_dict(self, soup, node):
        data = dict()
        for child_node in node.children:
            child_soup = self._get_select(soup, child_node)
            if child_soup:
                data.update(self._parser(child_soup, child_node))
        if node.data_names:
            return {node.data_names[0]: data}
        else:
            return data

    def _parser_data(self, soup, node):
        data = None
        if node.data_names:
            data = dict()
            if len(node.data_items) == len(node.data_names):
                for i, name in enumerate(node.data_names):
                    item = node.data_items[i]
                    value = self._parser_item(soup, item)
                    data[name] = value
            elif len(node.data_items) == 0:
                data[node.data_names[0]] = self._parser_item(soup, 'string')
            else:
                logger.warning('invalid template format on node <{}>'.format(node))
            for child_node in node.children:
                child_soup = self._get_select(soup, child_node)
                child_data = self._parser(child_soup, child_node)
                if not isinstance(child_data, dict):
                    logger.warning('invalid template node <{}>'.format(child_node))
                else:
                    data.update(child_data)
        else:
            if node.data_items:
                data = self._parser_item(soup, node.data_items[0])
            else:
                data = self._parser_item(soup, 'string')
        return data

    def _parser_item(self, soup, item):
        if item == 'string':
            return soup.string
        else:
            return soup.attrs.get(item, None)


if __name__ == '__main__':
    parser = WebPageParser(template_file='samples/basic_template.html')
    data = parser.parser(page_file='samples/basic_sample.html')
    print(json.dumps(data, ensure_ascii=False))
    parser = WebPageParser(template_file='samples/complex_template.html')
    data = parser.parser(page_file='samples/complex_sample.html')
    print(json.dumps(data, ensure_ascii=False))
