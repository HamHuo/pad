import sys

from models import create_tables, Tag, Point, PointTag, UserPoint

if len(sys.argv) >= 2:

    if sys.argv[1] == 'init':
        t = Tag.table_exists()
        create_tables()
        if not t:
            for tag in ['地狱级npc', '觉醒素材', 'mp-rush', '1E金币龙王', '潜觉扩张', '稀有素材rush',
                        '三代雷达龙(光)', '三代雷达龙(暗)', '三代雷达龙(水)', '三代雷达龙(火)', '三代雷达龙(木)',
                        '297光玻璃', '彩喇叭', '圣诞龙(不区分颜色)']:
                Tag.create(tag=tag)

    if sys.argv[1] == 'clear':
        Point.delete().execute()
        PointTag.delete().execute()

    elif sys.argv[1] == 'clear_mark':
        tags = {x.tag for x in Tag.select().execute()}
        tags.remove('地狱级npc')
        tags = list(tags)
        tags_id = [x for x in Tag.select().where(Tag.tag.in_(tags))]
        q = PointTag.delete().where(PointTag.tag.in_(tags_id)).execute()
        for p in Point.select(Point):
            new_tr = [x.tag.tag for x in p.pointtag]
            if not new_tr:
                p.delete_instance()
            else:
                p.treasure = ', '.join(new_tr)
                p.save()
        for p in UserPoint.select():
            p.delete_instance()

    if sys.argv[1] == 'add':
        if sys.argv[2] == 'tag':
            Tag.create(sys.argv[3])
    if sys.argv[1] == 'delete':
        if sys.argv[2] == 'tag':
            t = Tag.get(sys.argv[3])
            t.delete()
        if sys.argv[2] == 'point':
            p = Point.get(longitude=sys.argv[3], latitude=sys.argv[4])
            p.delete_instance()

else:
    t = Tag.select(Tag).execute()
    for x in t:
        [print(y.point.treasure) for y in x.pointtag]
