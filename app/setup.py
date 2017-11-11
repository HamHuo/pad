import sys

from models import create_tables, Tag, Point, PointTag, LogPoint

if sys.argv[1] == 'init':
    create_tables()
    for tag in ['mp-rush', '1E金币龙王', '潜觉扩张', '稀有素材rush',
                '三代雷达龙(光)', '三代雷达龙(暗)', '三代雷达龙(水)', '三代雷达龙(火)', '三代雷达龙(木)',
                '297光玻璃', '彩喇叭', '圣诞龙(不区分颜色)', '地狱级npc']:
        Tag.create(tag=tag)

if sys.argv[1] == 'clear':
    Point.delete().execute()
if sys.argv[1] == 'upgrade':
    LogPoint.create_table()

elif sys.argv[1] == 'clear_question_mark':
    tags_all = {x.tag for x in Tag.select().execute()}
    tags_all.remove('地狱级npc')
    print(tags_all)
    tags = [x.id for x in Tag.select(Tag.tag.in_(list(tags_all)))]
    print(tags)
    PointTag.delete().where(PointTag.tag.in_(tags)).execute()
    all_tag = [x.id for x in Tag.select().execute()]
    Point.delete().where(Point.id.not_in(all_tag)).execute()

elif sys.argv[1] == 'add':
    if sys.argv[2] == 'tag':
        Tag.create(sys.argv[3])

elif sys.argv[1] == 'delete':
    if sys.argv[2] == 'tag':
        t = Tag.get(sys.argv[3])
        t.delete()
    if sys.argv[2] == 'point':
        p = Point.get(longitude=sys.argv[3], latitude=sys.argv[4])
        p.delete_instance()
