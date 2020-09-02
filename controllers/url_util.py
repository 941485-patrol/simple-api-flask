from flask import (url_for,request)
def url_util(query, url):
    utilObj = {
            'home': url_for(url),
            'this': request.full_path,
            'next_page': url_for(url, page=query.next_num, sort=request.args.get('sort', None), search=request.args.get('search', None)) if query.has_next else None,
            'prev_page': url_for(url, page=query.prev_num, sort=request.args.get('sort', None), search=request.args.get('search', None)) if query.has_prev else None,
            'total_pages': query.pages,
            'total_items': query.total,
            'items_this_page':len(query.items),
        }
    return utilObj