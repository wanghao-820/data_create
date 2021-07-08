#!/usr/bin/env python
# -*- coding:UTF-8 -*-


# DESCRIPTION:


from apis import course_apis,portal_apis
from utils import db_utils, str_utils, time_utils
from collections import Counter 


spring_clazz = []


class Renewal():
    def __init__(self):
        self.db = db_utils.DBUtils(name='portal')
        self.db.dict = db_utils.DBUtils(name='portal',cursor_dict=True)
        self.db.payment = db_utils.DBUtils(name='payment')
        self.course_api = course_apis
        self.portal_api = portal_apis

    # 调整课时的时间，为了区分插班生和不是插班生,默认是非插班生
    def adject_clazz_plan_time(self, clazz_id: int, days: int=1):
        start_time = time_utils.time_format(time_utils.time_delta(days=days)) 
        stop_time = time_utils.time_format(time_utils.time_delta(days=days,minutes=30)) 
        self.db.update("update clazz_plan set start_time = '{}', stop_time = '{}'  where clazz_id = {} and status = 1 order by seq;".format(start_time,stop_time,clazz_id), commit=True)
        # # 并且废弃掉已有的小班
        self.db.update("update team set `status` = 0 WHERE clazz_id = {};".format(clazz_id), commit=True)
        # 然后新建小班并且分配班主任
        master_ids = [10706952, 10706958, 10706954, 10652874]
        # master_ids = [10706954, 10652874]
        for i in range(2):
            team_id = self.portal_api.create_team(clazz_id=clazz_id)
            # 添加班主任  tom
            self.portal_api.exchange_team_master(team_id= team_id, from_master_id= None, to_master_id= master_ids[i])

    # 退课
    def quit_clazz(self, order_ids: list):
        for order_id in order_ids:
            # order_id = order_id
            self.portal_api.create_clazz_quit(order_id=order_id)
            # 获取审批号
            approval_code = self.db.select('SELECT approval_code FROM clazz_quit WHERE order_id = {} and type = 1'.format(order_id))[0][0]
            # 通过审批
            self.portal_api.create_quit_approval_finish(approval_code=approval_code)

    # 通过支付库获取skuid
    def get_sku_id(self, clazz_id):
        sku_ids = self.db.payment.select("select sku_id from sszpay_product_attr where attr_key = 'clazz_ids' and attr_value = {} and status = 1 ;".format(clazz_id))
        sku_ids = [sku_id[0] for sku_id in sku_ids]
        if len(sku_ids)>1:
            sku_ids = tuple(sku_ids)
            sku_id = self.db.select(f"SELECT sku_id FROM product_tag_sku WHERE sku_id in {sku_ids} group by product_tag_id, sku_id;")[0][0]
        else:
            sku_id = int(sku_ids[0])
        return sku_id

    # 通过clazz_id和uid获取order_id
    def get_order_id(self, uid, clazz_id):
        team_ids_dict = self.db.dict.select("SELECT id FROM team WHERE clazz_id = {} and `status` = 1 ;".format(clazz_id))
        team_ids = []
        for team_id in team_ids_dict:
            team_ids.append(team_id.get('id'))
        order_id = self.db.dict.select("SELECT order_id FROM clazz_student_log WHERE clazz_id = {} and team_id in {} and student_id = {} GROUP BY student_id ;".format(clazz_id, tuple(team_ids), uid))[0].get('order_id')
        return order_id

    # 直接payment表获取order_id
    def get_order_id_from_payment(self, uid, clazz_id):
        order_id = self.db.payment.select("SELECT so.p_order_id FROM sszpay_product_attr spa LEFT JOIN sszpay_order so on so.sku_id = spa.sku_id WHERE so.user_id in ({}) AND so.status in (1,2) AND spa.attr_key = 'clazz_ids' and spa.attr_value = {} and spa.status = 1;".format(uid,clazz_id))[0][0]
        return order_id

    # 获取用户的access_token
    def uid2token(self, uid: int):
        access_token = self.db.select("SELECT access_token FROM users WHERE id = {} AND `role` = 3 ;".format(uid))[0][0]
        return access_token

    def get_clazz_master_info_field(self, master_id: int=10706952, clazz_id: int=1793, field='service_num'):
        data = self.db.select("SELECT {} FROM clazz_master_info WHERE master_id in ({}) AND clazz_id = {};".format(field, master_id, clazz_id))
        if data:
            data_num = data[0]
        else:
            data_num = (0,0)
        return data_num


    def get_team_id(self, clazz_id:int):
        data = self.db.select("SELECT id FROM team WHERE clazz_id = {} and status = 1;".format(clazz_id))
        if data:
            team_id = data[0][0]
        else:
            team_id = False
        return team_id


