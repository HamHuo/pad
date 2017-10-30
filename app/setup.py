import sys

from models import create_tables, Tag, Point, PointTag

if sys.argv[1] == 'init':
    create_tables()
    for tag in ['mp-rush', '1E金币龙王', '潜觉扩张', '稀有素材rush',
                '三代雷达龙(光)', '三代雷达龙(暗)', '三代雷达龙(水)', '三代雷达龙(火)', '三代雷达龙(木)',
                '297光玻璃', '彩喇叭', '圣诞龙(不区分颜色)']:
        Tag.create(tag=tag)

if sys.argv[1] == 'clear':
    Point.delete().execute()
    PointTag.delete().execute()
