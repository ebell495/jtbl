import unittest
import textwrap
import jtbl.cli


class MyTests(unittest.TestCase):

    def setUp(self):
        self.SUCCESS, self.ERROR = True, False
        self.columns = 80

    def test_simple_key_value(self):
        stdin = [{"key": "value"}]
        expected = textwrap.dedent('''\
        key
        -----
        value''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=self.columns), (self.SUCCESS, expected))

    def test_multi_key_value(self):
        stdin = [{"key1": "value1", "key2": "value1"}, {"key1": "value2", "key2": "value2"}]
        expected = textwrap.dedent('''\
        key1    key2
        ------  ------
        value1  value1
        value2  value2''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=self.columns), (self.SUCCESS, expected))

    def test_null_string(self):
        stdin = [None]
        expected = textwrap.dedent('''\
        jtbl:  Cannot represent this part of the JSON Object as a table.
               (Could be an Element, an Array, or Null data instead of an Object):
               [null]
        ''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=self.columns), (self.ERROR, expected))

    def test_array_input(self):
        stdin = ["value1", "value2", "value3"]
        expected = textwrap.dedent('''\
        jtbl:  Cannot represent this part of the JSON Object as a table.
               (Could be an Element, an Array, or Null data instead of an Object):
               ["value1", "value2", "value3"]
        ''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=self.columns), (self.ERROR, expected))

    def test_deep_nest(self):
        stdin = [{"this":{"is":{"a":{"deeply":{"nested":{"structure":"value1","item2":"value2"}}}}}}]
        expected = textwrap.dedent('''\
        this
        ---------------------------------------------------------------------------------
        {'is': {'a': {'deeply': {'nested': {'structure': 'value1', 'item2': 'value2'}}}}}''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=100), (self.SUCCESS, expected))

    def test_jc_dig(self):
        stdin = [{"id": 55658, "opcode": "QUERY", "status": "NOERROR", "flags": ["qr", "rd", "ra"], "query_num": 1, "answer_num": 5, "authority_num": 0, "additional_num": 1, "question": {"name": "www.cnn.com.", "class": "IN", "type": "A"}, "answer": [{"name": "www.cnn.com.", "class": "IN", "type": "CNAME", "ttl": 147, "data": "turner-tls.map.fastly.net."}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.1.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.65.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.129.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.193.67"}], "query_time": 44, "server": "2600", "when": "Wed Mar 18 12:20:59 PDT 2020", "rcvd": 143}]
        expected = textwrap.dedent('''\
        ╒══════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╕
        │ id   │ opco   │ stat   │ flag   │   quer │   answ │   auth │   addi │ ques   │ answ   │   quer │   serv │ when   │   rcvd │
        │      │ de     │ us     │ s      │   y_nu │   er_n │   orit │   tion │ tion   │ er     │   y_ti │     er │        │        │
        │      │        │        │        │      m │     um │   y_nu │   al_n │        │        │     me │        │        │        │
        │      │        │        │        │        │        │      m │     um │        │        │        │        │        │        │
        ╞══════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╡
        │ 5565 │ QUER   │ NOER   │ ['qr   │      1 │      5 │      0 │      1 │ {'na   │ [{'n   │     44 │   2600 │ Wed    │    143 │
        │ 8    │ Y      │ ROR    │ ', '   │        │        │        │        │ me':   │ ame'   │        │        │ Mar    │        │
        │      │        │        │ rd',   │        │        │        │        │  'ww   │ : 'w   │        │        │ 18 1   │        │
        │      │        │        │  'ra   │        │        │        │        │ w.cn   │ ww.c   │        │        │ 2:20   │        │
        │      │        │        │ ']     │        │        │        │        │ n.co   │ nn.c   │        │        │ :59    │        │
        │      │        │        │        │        │        │        │        │ m.',   │ om.'   │        │        │ PDT    │        │
        │      │        │        │        │        │        │        │        │  'cl   │ , 'c   │        │        │ 2020   │        │
        │      │        │        │        │        │        │        │        │ ass'   │ lass   │        │        │        │        │
        │      │        │        │        │        │        │        │        │ : 'I   │ ': '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │ N',    │ IN',   │        │        │        │        │
        │      │        │        │        │        │        │        │        │ 'typ   │  'ty   │        │        │        │        │
        │      │        │        │        │        │        │        │        │ e':    │ pe':   │        │        │        │        │
        │      │        │        │        │        │        │        │        │ 'A'}   │  'CN   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ AME'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ , 't   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ tl':   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  147   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ , 'd   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ata'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ : 't   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ urne   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ r-tl   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ s.ma   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ p.fa   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ stly   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ .net   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ .'},   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  {'n   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ame'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ : 't   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ urne   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ r-tl   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ s.ma   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ p.fa   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ stly   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ .net   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ .',    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'cla   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ss':   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  'IN   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ', '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ type   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ': '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ A',    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'ttl   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ': 5   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ , 'd   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ata'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ : '1   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 51.1   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 01.1   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ .67'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ }, {   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'nam   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ e':    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'tur   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ner-   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ tls.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ map.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ fast   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ly.n   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ et.'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ , 'c   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ lass   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ': '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ IN',   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  'ty   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ pe':   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  'A'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ , 't   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ tl':   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  5,    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'dat   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ a':    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ '151   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ .101   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ .65.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 67'}   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ , {'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ name   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ': '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ turn   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ er-t   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ls.m   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ap.f   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ astl   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ y.ne   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ t.',   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  'cl   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ass'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ : 'I   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ N',    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'typ   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ e':    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'A',   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  'tt   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ l':    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 5, '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ data   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ': '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 151.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 101.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 129.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 67'}   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ , {'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ name   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ': '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ turn   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ er-t   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ls.m   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ap.f   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ astl   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ y.ne   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ t.',   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  'cl   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ass'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ : 'I   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ N',    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'typ   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ e':    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'A',   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  'tt   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ l':    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 5, '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ data   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ': '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 151.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 101.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 193.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 67'}   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ]      │        │        │        │        │
        ╘══════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╛''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=80), (self.SUCCESS, expected))

    def test_jc_dig_150cols(self):
        stdin = [{"id": 55658, "opcode": "QUERY", "status": "NOERROR", "flags": ["qr", "rd", "ra"], "query_num": 1, "answer_num": 5, "authority_num": 0, "additional_num": 1, "question": {"name": "www.cnn.com.", "class": "IN", "type": "A"}, "answer": [{"name": "www.cnn.com.", "class": "IN", "type": "CNAME", "ttl": 147, "data": "turner-tls.map.fastly.net."}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.1.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.65.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.129.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.193.67"}], "query_time": 44, "server": "2600", "when": "Wed Mar 18 12:20:59 PDT 2020", "rcvd": 143}]
        expected = textwrap.dedent('''\
        ╒══════════╤══════════╤═══════╤══════════╤═════════╤══════════╤══════════╤══════════╤══════════╤══════════╤══════════╤══════════╤════════╤════════╕
        │ opcode   │   server │    id │ status   │ flags   │   query_ │   answer │   author │   additi │ questi   │ answer   │   query_ │ when   │   rcvd │
        │          │          │       │          │         │      num │     _num │   ity_nu │   onal_n │ on       │          │     time │        │        │
        │          │          │       │          │         │          │          │        m │       um │          │          │          │        │        │
        ╞══════════╪══════════╪═══════╪══════════╪═════════╪══════════╪══════════╪══════════╪══════════╪══════════╪══════════╪══════════╪════════╪════════╡
        │ QUERY    │     2600 │ 55658 │ NOERRO   │ ['qr',  │        1 │        5 │        0 │        1 │ {'name   │ [{'nam   │       44 │ Wed Ma │    143 │
        │          │          │       │ R        │  'rd',  │          │          │          │          │ ': 'ww   │ e': 'w   │          │ r 18 1 │        │
        │          │          │       │          │  'ra']  │          │          │          │          │ w.cnn.   │ ww.cnn   │          │ 2:20:5 │        │
        │          │          │       │          │         │          │          │          │          │ com.',   │ .com.'   │          │ 9 PDT  │        │
        │          │          │       │          │         │          │          │          │          │  'clas   │ , 'cla   │          │ 2020   │        │
        │          │          │       │          │         │          │          │          │          │ s': 'I   │ ss': '   │          │        │        │
        │          │          │       │          │         │          │          │          │          │ N', 't   │ IN', '   │          │        │        │
        │          │          │       │          │         │          │          │          │          │ ype':    │ type':   │          │        │        │
        │          │          │       │          │         │          │          │          │          │ 'A'}     │  'CNAM   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ E', 't   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ tl': 1   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ 47, 'd   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ ata':    │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ 'turne   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ r-tls.   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ map.fa   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ stly.n   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ et.'},   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │  {'nam   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ e': 't   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ urner-   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ tls.ma   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ p.fast   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ ly.net   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ .', 'c   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ lass':   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │  'IN',   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │  'type   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ ': 'A'   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ , 'ttl   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ ': 5,    │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ 'data'   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ : '151   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ .101.1   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ .67'},   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │  {'nam   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ e': 't   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ urner-   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ tls.ma   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ p.fast   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ ly.net   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ .', 'c   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ lass':   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │  'IN',   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │  'type   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ ': 'A'   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ , 'ttl   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ ': 5,    │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ 'data'   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ : '151   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ .101.6   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ 5.67'}   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ , {'na   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ me': '   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ turner   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ -tls.m   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ ap.fas   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ tly.ne   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ t.', '   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ class'   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ : 'IN'   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ , 'typ   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ e': 'A   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ ', 'tt   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ l': 5,   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │  'data   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ ': '15   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ 1.101.   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ 129.67   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ '}, {'   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ name':   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │  'turn   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ er-tls   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ .map.f   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ astly.   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ net.',   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │  'clas   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ s': 'I   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ N', 't   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ ype':    │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ 'A', '   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ ttl':    │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ 5, 'da   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ ta': '   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ 151.10   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ 1.193.   │          │        │        │
        │          │          │       │          │         │          │          │          │          │          │ 67'}]    │          │        │        │
        ╘══════════╧══════════╧═══════╧══════════╧═════════╧══════════╧══════════╧══════════╧══════════╧══════════╧══════════╧══════════╧════════╧════════╛''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=150), (self.SUCCESS, expected))

    def test_jc_dig_150cols_t(self):
        stdin = [{"id": 55658, "opcode": "QUERY", "status": "NOERROR", "flags": ["qr", "rd", "ra"], "query_num": 1, "answer_num": 5, "authority_num": 0, "additional_num": 1, "question": {"name": "www.cnn.com.", "class": "IN", "type": "A"}, "answer": [{"name": "www.cnn.com.", "class": "IN", "type": "CNAME", "ttl": 147, "data": "turner-tls.map.fastly.net."}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.1.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.65.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.129.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.193.67"}], "query_time": 44, "server": "2600", "when": "Wed Mar 18 12:20:59 PDT 2020", "rcvd": 143}]
        expected = textwrap.dedent('''\
        opcode    status      server     id  flags       query_nu    answer_n    authorit    addition  question    answer      query_ti  when       rcvd
        --------  --------  --------  -----  --------  ----------  ----------  ----------  ----------  ----------  --------  ----------  -------  ------
        QUERY     NOERROR       2600  55658  ['qr', '           1           5           0           1  {'name':    [{'name'          44  Wed Mar     143''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, truncate=True, columns=150), (self.SUCCESS, expected))

    def test_jc_dig_nowrap(self):
        stdin = [{"id": 55658, "opcode": "QUERY", "status": "NOERROR", "flags": ["qr", "rd", "ra"], "query_num": 1, "answer_num": 5, "authority_num": 0, "additional_num": 1, "question": {"name": "www.cnn.com.", "class": "IN", "type": "A"}, "answer": [{"name": "www.cnn.com.", "class": "IN", "type": "CNAME", "ttl": 147, "data": "turner-tls.map.fastly.net."}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.1.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.65.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.129.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.193.67"}], "query_time": 44, "server": "2600", "when": "Wed Mar 18 12:20:59 PDT 2020", "rcvd": 143}]
        expected = textwrap.dedent('''\
           id  opcode    status    flags                 query_num    answer_num    authority_num    additional_num  question                                              answer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       query_time    server  when                            rcvd
        -----  --------  --------  ------------------  -----------  ------------  ---------------  ----------------  ----------------------------------------------------  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  ------------  --------  ----------------------------  ------
        55658  QUERY     NOERROR   ['qr', 'rd', 'ra']            1             5                0                 1  {'name': 'www.cnn.com.', 'class': 'IN', 'type': 'A'}  [{'name': 'www.cnn.com.', 'class': 'IN', 'type': 'CNAME', 'ttl': 147, 'data': 'turner-tls.map.fastly.net.'}, {'name': 'turner-tls.map.fastly.net.', 'class': 'IN', 'type': 'A', 'ttl': 5, 'data': '151.101.1.67'}, {'name': 'turner-tls.map.fastly.net.', 'class': 'IN', 'type': 'A', 'ttl': 5, 'data': '151.101.65.67'}, {'name': 'turner-tls.map.fastly.net.', 'class': 'IN', 'type': 'A', 'ttl': 5, 'data': '151.101.129.67'}, {'name': 'turner-tls.map.fastly.net.', 'class': 'IN', 'type': 'A', 'ttl': 5, 'data': '151.101.193.67'}]            44      2600  Wed Mar 18 12:20:59 PDT 2020     143''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, nowrap=True, columns=150), (self.SUCCESS, expected))

    def test_jc_dig_nowrap_t_cols_80(self):
        """test that nowrap overrides both truncate and columns"""
        stdin = [{"id": 55658, "opcode": "QUERY", "status": "NOERROR", "flags": ["qr", "rd", "ra"], "query_num": 1, "answer_num": 5, "authority_num": 0, "additional_num": 1, "question": {"name": "www.cnn.com.", "class": "IN", "type": "A"}, "answer": [{"name": "www.cnn.com.", "class": "IN", "type": "CNAME", "ttl": 147, "data": "turner-tls.map.fastly.net."}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.1.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.65.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.129.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.193.67"}], "query_time": 44, "server": "2600", "when": "Wed Mar 18 12:20:59 PDT 2020", "rcvd": 143}]
        expected = textwrap.dedent('''\
           id  opcode    status    flags                 query_num    answer_num    authority_num    additional_num  question                                              answer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       query_time    server  when                            rcvd
        -----  --------  --------  ------------------  -----------  ------------  ---------------  ----------------  ----------------------------------------------------  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  ------------  --------  ----------------------------  ------
        55658  QUERY     NOERROR   ['qr', 'rd', 'ra']            1             5                0                 1  {'name': 'www.cnn.com.', 'class': 'IN', 'type': 'A'}  [{'name': 'www.cnn.com.', 'class': 'IN', 'type': 'CNAME', 'ttl': 147, 'data': 'turner-tls.map.fastly.net.'}, {'name': 'turner-tls.map.fastly.net.', 'class': 'IN', 'type': 'A', 'ttl': 5, 'data': '151.101.1.67'}, {'name': 'turner-tls.map.fastly.net.', 'class': 'IN', 'type': 'A', 'ttl': 5, 'data': '151.101.65.67'}, {'name': 'turner-tls.map.fastly.net.', 'class': 'IN', 'type': 'A', 'ttl': 5, 'data': '151.101.129.67'}, {'name': 'turner-tls.map.fastly.net.', 'class': 'IN', 'type': 'A', 'ttl': 5, 'data': '151.101.193.67'}]            44      2600  Wed Mar 18 12:20:59 PDT 2020     143''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, nowrap=True, columns=80, truncate=True), (self.SUCCESS, expected))

    def test_jc_dig_answer(self):
        stdin = [{"name":"www.cnn.com.","class":"IN","type":"CNAME","ttl":147,"data":"turner-tls.map.fastly.net."},{"name":"turner-tls.map.fastly.net.","class":"IN","type":"A","ttl":5,"data":"151.101.1.67"},{"name":"turner-tls.map.fastly.net.","class":"IN","type":"A","ttl":5,"data":"151.101.65.67"},{"name":"turner-tls.map.fastly.net.","class":"IN","type":"A","ttl":5,"data":"151.101.129.67"},{"name":"turner-tls.map.fastly.net.","class":"IN","type":"A","ttl":5,"data":"151.101.193.67"}]
        expected = textwrap.dedent('''\
        name                        class    type      ttl  data
        --------------------------  -------  ------  -----  --------------------------
        www.cnn.com.                IN       CNAME     147  turner-tls.map.fastly.net.
        turner-tls.map.fastly.net.  IN       A           5  151.101.1.67
        turner-tls.map.fastly.net.  IN       A           5  151.101.65.67
        turner-tls.map.fastly.net.  IN       A           5  151.101.129.67
        turner-tls.map.fastly.net.  IN       A           5  151.101.193.67''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=80), (self.SUCCESS, expected))


    def test_json_lines(self):
        """test JSON Lines data"""
        stdin = [
            {"name":"lo0","type":None,"ipv4_addr":"127.0.0.1","ipv4_mask":"255.0.0.0"},
            {"name":"gif0","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"stf0","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"XHC0","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"XHC20","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"VHC128","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"XHC1","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"en5","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"ap1","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"en0","type":None,"ipv4_addr":"192.168.1.221","ipv4_mask":"255.255.255.0"},
            {"name":"p2p0","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"awdl0","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"en1","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"en2","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"en3","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"en4","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"bridge0","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"utun0","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"utun1","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"utun2","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"utun3","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"utun4","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"vmnet1","type":None,"ipv4_addr":"192.168.101.1","ipv4_mask":"255.255.255.0"},
            {"name":"vmnet8","type":None,"ipv4_addr":"192.168.71.1","ipv4_mask":"255.255.255.0"}
        ]
        expected = textwrap.dedent('''\
        name     type    ipv4_addr      ipv4_mask
        -------  ------  -------------  -------------
        lo0              127.0.0.1      255.0.0.0
        gif0
        stf0
        XHC0
        XHC20
        VHC128
        XHC1
        en5
        ap1
        en0              192.168.1.221  255.255.255.0
        p2p0
        awdl0
        en1
        en2
        en3
        en4
        bridge0
        utun0
        utun1
        utun2
        utun3
        utun4
        vmnet1           192.168.101.1  255.255.255.0
        vmnet8           192.168.71.1   255.255.255.0''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=self.columns), (self.SUCCESS, expected))

    def test_markdown(self):
        """test markdown output"""
        stdin = [
            {
                "column1": "data",
                "column2": 123,
                "column3": True,
                "column4": None
            },
            {
                "column1": "This is a long string that should not be truncated by the markdown table format. Lines should not be wrapped for markdown.",
                "column2": 123,
                "column3": True,
                "column4": None
            }
        ]

        expected = textwrap.dedent('''\
        | column1                                                                                                                    |   column2 | column3   | column4   |
        |----------------------------------------------------------------------------------------------------------------------------|-----------|-----------|-----------|
        | data                                                                                                                       |       123 | True      |           |
        | This is a long string that should not be truncated by the markdown table format. Lines should not be wrapped for markdown. |       123 | True      |           |''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=self.columns, nowrap=True, table_format='github'), (self.SUCCESS, expected))


if __name__ == '__main__':
    unittest.main()
