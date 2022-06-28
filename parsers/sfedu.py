from parsers import manager, ParserBase
import requests
from lxml import html
@manager.register(
    name='SfeduParser',
    id=ParserBase.get_university_id('sfedu'),
    dirs=['10.05.03', '10.05.05', '10.05.02', '10.03.01']
)
class SfeduParser(ParserBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = requests.Session()
    def exec(self) -> None:
        super().exec()
        self.parse('https://sfedu.ru/php_j/abitur/show.php?finance=b&list=TGKT10.05.036500OSS', '10.05.03')
        self.parse('https://sfedu.ru/php_j/abitur/show.php?finance=b&list=TGKT10.05.056500OSS', '10.05.05')
        self.parse('https://sfedu.ru/php_j/abitur/show.php?finance=b&list=TGKT10.05.026500OSS', '10.05.02')
        self.parse('https://sfedu.ru/php_j/abitur/show.php?finance=b&list=TGKT10.03.016200OSS', '10.03.01')
        super().after_exec()
    def parse(self, link: str, code: str) -> None:
        page = self.session.get(link).content
        tree = html.fromstring(page)
        study_id = self.get_direction_id(code)
        if study_id == -1:
            raise ValueError('Invalid StudyDirection')
        tr_list = tree.xpath('.//tr')
        for i in tr_list:
            children = i.getchildren()
            if len(children) >= 5:
                if self.validate_number(children[1].text):
                    print(str(children[1].text), study_id)
                    self.add_people(
                        ins_number=str(children[1].text),
                        study_id=study_id,
                        link=link,
                        agreed=not children[4].text is None
                    )
manager.run(SfeduParser)