if __name__ == '__main__':
    # 调整课时的时间  为了区分插班和不是插班生
    clazz_id = 1793
    # uid = 10650119
    uid = 196
    test = Renewal()

    # 通过clazz_id 获取skuid
    # sku_id = test.get_sku_id(1793)
    # print(sku_id)
    # order_id = test.get_order_id_from_payment(uid, clazz_id)
    # print(order_id)

    # 通过uid获取access_token
    # token = test.uid2token(uid)
    # print(token)

    # print(test.get_clazz_master_info_field(clazz_id=1424, master_id=10706954))

    # test.adject_clazz_plan_time(clazz_id=1424, days=1)
    # sku_id = test.get_sku_id(3015)
    # print(sku_id)
    # order_id = [25673213300001]
    # test.quit_clazz(order_id)
    # db_utils.DBUtils().pd_from_sql("SELECT * FROM clazz_student_log order BY id DESC limit 10;")
    
    # for clazz_id, master_id in 
    # data = db_utils.DBUtils().select("SELECT t.clazz_id, t.master_id FROM team t left JOIN clazz c on c.id = t.clazz_id WHERE c.`year` = 2020 and c.status =1 and c.`type` =2 and t.team_level=1 and t.status=1 and t.master_id is NOT null GROUP BY master_id, clazz_id;")
    # print(len(data))
