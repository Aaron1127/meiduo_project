

def get_breadcrumb(category):
    """
    查詢麵包屑導航
    :param category: 分類級數: 1, 2, 3級
    :return: 1級返回1級, 2級返回1, 2級, 3級返回1, 2, 3級
    """

    breadcrumb = {
        'cat1': '',
        'cat2': '',
        'cat3': '',
    }

    if category.parent is None:  # 1級
        breadcrumb['cat1'] = category

    elif category.subs.count() == 0:  # 3級
        cat2 = category.parent
        breadcrumb['cat1'] = cat2.parent
        breadcrumb['cat2'] = cat2
        breadcrumb['cat3'] = category

    else:  # 2級
        breadcrumb['cat1'] = category.parent
        breadcrumb['cat2'] = category

    return breadcrumb



