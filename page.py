class Page:
    def __init__(self, **kwargs):
        if 'url' in kwargs:
            self.url = kwargs['url']
        if 'link' in kwargs:
            self.link = kwargs['link']
        if 'title' in kwargs:
            self.title = kwargs['title']
        if 'description' in kwargs:
            self.description = kwargs['description']
        if 'status_code' in kwargs:
            self.status_code = kwargs['status_code']
        # else:
        #     self.status_code = 0
        if 'retry' in kwargs:
            self.retry = kwargs['retry']
        else:
            self.retry = 0
        if 'id' in kwargs:
            self.id = kwargs['id']




if __name__ == '__main__':
    a = {'url': 123, 'link': 'www.qwe.ru', 'status': 0}

    p = Page(**a)
    print(p.url)
    p.status = 1
    print(p.status)

