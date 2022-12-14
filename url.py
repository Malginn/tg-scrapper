#coding: utf-8
from googletrans import Translator
translator = Translator()


def translate_text(data):
    for k, v in data.items():
        if type(v) == list:
            for count, i in enumerate(data[k]):
                data[k][count] = translator.translate(i, src='zh-tw', dest='ru').text
        else:
            data[k] = translator.translate(v, src='zh-tw', dest='ru').text
    return data

URL = ''

dict_ = {'name': 'Yi Z CLUB 设计感后背钉珠字母宽松纯棉牛仔夹克外套秋冬女装0.83', 'seller': 'Yi Z CLUB 高端女装 原衣庄外贸', 'price': ['194.99'], 'size': ['CHN-XS', 'CHN-S'], 'delivery': '快递 ¥10.00', 'color': '黑灰[22-10-24]', 'characteristic': ['品牌: other/其他', '尺码: CHN-XS CHN-S', '面料: 其他/other', '图案: 字母/数字/文字', '风格: 街头', '领子: 其他/other', '衣门襟: 单排扣', '颜色分类: 黑灰[22-10-24]', '袖型: 常规', '组合形式: 单件', '货号: ***', '年份季节: 2022年秋季', '袖长: 长袖', '厚薄: 常规', '衣长: 常规', '服装版型: 宽松型', '流行元素/工艺: 口袋 钉珠 纽扣', '材质成分: 棉100%'], 'image': []}
print(translate_text(dict_))
