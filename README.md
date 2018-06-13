# HTML Parser
## Introduction
This tool can help get useful data from html web page. It parses html page with the template file which marks data that you need with special attributes. The template file positions html blocks that contain data, and describes types, names and structures of data. You can modify an example page file to get it, or write a basic html structure that can position your data. I suggest you to use the first method, the tool can delete irrelevant parts and organize html tree automatically.
## How to use
```python
parser = WebPageParser(template_file='samples/basic_template.html')
parser = WebPageParser(template_text='...')
data = parser.parser(page_file='samples/basic_sample.html', encoding='urf-8')
data = parser.parser(page_url='http://.....')
data = parser.parser(page_text='.....')
```
## Template file
## string
To get data from content or attributes of element.
```html
<a href="....">link</a>
```
To get content. This will get data {'name': 'link'} 
```html
<a p-value="true" p-name="name"></a>
```
To get href. This will get data {'name': '...'}
```html
<a p-value="true" p-name="name" p-item="href"></a>
```
## list
For HTML
```html
<ul class="image-list">
    <li class="image-item"><a href="/image/1"></a></li>
    <li class="image-item"><a href="/image/2"></a></li>
    <li class="image-item"><a href="/image/3"></a></li>
    <li class="image-item"><a href="/image/4"></a></li>
</ul>
```
template:
```html
<ul class="image-list" p-value="true" p-name="images" p-type="list">
    <li class="image-item">
        <a p-value="true" p-item="href"></a>
    </li>
</ul>
```
In list template, in the element which is marked with p-type=list, require one child p-value node and just one that is for selecting item data. If list item is dict or list, structure in item is also allowed.
## dict
For HTML
```html
<div class="dict-data-container">
    <a class="user-name" href="/user/13456" title="user xxx">xxx</a>
    <p class="user-age">20</p>
    <div class="sub-div">
        <p class="user-fans-num">10</p>
        <p class="user-follow-num">20</p>
    </div>
</div>
```
template:
```html
<div class="dict-data-container" p-value="true" p-name="user_link" p-type="dict">
    <a class="user-name" p-value="true" p-name="name link title" p-item="string href title"></a>
    <p class="user-age" p-value="true" p-name="age"></p>
    <div class="sub-div">
        <p class="user-fans-num" p-value="true" p-name="fans_num"></p>
        <p class="user-follow-num" p-value="true" p-name="follow_num"></p>
    </div>
</div>
```
In dict template, p-name is required for key of dictionary. Multiple p-item is allowed, split with space, and "string" means content of element, others items are attributies name.
## complex nesting
html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<div id="container">
    <div class="column-1">
        <!--dict in list-->
        <ul class="column-1-ul">
            <li>
                <div class="dict-data-container">
                    <a class="user-name" href="/user/1" title="user xxx">xxx</a>
                    <p class="user-age">20</p>
                    <div class="sub-div">
                        <p class="user-fans-num">10</p>
                        <p class="user-follow-num">20</p>
                    </div>
                </div>
            </li>
            <li>
                <div class="dict-data-container">
                    <a class="user-name" href="/user/2" title="user yyy">yyy</a>
                    <p class="user-age">10</p>
                    <div class="sub-div">
                        <p class="user-fans-num">10</p>
                        <p class="user-follow-num">20</p>
                    </div>
                </div>
            </li>
        </ul>
    </div>
    <div class="column-2">
        <!--list in dict-->
        <div class="dict-data-container">
            <a class="user-name" href="/user/1" title="user xxx">xxx</a>
            <p class="user-age">20</p>
            <div class="sub-div">
                <p class="user-fans-num">10</p>
                <p class="user-follow-num">20</p>
            </div>
            <ul class="image-list">
                <li class="image-item"><a href="/image/1"></a></li>
                <li class="image-item"><a href="/image/2"></a></li>
                <li class="image-item"><a href="/image/3"></a></li>
                <li class="image-item"><a href="/image/4"></a></li>
            </ul>
        </div>
    </div>
    <div class="column-3">
        <!--dict in dict-->
        <div class="dict-data-container">
            <div class="profile">
                <a class="user-name" href="/user/1" title="user xxx">xxx</a>
                <p class="user-age">20</p>
            </div>
            <div class="sub-div">
                <p class="user-fans-num">10</p>
                <p class="user-follow-num">20</p>
            </div>
        </div>
    </div>
    <div class="column-4">
        <!--list in list-->
        <ul class="image-list">
            <ul class="image-tags">
                <p class="tag">tag1-1</p>
                <p class="tag">tag1-2</p>
                <p class="tag">tag1-3</p>
            </ul>
            <ul class="image-tags">
                <p class="tag">tag2-1</p>
                <p class="tag">tag2-2</p>
                <p class="tag">tag2-3</p>
            </ul>
            <ul class="image-tags">
                <p class="tag">tag3-1</p>
                <p class="tag">tag3-2</p>
                <p class="tag">tag3-3</p>
            </ul>
        </ul>
    </div>
</div>
</body>
</html>
```
template:
```html
<div id="container">
    <div class="column-1">
        <!--dict in list-->
        <ul class="column-1-ul" p-value="true" p-name="user_list" p-type="list">
            <li p-value="true" p-type="dict">
                <div class="dict-data-container">
                    <a class="user-name" p-value="true" p-name="name link title" p-item="string href title"></a>
                    <p class="user-age" p-value="true" p-name="age"></p>
                    <div class="sub-div">
                        <p class="user-fans-num" p-value="true" p-name="fans_num"></p>
                        <p class="user-follow-num" p-value="true" p-name="follow_num"></p>
                    </div>
                </div>
            </li>
        </ul>
    </div>
    <div class="column-2">
        <!--list in dict-->
        <div class="dict-data-container" p-value="true" p-name="user_all" p-type="dict">
            <a class="user-name" p-value="true" p-name="name link title" p-item="string href title"></a>
            <p class="user-age" p-value="true" p-name="age"></p>
            <div class="sub-div">
                <p class="user-fans-num" p-value="true" p-name="fans_num"></p>
                <p class="user-follow-num" p-value="true" p-name="follow_num"></p>
            </div>
            <ul class="image-list" p-value="true" p-name="images" p-type="list">
                <li class="image-item">
                    <a p-value="true" p-item="href"></a>
                </li>
            </ul>
        </div>
    </div>
    <div class="column-3">
        <!--dict in dict-->
        <div class="dict-data-container" p-value="true" p-name="user_info" p-type="dict">
            <div class="profile" p-value="true" p-name="profile" p-type="dict">
                <a class="user-name" p-value="true" p-name="name link title" p-item="string href title"></a>
                <p class="user-age" p-value="true" p-name="age"></p>
            </div>
            <div class="sub-div" p-value="true" p-name="counts" p-type="dict">
                <p class="user-fans-num" p-value="true" p-name="fans_num"></p>
                <p class="user-follow-num" p-value="true" p-name="follow_num"></p>
            </div>
        </div>
    </div>
    <div class="column-4">
        <!--list in list-->
        <ul class="image-list" p-value="true" p-name="image_tags" p-type="list">
            <ul class="image-tags" p-value="true" p-type="list">
                <p class="tag" p-value="true"></p>
            </ul>
        </ul>
    </div>
</div>
```
 