#     clazz_id = 2079
#     master_id = 10988939
#     # for clazz_id, master_id in data:
#     old_num = db_utils.DBUtils().select(f"select COUNT(csri.service_value) as num  from clazz_student_renewal_info csri LEFT JOIN clazz_student cs on csri.student_id = cs.student_id and csri.clazz_id = cs.clazz_id where csri.clazz_id = {clazz_id} and csri.master_id = {master_id} and csri.in_clazz_flag =1 and csri.status =1 AND cs.strategy_id!=36;")[0][0]
#     new_num = db_utils.DBUtils().select(f"select service_num from clazz_master_info where clazz_id = {clazz_id} and master_id = {master_id} and status =1;")[0][0]
# # if old_num - new_num != 0 :
#     print(clazz_id, master_id, old_num - new_num)
#     print(old_num, new_num)



    data = db_utils.DBUtils().select("SELECT c.id FROM clazz c	LEFT JOIN clazz_relation cr ON cr.clazz_id = c.id AND cr.type = 1 AND cr.status = 1	LEFT JOIN clazz c2 ON cr.sub_clazz_id = c2.id WHERE	c.year = 2020 AND c.type in(2, 9) AND c.status != - 1;")
    # ids = [id[0] for id in data]
    # print(ids)
    # print(len(ids))

    a = [2048, 2049, 2050, 2051, 2052, 2053, 2054, 2055, 2056, 2057, 2058, 2059, 2060, 2061, 2062, 2063, 2064, 2065, 2066, 2067, 2068, 2069, 2070, 2071, 2072, 2073, 2074, 2075, 2076, 2077, 2078, 2079, 2080, 2081, 2082, 2083, 2085, 2086, 2087, 2088, 2089, 2090, 2091, 2092, 2093, 2094, 2095, 2096, 2097, 2099, 2100, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2110, 2111, 2112, 2478, 2479, 2511, 2515, 2518, 2524, 2537, 2538, 2539, 2580, 2687, 2688, 2693, 2789, 2828, 2829, 2834, 2842, 2843, 2844, 1395, 1396, 1397, 1398, 1399, 1400, 1401, 1402, 1403, 1404, 1405, 1406, 1407, 1408, 1409, 1410, 1411, 1412, 1413, 1414, 1415, 1416, 1417, 1418, 1419, 1420, 1421, 1422, 1423, 1424, 1425, 1426, 1427, 1428, 1429, 1430, 1431, 1432, 1433, 1434, 1437, 1438, 1439, 1440, 1441, 1442, 1443, 1444, 1445, 1446, 1447, 1448, 1449, 1450, 1451, 1452, 1453, 1454, 1455, 1456, 1457, 1458, 1459, 1460, 1461, 1462, 1463, 1464, 1465, 1466, 1467, 1468, 1469, 1470, 1471, 1472, 1473, 1474, 1475, 1476, 1477, 1478, 1479, 1480, 1481, 1482, 1483, 1484, 1485, 1486, 1487, 1488, 1489, 1490, 1491, 1492, 1493, 1494, 1495, 1496, 1498, 1499, 1500, 1501, 1502, 1503, 1504, 1505, 1506, 1507, 1508, 1509, 1510, 1511, 1512, 1513, 1514, 1515, 1516, 1517, 1518, 1519, 1520, 1521, 1522, 1523, 1524, 1525, 1526, 1527, 1528, 1529, 1530, 1532, 1533, 1534, 1535, 1536, 1537, 1538, 1539, 1540, 1541, 1542, 1543, 1544, 1545, 1546, 1547, 1548, 1549, 1550, 1551, 1552, 1553, 1556, 1557, 1558, 1559, 1561, 1562, 1564, 1565, 1566, 1567, 1568, 1569, 1570, 1571, 1572, 1573, 1575, 1576, 1577, 1578, 1579, 1580, 1581, 1582, 1583, 1584, 1585, 1586, 1588, 1589, 1590, 1591, 1592, 1598, 1662, 1671, 1673, 1678, 1712, 1748, 1751, 1758, 1793, 1817, 1865, 1874, 1876, 1901, 1909, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047]
    b = [1395, 1396, 1397, 1398, 1399, 1400, 1401, 1402, 1403, 1404, 1405, 1406, 1407, 1408, 1409, 1410, 1411, 1412, 1413, 1414, 1415, 1416, 1417, 1418, 1419, 1420, 1421, 1422, 1423, 1424, 1425, 1426, 1427, 1428, 1429, 1430, 1431, 1432, 1433, 1434, 1437, 1438, 1439, 1440, 1441, 1442, 1443, 1444, 1445, 1446, 1447, 1448, 1449, 1450, 1451, 1452, 1453, 1454, 1455, 1456, 1457, 1458, 1459, 1460, 1461, 1462, 1463, 1464, 1465, 1466, 1467, 1468, 1469, 1470, 1471, 1472, 1473, 1474, 1475, 1476, 1477, 1478, 1479, 1480, 1481, 1482, 1483, 1484, 1485, 1486, 1487, 1488, 1489, 1490, 1491, 1492, 1493, 1494, 1495, 1496, 1498, 1499, 1500, 1501, 1502, 1503, 1504, 1505, 1506, 1507, 1508, 1509, 1510, 1511, 1512, 1513, 1514, 1515, 1516, 1517, 1518, 1519, 1520, 1521, 1522, 1523, 1524, 1525, 1526, 1527, 1528, 1529, 1530, 1532, 1533, 1534, 1535, 1536, 1537, 1538, 1539, 1540, 1541, 1542, 1543, 1544, 1545, 1546, 1547, 1548, 1549, 1550, 1551, 1552, 1553, 1556, 1557, 1558, 1559, 1561, 1562, 1564, 1565, 1566, 1567, 1568, 1569, 1570, 1571, 1572, 1573, 1575, 1576, 1577, 1578, 1579, 1580, 1581, 1582, 1583, 1584, 1585, 1586, 1588, 1589, 1590, 1591, 1592, 1598, 1662, 1671, 1673, 1678, 1712, 1748, 1751, 1758, 1793, 1817, 1817, 1865, 1874, 1876, 1901, 1909, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050, 2051, 2052, 2053, 2054, 2055, 2056, 2057, 2058, 2059, 2060, 2061, 2062, 2063, 2064, 2065, 2066, 2067, 2068, 2069, 2070, 2071, 2072, 2073, 2074, 2075, 2076, 2077, 2078, 2079, 2080, 2081, 2082, 2083, 2085, 2086, 2087, 2088, 2089, 2090, 2091, 2092, 2093, 2094, 2095, 2096, 2097, 2099, 2100, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2110, 2111, 2112, 2478, 2479, 2511, 2515, 2518, 2524, 2537, 2538, 2539, 2580, 2687, 2688, 2693, 2789, 2828, 2829, 2834, 2842, 2843, 2844]
    c = dict(Counter(b))
    print ([key for key,value in c.items()if value > 1])

