#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Comprehensive data source configuration for subway safety monitoring
Includes: 54 Chinese metro cities, Hong Kong MTR, Weibo, WeChat
"""

# 54 Chinese cities with metro systems
CHINESE_METRO_CITIES = [
    # First-tier and major cities
    {
        "name": "北京地铁",
        "city": "北京",
        "url": "https://www.bjsubway.com",
        "weibo": "北京地铁",
        "wechat": "bjsubway",
    },
    {
        "name": "上海地铁",
        "city": "上海",
        "url": "https://www.shmetro.com",
        "weibo": "上海地铁",
        "wechat": "shmetro",
    },
    {
        "name": "广州地铁",
        "city": "广州",
        "url": "https://www.gzmtr.com",
        "weibo": "广州地铁",
        "wechat": "gzmtr105",
    },
    {
        "name": "深圳地铁",
        "city": "深圳",
        "url": "https://www.szmc.net",
        "weibo": "深圳地铁",
        "wechat": "shenzhenmetro",
    },
    {
        "name": "成都地铁",
        "city": "成都",
        "url": "https://www.chengdu.gov.cn/cdzt/cdsdtlglzx/index.shtml",
        "weibo": "成都地铁",
        "wechat": "chengdumetro",
    },
    {
        "name": "杭州地铁",
        "city": "杭州",
        "url": "https://www.hzmetro.com",
        "weibo": "杭州地铁",
        "wechat": "hangzhoumetro",
    },
    {
        "name": "武汉地铁",
        "city": "武汉",
        "url": "https://www.wuhanmetro.com.cn",
        "weibo": "武汉地铁",
        "wechat": "wuhanmetro",
    },
    {
        "name": "西安地铁",
        "city": "西安",
        "url": "https://www.xianrail.com",
        "weibo": "西安地铁",
        "wechat": "xianmetro",
    },
    {
        "name": "重庆轨道",
        "city": "重庆",
        "url": "https://www.cqmetro.cn",
        "weibo": "重庆轨道",
        "wechat": "cqmetro",
    },
    {
        "name": "天津地铁",
        "city": "天津",
        "url": "https://www.tjmetro.com",
        "weibo": "天津地铁",
        "wechat": "tjmetro",
    },
    # Second-tier cities
    {
        "name": "南京地铁",
        "city": "南京",
        "url": "https://www.njmetro.com.cn",
        "weibo": "南京地铁",
        "wechat": "njdtglzx",
    },
    {
        "name": "苏州轨道交通",
        "city": "苏州",
        "url": "https://www.sz-mtr.com",
        "weibo": "苏州轨道交通",
        "wechat": "sz-mtr",
    },
    {
        "name": "郑州地铁",
        "city": "郑州",
        "url": "https://www.zzmetro.com",
        "weibo": "郑州地铁",
        "wechat": "zhengzhoumetro",
    },
    {
        "name": "长沙地铁",
        "city": "长沙",
        "url": "https://www.hncsmtr.com",
        "weibo": "长沙地铁",
        "wechat": "hncsmtr",
    },
    {
        "name": "沈阳地铁",
        "city": "沈阳",
        "url": "https://www.symtc.com",
        "weibo": "沈阳地铁",
        "wechat": "symtc",
    },
    {
        "name": "宁波轨道交通",
        "city": "宁波",
        "url": "https://www.nbmetro.com.cn",
        "weibo": "宁波轨道交通",
        "wechat": "nbgdjt",
    },
    {
        "name": "青岛地铁",
        "city": "青岛",
        "url": "https://www.qdmtr.com",
        "weibo": "青岛地铁",
        "wechat": "qdmtr",
    },
    {
        "name": "大连地铁",
        "city": "大连",
        "url": "https://www.dlmetro.com.cn",
        "weibo": "大连地铁",
        "wechat": "dalianmetro",
    },
    {
        "name": "东莞轨道交通",
        "city": "东莞",
        "url": "https://www.dggdjt.com",
        "weibo": "东莞轨道交通",
        "wechat": "dggdjt",
    },
    {
        "name": "无锡地铁",
        "city": "无锡",
        "url": "https://www.wxmetro.net.cn",
        "weibo": "无锡地铁",
        "wechat": "wuximetro",
    },
    # Third-tier cities
    {
        "name": "石家庄地铁",
        "city": "石家庄",
        "url": "https://www.sjzmetro.com.cn",
        "weibo": "石家庄地铁",
        "wechat": "sjzmetro",
    },
    {
        "name": "福州地铁",
        "city": "福州",
        "url": "https://www.fzmtr.com",
        "weibo": "福州地铁",
        "wechat": "fuzhoumetro",
    },
    {
        "name": "厦门地铁",
        "city": "厦门",
        "url": "https://www.xmtr.com",
        "weibo": "厦门地铁",
        "wechat": "xiamenmetro",
    },
    {
        "name": "济南地铁",
        "city": "济南",
        "url": "https://www.jnmetro.com",
        "weibo": "济南地铁",
        "wechat": "jinanditie",
    },
    {
        "name": "南昌地铁",
        "city": "南昌",
        "url": "https://www.ncmtr.com",
        "weibo": "南昌地铁",
        "wechat": "ncsubway",
    },
    {
        "name": "合肥地铁",
        "city": "合肥",
        "url": "https://www.hfgd.com.cn",
        "weibo": "合肥地铁",
        "wechat": "hefeimetro",
    },
    {
        "name": "贵阳地铁",
        "city": "贵阳",
        "url": "https://www.gyurbanmetro.com.cn",
        "weibo": "贵阳地铁",
        "wechat": "guiyangmetro",
    },
    {
        "name": "太原地铁",
        "city": "太原",
        "url": "https://www.tymetro.com.cn",
        "weibo": "太原地铁",
        "wechat": "taiyuanmetro",
    },
    {
        "name": "乌鲁木齐地铁",
        "city": "乌鲁木齐",
        "url": "https://www.urumqimetro.com",
        "weibo": "乌鲁木齐地铁",
        "wechat": "wlmqmetro",
    },
    {
        "name": "长春地铁",
        "city": "长春",
        "url": "https://www.cccmt.com",
        "weibo": "长春地铁",
        "wechat": "changchunmetro",
    },
    # Fourth-tier and newer metros
    {
        "name": "哈尔滨地铁",
        "city": "哈尔滨",
        "url": "https://www.hrbmetro.com",
        "weibo": "哈尔滨地铁",
        "wechat": "hrbmetro",
    },
    {
        "name": "昆明轨道交通",
        "city": "昆明",
        "url": "https://www.kmgdjs.com",
        "weibo": "昆明轨道交通",
        "wechat": "kunmingmetro",
    },
    {
        "name": "兰州地铁",
        "city": "兰州",
        "url": "https://www.lzmetro.com.cn",
        "weibo": "兰州地铁",
        "wechat": "lanzhoumetro",
    },
    {
        "name": "呼和浩特地铁",
        "city": "呼和浩特",
        "url": "https://www.hhhtmetro.com",
        "weibo": "呼和浩特地铁",
        "wechat": "hhhtmetro",
    },
    {
        "name": "银川轨道交通",
        "city": "银川",
        "url": "https://www.ycgdjt.com",
        "weibo": "银川轨道交通",
        "wechat": "yinchuanmetro",
    },
    {
        "name": "西宁地铁",
        "city": "西宁",
        "url": "https://www.xnmetro.com",
        "weibo": "西宁地铁",
        "wechat": "xiningmetro",
    },
    {
        "name": "徐州地铁",
        "city": "徐州",
        "url": "https://www.xzdtcm.com",
        "weibo": "徐州地铁",
        "weichat": "xuzhoumetro",
    },
    {
        "name": "常州地铁",
        "city": "常州",
        "url": "https://www.czmetro.com.cn",
        "weibo": "常州地铁",
        "wechat": "changzhoumetro",
    },
    {
        "name": "温州轨道",
        "city": "温州",
        "url": "https://www.wzmtr.com",
        "weibo": "温州轨道",
        "wechat": "wzgdjt",
    },
    {
        "name": "绍兴地铁",
        "city": "绍兴",
        "url": "https://www.sxmetro.com",
        "weibo": "绍兴地铁",
        "wechat": "shaoxingmetro",
    },
    {
        "name": "芜湖轨道",
        "city": "芜湖",
        "url": "https://www.wuhumetro.com",
        "weibo": "芜湖轨道",
        "wechat": "wuhumetro",
    },
    {
        "name": "洛阳轨道交通",
        "city": "洛阳",
        "url": "https://www.lygdjt.com",
        "weibo": "洛阳轨道交通",
        "wechat": "luoyangmetro",
    },
    {
        "name": "南通轨道交通",
        "city": "南通",
        "url": "https://www.ntgdjt.com",
        "weibo": "南通轨道交通",
        "wechat": "nantongmetro",
    },
    {
        "name": "金华轨道",
        "city": "金华",
        "url": "https://www.jhgdjt.com",
        "weibo": "金华轨道",
        "wechat": "jhgds",
    },
    {
        "name": "台州轨道",
        "city": "台州",
        "url": "https://www.tzgdjt.com",
        "weibo": "台州轨道",
        "wechat": "taizhoumetro",
    },
    {
        "name": "嘉兴轨道",
        "city": "嘉兴",
        "url": "https://www.jxcm.cn",
        "weibo": "嘉兴轨道",
        "wechat": "jiaxingmetro",
    },
    {
        "name": "绍兴柯桥轨道",
        "city": "绍兴",
        "url": "https://www.sxkgd.com",
        "weibo": "绍兴柯桥轨道",
        "wechat": "sxkqgd",
    },
    {
        "name": "兰州新区轨道",
        "city": "兰州",
        "url": "https://www.lzxqgd.com",
        "weibo": "兰州新区轨道",
        "wechat": "lzxqgd",
    },
    {
        "name": "苏州吴江轨道",
        "city": "苏州",
        "url": "https://www.wujiangmetro.com",
        "weibo": "苏州吴江轨道",
        "wechat": "wjrmt",
    },
    {
        "name": "海口轨道",
        "city": "海口",
        "url": "https://www.hkmetro.com",
        "weibo": "海口轨道",
        "wechat": "haikoumetro",
    },
]

# Hong Kong and Macau
HK_MACAU_METRO = [
    {
        "name": "港铁 MTR",
        "city": "香港",
        "url": "https://www.mtr.com.hk",
        "weibo": "港铁",
        "wechat": "mtrhker",
    },
    {
        "name": "澳门轻轨",
        "city": "澳门",
        "url": "https://www.lrt.gov.mo",
        "weibo": "澳门轻轨",
        "wechat": "macauLRT",
    },
]

# Industry associations and government sources
GOVERNMENT_SOURCES = [
    {
        "name": "中国城市轨道交通协会",
        "city": "全国",
        "url": "http://www.camet.org.cn",
        "weibo": "中国城市轨道交通协会",
        "wechat": "camet123",
    },
    {
        "name": "交通运输部",
        "city": "全国",
        "url": "https://www.mot.gov.cn",
        "weibo": "交通运输部",
        "wechat": "mot-gov",
    },
    {
        "name": "国家铁路局",
        "city": "全国",
        "url": "https://www.nra.gov.cn",
        "weibo": "国家铁路局",
        "wechat": "nragov",
    },
]

# Provincial-level transportation and emergency management departments
# (For provinces with metro systems)
PROVINCIAL_SOURCES = {
    "transportation": [
        {
            "name": "广东省交通运输厅",
            "province": "广东",
            "url": "https://td.gd.gov.cn",
            "type": "province",
        },
        {
            "name": "江苏省交通运输厅",
            "province": "江苏",
            "url": "https://jtyst.jiangsu.gov.cn",
            "type": "province",
        },
        {
            "name": "浙江省交通运输厅",
            "province": "浙江",
            "url": "https://jtyst.zj.gov.cn",
            "type": "province",
        },
        {
            "name": "山东省交通运输厅",
            "province": "山东",
            "url": "https://sdygj.gov.cn",
            "type": "province",
        },
        {
            "name": "河南省交通运输厅",
            "province": "河南",
            "url": "https://www.hncd.gov.cn",
            "type": "province",
        },
        {
            "name": "四川省交通运输厅",
            "province": "四川",
            "url": "https://jtt.sc.gov.cn",
            "type": "province",
        },
        {
            "name": "湖北省交通运输厅",
            "province": "湖北",
            "url": "https://jtt.hubei.gov.cn",
            "type": "province",
        },
        {
            "name": "湖南省交通运输厅",
            "province": "湖南",
            "url": "https://jtt.hunan.gov.cn",
            "type": "province",
        },
        {
            "name": "安徽省交通运输厅",
            "province": "安徽",
            "url": "https://jtt.ah.gov.cn",
            "type": "province",
        },
        {
            "name": "福建省交通运输厅",
            "province": "福建",
            "url": "https://jt.fj.gov.cn",
            "type": "province",
        },
        {
            "name": "江西省交通运输厅",
            "province": "江西",
            "url": "https://jt.jiangxi.gov.cn",
            "type": "province",
        },
        {
            "name": "辽宁省交通运输厅",
            "province": "辽宁",
            "url": "https://jtt.ln.gov.cn",
            "type": "province",
        },
        {
            "name": "吉林省交通运输厅",
            "province": "吉林",
            "url": "https://jt.jl.gov.cn",
            "type": "province",
        },
        {
            "name": "黑龙江省交通运输厅",
            "province": "黑龙江",
            "url": "https://hljjt.gov.cn",
            "type": "province",
        },
        {
            "name": "河北省交通运输厅",
            "province": "河北",
            "url": "https://hbt.hebei.gov.cn",
            "type": "province",
        },
        {
            "name": "山西省交通运输厅",
            "province": "山西",
            "url": "https://jt.shanxi.gov.cn",
            "type": "province",
        },
        {
            "name": "云南省交通运输厅",
            "province": "云南",
            "url": "https://jt.yn.gov.cn",
            "type": "province",
        },
        {
            "name": "贵州省交通运输厅",
            "province": "贵州",
            "url": "https://jt.guizhou.gov.cn",
            "type": "province",
        },
        {
            "name": "甘肃省交通运输厅",
            "province": "甘肃",
            "url": "https://jt.gansu.gov.cn",
            "type": "province",
        },
        {
            "name": "内蒙古自治区交通运输厅",
            "province": "内蒙古",
            "url": "https://jt.nmg.gov.cn",
            "type": "province",
        },
        {
            "name": "新疆维吾尔自治区交通运输厅",
            "province": "新疆",
            "url": "https://jt.xinjiang.gov.cn",
            "type": "province",
        },
        {
            "name": "宁夏回族自治区交通运输厅",
            "province": "宁夏",
            "url": "https://jtt.nx.gov.cn",
            "type": "province",
        },
        {
            "name": "青海省交通运输厅",
            "province": "青海",
            "url": "https://jt.qinghai.gov.cn",
            "type": "province",
        },
    ],
    "emergency_management": [
        {
            "name": "广东省应急管理厅",
            "province": "广东",
            "url": "https://yjgl.gd.gov.cn",
            "type": "province",
        },
        {
            "name": "江苏省应急管理厅",
            "province": "江苏",
            "url": "https://yjgl.jiangsu.gov.cn",
            "type": "province",
        },
        {
            "name": "浙江省应急管理厅",
            "province": "浙江",
            "url": "https://zjyjgl.gov.cn",
            "type": "province",
        },
        {
            "name": "山东省应急管理厅",
            "province": "山东",
            "url": "https://yjgl.shandong.gov.cn",
            "type": "province",
        },
        {
            "name": "河南省应急管理厅",
            "province": "河南",
            "url": "https://safety.henan.gov.cn",
            "type": "province",
        },
        {
            "name": "四川省应急管理厅",
            "province": "四川",
            "url": "https://yjgl.sc.gov.cn",
            "type": "province",
        },
        {
            "name": "湖北省应急管理厅",
            "province": "湖北",
            "url": "https://yjt.hubei.gov.cn",
            "type": "province",
        },
        {
            "name": "湖南省应急管理厅",
            "province": "湖南",
            "url": "https://yjgl.hunan.gov.cn",
            "type": "province",
        },
        {
            "name": "安徽省应急管理厅",
            "province": "安徽",
            "url": "https://yjj.ah.gov.cn",
            "type": "province",
        },
        {
            "name": "福建省应急管理厅",
            "province": "福建",
            "url": "https://fjsafety.gov.cn",
            "type": "province",
        },
        {
            "name": "江西省应急管理厅",
            "province": "江西",
            "url": "https://yjgl.jiangxi.gov.cn",
            "type": "province",
        },
        {
            "name": "辽宁省应急管理厅",
            "province": "辽宁",
            "url": "https://ln.gov.cn/fzms/yingjiguanli",
            "type": "province",
        },
        {
            "name": "吉林省应急管理厅",
            "province": "吉林",
            "url": "https://jlsafety.gov.cn",
            "type": "province",
        },
        {
            "name": "黑龙江省应急管理厅",
            "province": "黑龙江",
            "url": "https://yjgl.gov.cn",
            "type": "province",
        },
        {
            "name": "河北省应急管理厅",
            "province": "河北",
            "url": "https://yjgl.hebei.gov.cn",
            "type": "province",
        },
        {
            "name": "山西省应急管理厅",
            "province": "山西",
            "url": "https://yjgl.shanxi.gov.cn",
            "type": "province",
        },
        {
            "name": "云南省应急管理厅",
            "province": "云南",
            "url": "https://yjg.yn.gov.cn",
            "type": "province",
        },
        {
            "name": "贵州省应急管理厅",
            "province": "贵州",
            "url": "https://yjgl.guizhou.gov.cn",
            "type": "province",
        },
        {
            "name": "甘肃省应急管理厅",
            "province": "甘肃",
            "url": "https://yjgl.gansu.gov.cn",
            "type": "province",
        },
        {
            "name": "内蒙古自治区应急管理厅",
            "province": "内蒙古",
            "url": "https://yjgl.nmg.gov.cn",
            "type": "province",
        },
        {
            "name": "新疆维吾尔自治区应急管理厅",
            "province": "新疆",
            "url": "https://xj.gov.cn/gov/yjj",
            "type": "province",
        },
        {
            "name": "宁夏回族自治区应急管理厅",
            "province": "宁夏",
            "url": "https://nx.gov.cn/yjj",
            "type": "province",
        },
        {
            "name": "青海省应急管理厅",
            "province": "青海",
            "url": "https://qinghai.gov.cn/gov/yjj",
            "type": "province",
        },
    ],
}

# City-level transportation bureaus and emergency management bureaus
CITY_GOVERNMENT_SOURCES = {
    "transportation_bureaus": [
        {
            "name": "北京市交通委员会",
            "city": "北京",
            "url": "https://jw.beijing.gov.cn",
            "type": "city",
        },
        {
            "name": "上海市交通委员会",
            "city": "上海",
            "url": "https://jw.shanghai.gov.cn",
            "type": "city",
        },
        {
            "name": "广州市交通运输局",
            "city": "广州",
            "url": "https://www.gz.gov.cn/gzswjg/index",
            "type": "city",
        },
        {
            "name": "深圳市交通运输局",
            "city": "深圳",
            "url": "https://jtys.sz.gov.cn",
            "type": "city",
        },
        {
            "name": "成都市交通运输局",
            "city": "成都",
            "url": "https://www.cdjt.gov.cn",
            "type": "city",
        },
        {
            "name": "杭州市交通运输局",
            "city": "杭州",
            "url": "https://hzcb.hangzhou.gov.cn",
            "type": "city",
        },
        {
            "name": "武汉市交通运输局",
            "city": "武汉",
            "url": "https://www.wht.gov.cn/wuhanjiaotong",
            "type": "city",
        },
        {
            "name": "西安市交通运输局",
            "city": "西安",
            "url": "http://jtys.xa.gov.cn",
            "type": "city",
        },
        {
            "name": "重庆市交通局",
            "city": "重庆",
            "url": "https://www.cq.gov.cn/sy/jtw",
            "type": "city",
        },
        {
            "name": "天津市交通运输委员会",
            "city": "天津",
            "url": "https://www.tj.gov.cn/jtw",
            "type": "city",
        },
        {
            "name": "南京市交通运输局",
            "city": "南京",
            "url": "https://www.njjt.gov.cn",
            "type": "city",
        },
        {
            "name": "苏州市交通运输局",
            "city": "苏州",
            "url": "https://www.szjt.gov.cn",
            "type": "city",
        },
        {
            "name": "郑州市交通运输局",
            "city": "郑州",
            "url": "https://zzsj.zhengzhou.gov.cn",
            "type": "city",
        },
        {
            "name": "长沙市交通运输局",
            "city": "长沙",
            "url": "https://www.hnszjt.com",
            "type": "city",
        },
        {
            "name": "沈阳市交通运输局",
            "city": "沈阳",
            "url": "https://www.syjt.gov.cn",
            "type": "city",
        },
        {
            "name": "宁波市交通运输局",
            "city": "宁波",
            "url": "https://www.nbjt.gov.cn",
            "type": "city",
        },
        {
            "name": "青岛市交通运输局",
            "city": "青岛",
            "url": "https://www.qdjt.gov.cn",
            "type": "city",
        },
        {
            "name": "大连市交通运输局",
            "city": "大连",
            "url": "https://www.dl.gov.cn/dlj",
            "type": "city",
        },
        {
            "name": "东莞市交通运输局",
            "city": "东莞",
            "url": "https://www.dg.gov.cn/jtj",
            "type": "city",
        },
        {
            "name": "无锡市交通运输局",
            "city": "无锡",
            "url": "https://www.wuxi.gov.cn/jtj",
            "type": "city",
        },
    ],
    "emergency_management_bureaus": [
        {
            "name": "北京市应急管理局",
            "city": "北京",
            "url": "https://yjglj.beijing.gov.cn",
            "type": "city",
        },
        {
            "name": "上海市应急管理局",
            "city": "上海",
            "url": "https://www.shemergency.gov.cn",
            "type": "city",
        },
        {
            "name": "广州市应急管理局",
            "city": "广州",
            "url": "https://www.gz.gov.cn/emergency",
            "type": "city",
        },
        {
            "name": "深圳市应急管理局",
            "city": "深圳",
            "url": "https://www.sz.gov.cn/safety",
            "type": "city",
        },
        {
            "name": "成都市应急管理局",
            "city": "成都",
            "url": "https://cdyjgl.chengdu.gov.cn",
            "type": "city",
        },
        {
            "name": "杭州市应急管理局",
            "city": "杭州",
            "url": "https://yjgl.hangzhou.gov.cn",
            "type": "city",
        },
        {
            "name": "武汉市应急管理局",
            "city": "武汉",
            "url": "https://www.wh.gov.cn/yjj",
            "type": "city",
        },
        {
            "name": "西安市应急管理局",
            "city": "西安",
            "url": "https://yjj.xa.gov.cn",
            "type": "city",
        },
        {
            "name": "重庆市应急管理局",
            "city": "重庆",
            "url": "https://www.cq.gov.cn/yjj",
            "type": "city",
        },
        {
            "name": "天津市应急管理局",
            "city": "天津",
            "url": "https://www.tj.gov.cn/yjj",
            "type": "city",
        },
        {
            "name": "南京市应急管理局",
            "city": "南京",
            "url": "https://ajj.nanjing.gov.cn",
            "type": "city",
        },
        {
            "name": "苏州市应急管理局",
            "city": "苏州",
            "url": "https://www.szsafety.gov.cn",
            "type": "city",
        },
        {
            "name": "郑州市应急管理局",
            "city": "郑州",
            "url": "https://ajj.zhengzhou.gov.cn",
            "type": "city",
        },
        {
            "name": "长沙市应急管理局",
            "city": "长沙",
            "url": "https://www.changsha.gov.cn/yjj",
            "type": "city",
        },
        {
            "name": "沈阳市应急管理局",
            "city": "沈阳",
            "url": "https://www.sy.gov.cn/yjj",
            "type": "city",
        },
        {
            "name": "宁波市应急管理局",
            "city": "宁波",
            "url": "https://www.nbsafety.gov.cn",
            "type": "city",
        },
        {
            "name": "青岛市应急管理局",
            "city": "青岛",
            "url": "https://qdemoa.qingdao.gov.cn",
            "type": "city",
        },
        {
            "name": "大连市应急管理局",
            "city": "大连",
            "url": "https://www.dl.gov.cn/yjj",
            "type": "city",
        },
        {
            "name": "东莞市应急管理局",
            "city": "东莞",
            "url": "https://www.dg.gov.cn/yjj",
            "type": "city",
        },
        {
            "name": "无锡市应急管理局",
            "city": "无锡",
            "url": "https://www.wuxi.gov.cn/yjj",
            "type": "city",
        },
    ],
}

# Direct-controlled municipalities government sources
MUNICIPALITY_SOURCES = {
    "beijing": [
        {
            "name": "北京市交通委员会",
            "url": "https://jw.beijing.gov.cn",
            "type": "municipal_transportation",
        },
        {
            "name": "北京市应急管理局",
            "url": "https://yjglj.beijing.gov.cn",
            "type": "municipal_emergency",
        },
    ],
    "shanghai": [
        {
            "name": "上海市交通委员会",
            "url": "https://jw.shanghai.gov.cn",
            "type": "municipal_transportation",
        },
        {
            "name": "上海市应急管理局",
            "url": "https://www.shemergency.gov.cn",
            "type": "municipal_emergency",
        },
    ],
    "tianjin": [
        {
            "name": "天津市交通运输委员会",
            "url": "https://www.tj.gov.cn/jtw",
            "type": "municipal_transportation",
        },
        {
            "name": "天津市应急管理局",
            "url": "https://www.tj.gov.cn/yjj",
            "type": "municipal_emergency",
        },
    ],
    "chongqing": [
        {
            "name": "重庆市交通局",
            "url": "https://www.cq.gov.cn/sy/jtw",
            "type": "municipal_transportation",
        },
        {
            "name": "重庆市应急管理局",
            "url": "https://www.cq.gov.cn/yjj",
            "type": "municipal_emergency",
        },
    ],
}

# International sources
INTERNATIONAL_SOURCES = [
    {
        "name": "UITP (国际公共交通协会)",
        "city": "国际",
        "url": "https://www.uitp.org",
        "weibo": "",
        "wechat": "",
    },
    {
        "name": "Federal Transit Administration",
        "city": "美国",
        "url": "https://www.transit.dot.gov",
        "weibo": "",
        "wechat": "",
    },
    {
        "name": "Tokyo Metro",
        "city": "东京",
        "url": "https://www.tokyometro.jp",
        "weibo": "",
        "wechat": "",
    },
    {
        "name": "Singapore MRT",
        "city": "新加坡",
        "url": "https://www.sbstransit.com.sg",
        "weibo": "",
        "wechat": "",
    },
    {
        "name": "London Underground",
        "city": "伦敦",
        "url": "https://tfl.gov.uk",
        "weibo": "",
        "wechat": "",
    },
]

# Social media monitoring targets
SOCIAL_MEDIA_SOURCES = {
    "weibo": [
        {"name": "北京地铁", "uid": "1921971483", "type": "official"},
        {"name": "上海地铁", "uid": "1780024675", "type": "official"},
        {"name": "广州地铁", "uid": "1682624913", "type": "official"},
        {"name": "深圳地铁", "uid": "1665243115", "type": "official"},
        {"name": "成都地铁", "uid": "1823881805", "type": "official"},
        {"name": "杭州地铁", "uid": "1739347920", "type": "official"},
        {"name": "武汉地铁", "uid": "1853384914", "type": "official"},
        {"name": "西安地铁", "uid": "1853384721", "type": "official"},
        {"name": "重庆轨道", "uid": "1848646862", "type": "official"},
        {"name": "天津地铁", "uid": "1825056707", "type": "official"},
        {"name": "中国城市轨道交通协会", "uid": "1921971483", "type": "association"},
    ],
    "wechat": [
        {"name": "北京地铁", "id": "bjsubway"},
        {"name": "上海地铁", "id": "shmetro"},
        {"name": "广州地铁", "id": "gzmtr105"},
        {"name": "深圳地铁", "id": "shenzhenmetro"},
        {"name": "成都地铁", "id": "chengdumetro"},
        {"name": "杭州地铁", "id": "hangzhoumetro"},
        {"name": "武汉地铁", "id": "wuhanmetro"},
        {"name": "西安地铁", "id": "xianmetro"},
        {"name": "重庆轨道", "id": "cqmetro"},
        {"name": "天津地铁", "id": "tjmetro"},
        {"name": "南京地铁", "id": "njdtglzx"},
        {"name": "中国城市轨道交通协会", "id": "camet123"},
    ],
}


def get_all_data_sources():
    """Get all configured data sources"""
    all_sources = {
        "chinese_cities": CHINESE_METRO_CITIES,
        "hk_macau": HK_MACAU_METRO,
        "government": GOVERNMENT_SOURCES,
        "provincial_transportation": PROVINCIAL_SOURCES["transportation"],
        "provincial_emergency": PROVINCIAL_SOURCES["emergency_management"],
        "city_transportation": CITY_GOVERNMENT_SOURCES["transportation_bureaus"],
        "city_emergency": CITY_GOVERNMENT_SOURCES["emergency_management_bureaus"],
        "municipalities": MUNICIPALITY_SOURCES,
        "international": INTERNATIONAL_SOURCES,
        "social_media": SOCIAL_MEDIA_SOURCES,
    }
    return all_sources


def get_source_statistics():
    """Get statistics about configured sources"""
    provincial_transport = len(PROVINCIAL_SOURCES["transportation"])
    provincial_emergency = len(PROVINCIAL_SOURCES["emergency_management"])
    city_transport = len(CITY_GOVERNMENT_SOURCES["transportation_bureaus"])
    city_emergency = len(CITY_GOVERNMENT_SOURCES["emergency_management_bureaus"])
    municipalities = sum(len(v) for v in MUNICIPALITY_SOURCES.values())

    stats = {
        "total_chinese_cities": len(CHINESE_METRO_CITIES),
        "hk_macau": len(HK_MACAU_METRO),
        "government": len(GOVERNMENT_SOURCES),
        "provincial_transportation": provincial_transport,
        "provincial_emergency": provincial_emergency,
        "city_transportation": city_transport,
        "city_emergency": city_emergency,
        "municipalities": municipalities,
        "international": len(INTERNATIONAL_SOURCES),
        "weibo_accounts": len(SOCIAL_MEDIA_SOURCES["weibo"]),
        "wechat_accounts": len(SOCIAL_MEDIA_SOURCES["wechat"]),
    }
    stats["total"] = (
        stats["total_chinese_cities"]
        + stats["hk_macau"]
        + stats["government"]
        + provincial_transport
        + provincial_emergency
        + city_transport
        + city_emergency
        + municipalities
        + stats["international"]
    )
    return stats


if __name__ == "__main__":
    stats = get_source_statistics()
    print("=" * 60)
    print("Subway Safety Dashboard - Data Source Statistics")
    print("=" * 60)
    print(f"Chinese Metro Cities: {stats['total_chinese_cities']}")
    print(f"Hong Kong/Macau: {stats['hk_macau']}")
    print(f"National Government: {stats['government']}")
    print(f"Provincial Transportation: {stats['provincial_transportation']}")
    print(f"Provincial Emergency: {stats['provincial_emergency']}")
    print(f"City Transportation: {stats['city_transportation']}")
    print(f"City Emergency: {stats['city_emergency']}")
    print(f"Municipalities: {stats['municipalities']}")
    print(f"International: {stats['international']}")
    print(f"Weibo Accounts: {stats['weibo_accounts']}")
    print(f"WeChat Accounts: {stats['wechat_accounts']}")
    print("-" * 60)
    print(f"TOTAL Data Sources: {stats['total']}")
    print("=" * 60)
