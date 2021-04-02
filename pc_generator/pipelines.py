# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy.orm import sessionmaker

from pc_generator.models import db_connect, create_table, PcPart


class PcPartsPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        pc_part = PcPart()
        pc_part.name = item["name"]
        pc_part.price = item["price"]
        pc_part.href = item["href"]
        pc_part.img = item["img"]

        # exist_part = session.query(Author).filter_by(name = author.name).first()
        # if exist_author is not None:
        #     quote.author = exist_author
        # else:
        #     quote.author = author
        #
        # if "tags" in item:
        #     for tag_name in item["tags"]:
        #         tag = Tag(name=tag_name)
        #         exist_tag = session.query(Tag).filter_by(name=tag.name).first()
        #         if exist_tag is not None:
        #             tag = exist_tag
        #         quote.tags.append(tag)

        try:
            session.add(pc_part)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item


class SaveQuotesPipeline(object):
    pass
    # def __init__(self):
    #     engine = db_connect()
    #     create_table(engine)
    #     self.Session = sessionmaker(bind=engine)
    #
    # def process_item(self, item, spider):
    #     session = self.Session()
    #     quote = Quote()
    #     author = Author()
    #     tag = Tag()
    #     author.name = item["author_name"]
    #     author.birthday = item["author_birthday"]
    #     author.bornlocation = item["author_born_location"]
    #     author.bio = item["author_bio"]
    #     quote.quote_content = item["quote_content"]
    #
    #     exist_author = session.query(Author).filter_by(name = author.name).first()
    #     if exist_author is not None:
    #         quote.author = exist_author
    #     else:
    #         quote.author = author
    #
    #     if "tags" in item:
    #         for tag_name in item["tags"]:
    #             tag = Tag(name=tag_name)
    #             exist_tag = session.query(Tag).filter_by(name=tag.name).first()
    #             if exist_tag is not None:
    #                 tag = exist_tag
    #             quote.tags.append(tag)
    #
    #     try:
    #         session.add(quote)
    #         session.commit()
    #     except:
    #         session.rollback()
    #         raise
    #     finally:
    #         session.close()
    #
    #     return item


class DuplicatesPipeline(object):
    pass
    # def __init__(self):
    #     """
    #     Initializes database connection and sessionmaker.
    #     Creates tables.
    #     """
    #     engine = db_connect()
    #     create_table(engine)
    #     self.Session = sessionmaker(bind=engine)
    #     logging.info("****DuplicatesPipeline: database connected****")
    #
    # def process_item(self, item, spider):
    #     session = self.Session()
    #     exist_quote = session.query(Quote).filter_by(quote_content=item["quote_content"]).first()
    #     if exist_quote is not None:  # the current quote exists
    #         raise DropItem("Duplicate item found: %s" % item["quote_content"])
    #         session.close()
    #     else:
    #         return item
    #         session.close()