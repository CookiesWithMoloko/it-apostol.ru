from parsers import manager, ParserBase
import requests
from lxml import html
@manager.register(
    name='VsuetParser',
    id=ParserBase.get_university_id('vsuet'),
    dirs=['10.05.03']
)
class VsuetParser(ParserBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = requests.Session()
    def exec(self) -> None:
        super().exec()
        # 10.05.03
        r = self.session.post(
            "http://priem.vsuet.ru/query.php",
            data={
                "query": "getCatals",
                "type_id": 1,
                "kind_id": 2,
                "category_id": 4,
                "spec_id": 2,
                "namefile": "Doc-admis.php"
            }
        )
        study_id = self.get_direction_id("10.05.03")
        tree = html.fromstring(r.json()[0]['catalog'])
        a = tree.xpath('.//tr')
        for element in a:
            ch = element.getchildren()
            if len(ch) >= 2:
                if self.validate_number(str(ch[1].text)):
                    self.add_people(
                        ins_number=str(ch[1].text),
                        study_id=study_id,
                        link="http://priem.vsuet.ru/Doc-admis.php",
                        agreed=not ch[8].text is None
                    )
manager.run(VsuetParser)
