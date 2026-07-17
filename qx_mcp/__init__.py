import asyncio
import json
import hashlib
import time
import logging

import httpx
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("qx-mcp")

APPKEY = "xxxxxxxxxxxxxxxxxxxxx"
SECRET_KEY = "xxxxxxxxxxxxxxxxxxxxx"
BASE_URL = "https://api.qixin.com"

client = httpx.Client(base_url=BASE_URL, timeout=30)

mcp = FastMCP("qx-mcp")


def sign(timestamp: str) -> str:
    raw = APPKEY + timestamp + SECRET_KEY
    return hashlib.md5(raw.encode()).hexdigest()


def auth_headers() -> dict[str, str]:
    ts = str(int(time.time() * 1000))
    return {
        "Auth-Version": "2.0",
        "appkey": APPKEY,
        "timestamp": ts,
        "sign": sign(ts),
    }


def api_get(path: str, params: dict | None = None) -> str:
    resp = client.get(path, params=params, headers=auth_headers())
    resp.raise_for_status()
    return json.dumps(resp.json(), ensure_ascii=False)


def api_post(path: str, json_body: dict | None = None) -> str:
    resp = client.post(path, json=json_body, headers=auth_headers())
    resp.raise_for_status()
    return json.dumps(resp.json(), ensure_ascii=False)


def make_query(**kw) -> dict:
    return {k: v for k, v in kw.items() if v is not None}


# ═══ 1. 基础工商信息 ═══════════════════════════════════════

@mcp.tool(name="get_enterprise_basic_info", description="企业基础工商信息 — 包含照面/联系方式/主要人员/股东/变更/经营异常等")
async def get_enterprise_basic_info(keyword: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getDetailAndContactByName", {"keyword": keyword})


@mcp.tool(name="get_business_license", description="工商照面 — 统一社会信用代码/注册资本/经营范围/法定代表人")
async def get_business_license(keyword: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getBasicInfo", {"keyword": keyword})


@mcp.tool(name="get_enterprise_brief", description="企业简介")
async def get_enterprise_brief(name: str) -> str:
    """企业全名/统一社会信用代码/注册号"""
    return api_get("/APIService/enterprise/getEntBriefByName", {"name": name})


@mcp.tool(name="get_enterprise_logo", description="企业LOGO")
async def get_enterprise_logo(name: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getEntLogoByName", {"name": name})


@mcp.tool(name="get_history_names", description="企业历史名称")
async def get_history_names(keyword: str, skip: int = 0) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getHistoryName", {"keyword": keyword, "skip": str(skip)})


@mcp.tool(name="get_enterprise_codes", description="企业三码 — 统一社会信用代码/组织机构代码/注册号")
async def get_enterprise_codes(name: str, skip: int = 0) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getCreditCode", {"name": name, "skip": str(skip)})


@mcp.tool(name="get_capital_background", description="企业性质（资本背景）")
async def get_capital_background(name: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getEntCapCate", {"name": name})


@mcp.tool(name="get_enterprise_scale", description="企业规模 — 微型/小型/中型/大型")
async def get_enterprise_scale(name: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getEntSize", {"name": name})


@mcp.tool(name="get_industry_classification", description="企业行业（国民经济分类）")
async def get_industry_classification(name: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getIndClass", {"name": name})


@mcp.tool(name="get_enterprise_subject_type", description="企业主体性质 — 央企/地方国企/民企/事业单位等")
async def get_enterprise_subject_type(keyword: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getMerchantsType", {"keyword": keyword})


# ═══ 2. 股东/股权/投资 ═════════════════════════════════════

@mcp.tool(name="get_shareholders", description="工商股东信息（不含自行公示和年报股东）")
async def get_shareholders(keyword: str, skip: int = 0) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getPartners", {"keyword": keyword, "skip": str(skip)})


@mcp.tool(name="get_shareholders_public", description="工商股东信息（工商公示，含历史股东）")
async def get_shareholders_public(keyword: str, skip: int = 0) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getEntPartners", {"keyword": keyword, "skip": str(skip)})


@mcp.tool(name="get_investment_info", description="对外投资信息（最优股比）")
async def get_investment_info(name: str, skip: int = 0) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getEntInvestByName", {"name": name, "skip": str(skip)})


@mcp.tool(name="get_optimal_share_ratio", description="最优股比信息 — 综合多源数据算出的股比")
async def get_optimal_share_ratio(name: str, skip: int = 0) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getShareHolderByName", {"name": name, "skip": str(skip)})


@mcp.tool(name="get_invested_companies", description="参股控股企业信息")
async def get_invested_companies(keyword: str, skip: int = 0, pname: str | None = None) -> str:
    """企业全名/注册号/统一社会信用代码"""
    params = {"keyword": keyword, "skip": str(skip)}
    if pname:
        params["pname"] = pname
    return api_get("/APIService/investment/getEntInvestmentByName", params)


@mcp.tool(name="get_actual_control_companies", description="实际控制企业 — 相同实际控制人的企业信息")
async def get_actual_control_companies(name: str) -> str:
    """企业全名/统一社会信用代码"""
    return api_get("/APIService/investment/getActualControlsByName", {"name": name})


# ═══ 3. 关联关系 ════════════════════════════════════════════

@mcp.tool(name="get_suspect_relations", description="疑似关联方查询 — 相同软件著作权/专利/电话/地址等")
async def get_suspect_relations(name: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/relation/getSuspectRelationship", {"name": name})


@mcp.tool(name="get_related_enterprises", description="关联企业 — 法人/股东/对外投资/董监高两层穿透")
async def get_related_enterprises(
    name: str,
    relationship_type: str | None = None,
    relationship_level: str | None = None,
) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/relation/getRelatedRelation", make_query(keyword=keyword, relationship_type=relationship_type, relationship_level=relationship_level))


@mcp.tool(name="get_related_party_identification", description="关联方认定 — 上交所规则关联关系（含持股/路径）")
async def get_related_party_identification(name: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/relation/getRelatedRelationAndBasicInfo", {"name": name})


@mcp.tool(name="get_enterprise_chain", description="企业链图 — 股东/高管/对外投资/诉讼/疑似关系全景")
async def get_enterprise_chain(keyword: str) -> str:
    """公司全名"""
    return api_get("/APIService/relation/getChainRelationByName", {"keyword": keyword})


@mcp.tool(name="find_relation_between_two", description="两家企业间关联关系排查（最深15层）")
async def find_relation_between_two(
    keywordone: str, keywordtwo: str,
    relation: str | None = None, level: str | None = None,
) -> str:
    """关键词1, 关键词2"""
    return api_get("/APIService/relation/getTwoByName", make_query(keywordone=keywordone, keywordtwo=keywordtwo, relation=relation, level=level))


@mcp.tool(name="create_relation_find_task", description="企业间找关系-JOB申请（最多10家）- 异步返回key")
async def create_relation_find_task(
    enterprises: str,
    persons: str | None = None, relations: str | None = None,
    level: str | None = None, containSuspect: str | None = None,
) -> str:
    """企业全名用逗号分隔（2-10家）"""
    return api_get("/APIService/relation/createFindRelationTask", make_query(enterprises=enterprises, persons=persons, relations=relations, level=level, containSuspect=containSuspect))


@mcp.tool(name="get_relation_find_result", description="企业间找关系-详细数据 — 根据key查询结果")
async def get_relation_find_result(key: str) -> str:
    """33.10接口返回的key"""
    return api_get("/APIService/relation/getFindRelationResult", {"key": key})


@mcp.tool(name="create_multi_relation_job_50", description="多家企业间找关系job申请（最多50家）- 异步返回job_id")
async def create_multi_relation_job_50(keywords: str, is_execute: int, relations: str | None = None, level: str | None = None) -> str:
    """企业全名/人员信息用逗号分隔，人员用|定位"""
    return api_post("/APIService/relation/getMultiByName", {"keywords": keywords, "is_execute": str(is_execute), "relations": relations or "", "level": level or "6"})


@mcp.tool(name="get_multi_relation_detail_50", description="多家企业间找关系详情（50家）- 根据job_id获取结果")
async def get_multi_relation_detail_50(job_id: str, skip: int = 0) -> str:
    """22.36返回的job_id"""
    return api_get("/APIService/relation/getMultiRelationDetail", {"job_id": job_id, "skip": str(skip)})


# ═══ 4. 股权穿透/族谱/受益人 ════════════════════════════════

@mcp.tool(name="get_equity_penetration_report", description="企业族谱穿透信息 — 十二层股权穿透，可自定义比例和层级")
async def get_equity_penetration_report(
    name: str, direction: int,
    level: int = 3, totpercent: float = 0.05, form: int = 0,
) -> str:
    """企业全名, 方向(1向上股东/2向下投资), 层级(1-6), 最小股比, 格式(0JSON/1Excel)"""
    return api_get("/APIService/report/getEntRelationReportByName", {"name": name, "direction": str(direction), "level": str(level), "totpercent": str(totpercent), "form": str(form)})


@mcp.tool(name="get_three_layer_tree", description="三层族谱 — 六层股权穿透（3上+3下）")
async def get_three_layer_tree(name: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/relation/getRelationInfoByName", {"name": name})


@mcp.tool(name="get_six_layer_tree", description="六层族谱 — 十二层股权穿透（6上+6下）")
async def get_six_layer_tree(name: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/v2/relation/getRelationInfoByName", {"name": name})


@mcp.tool(name="get_equity_penetration", description="股权穿透信息（股东穿透）- 不限股比，到自然人/上市公司/政府等停止")
async def get_equity_penetration(name: str) -> str:
    """企业全名/统一社会信用代码"""
    return api_get("/APIService/reportData/getEquityPenetrationByName", {"name": name})


@mcp.tool(name="get_three_layer_shareholders", description="股权穿透（三层股东）- 三层股东向上穿透")
async def get_three_layer_shareholders(name: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/relation/getEquityStructureByName", {"name": name})


@mcp.tool(name="get_ten_layer_shareholders", description="股权穿透（十层股东）- 十层股东向上穿透详细信息")
async def get_ten_layer_shareholders(name: str) -> str:
    """企业全称"""
    return api_get("/APIService/reportData/getReportDataByName", {"name": name})


@mcp.tool(name="get_top_ten_beneficiaries", description="十大受益人")
async def get_top_ten_beneficiaries(keyword: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/benefit/getTopTenBeneficiariesByName", {"keyword": keyword})


@mcp.tool(name="get_actual_beneficiaries", description="实际受益人 — 央行235号/164号文算法")
async def get_actual_beneficiaries(keyword: str) -> str:
    """企业全名或注册号或统一社会信用代码"""
    return api_get("/APIService/benefit/getBeneficiariesByName", {"keyword": keyword})


@mcp.tool(name="get_actual_controller", description="实际控制人 — 根据《公司法》第216条")
async def get_actual_controller(name: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/entChart/getActualOwnerByName", {"name": name})


# ═══ 5. 人员 ═══════════════════════════════════════════════

@mcp.tool(name="get_key_personnel", description="主要人员 — 企业工商主要人员姓名及职位")
async def get_key_personnel(keyword: str, skip: int = 0) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getEmployees", {"keyword": keyword, "skip": str(skip)})


@mcp.tool(name="get_personnel_invest_position", description="主要人员对外投资任职信息 — 法定代表人/董监高的对外投资和任职")
async def get_personnel_invest_position(company: str, name: str) -> str:
    """企业全名, 自然人名"""
    return api_get("/APIService/personInfo/getNPInvestAndPositionByName", {"company": company, "name": name})


# ═══ 6. 变更/年报/社保 ═════════════════════════════════════

@mcp.tool(name="get_change_records", description="变更记录 — 企业工商变更项目/日期/前后内容")
async def get_change_records(keyword: str, skip: int = 0, type_code: int | None = None) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getChangeRecords", make_query(keyword=keyword, skip=str(skip) if skip else None, type_code=str(type_code) if type_code else None))


@mcp.tool(name="get_annual_reports", description="工商年报信息")
async def get_annual_reports(keyword: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/reports/getReportListByName", {"keyword": keyword})


@mcp.tool(name="get_social_security", description="社保信息 — 工商年报披露的社保信息")
async def get_social_security(keyword: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/reports/getSocialSecurityByName", {"keyword": keyword})


@mcp.tool(name="get_equity_changes", description="股权变更（工商公示）")
async def get_equity_changes(name: str, skip: int = 0) -> str:
    """企业全名/统一社会信用代码"""
    return api_get("/APIService/stock/getStockChangesByName", {"name": name, "skip": str(skip)})


@mcp.tool(name="get_enterprise_migration", description="企业迁移情况 — 迁出/迁入地址/省份/城市")
async def get_enterprise_migration(name: str, skip: int = 0) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getEntMoveInfoByName", {"name": name, "skip": str(skip)})


# ═══ 7. 分支机构 ═══════════════════════════════════════════

@mcp.tool(name="get_branches", description="分支机构 — 名称/法定代表人/成立日期/注册资本/状态")
async def get_branches(keyword: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getBranchs", {"keyword": keyword})


@mcp.tool(name="get_head_office", description="分支机构所属总公司核查")
async def get_head_office(name: str) -> str:
    """分支机构全名"""
    return api_get("/APIService/enterprise/getHeadOffice", {"name": name})


# ═══ 8. 联系方式/年报网址 ═══════════════════════════════════

@mcp.tool(name="get_contact_info", description="企业联系方式 — 地址/电话/邮箱")
async def get_contact_info(keyword: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getContactInfo", {"keyword": keyword})


@mcp.tool(name="get_websites", description="企业年报网址 — 网站名称/网址/类型/来源")
async def get_websites(keyword: str, skip: int = 0) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getWebsites", {"keyword": keyword, "skip": str(skip)})


# ═══ 9. 实时查询 ═══════════════════════════════════════════

@mcp.tool(name="get_real_time_info", description="工商实时信息 — 异步触发工商更新，返回jobid")
async def get_real_time_info(keyword: str, province: str | None = None) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/v2/enterprise/getDetailByNameOnline", make_query(keyword=keyword, province=province))


@mcp.tool(name="get_real_time_job_status", description="工商实时JOB状态 — 根据jobid查询结果")
async def get_real_time_job_status(jobid: str) -> str:
    """2.1接口返回的jobid"""
    return api_get("/APIService/v2/enterprise/getJobStatusByJobId", {"jobid": jobid})


# ═══ 10. 验证类 ═══════════════════════════════════════════

@mcp.tool(name="verify_three_elements", description="三要素验证 — 企业名+统一社会信用代码+法定代表人姓名一致性")
async def verify_three_elements(name: str, code: str, oper: str) -> str:
    """企业全名(*) / 统一信用代码 / 法定代表人(-)"""
    return api_get("/APIService/enterprise/checkEntCodeOper", {"name": name, "code": code, "oper": oper})


@mcp.tool(name="verify_four_elements", description="四要素验证 — 企业名+统一信用代码+法定代表人+营业期限")
async def verify_four_elements(name: str, code: str, oper: str, start: str, end: str | None = None) -> str:
    """企业全名, 统一信用代码, 法定代表人, 营业期限始(YYYYMMDD), 营业期限至"""
    return api_get("/APIService/enterprise/checkNameCodeOperPeriod", make_query(name=name, code=code, oper=oper, start=start, end=end))


@mcp.tool(name="verify_name_and_operator", description="企业名+法定代表人名称 二要素验证")
async def verify_name_and_operator(name: str, oper: str) -> str:
    """企业全名, 法定代表人姓名"""
    return api_get("/APIService/enterprise/checkEntOper", {"name": name, "oper": oper})


@mcp.tool(name="verify_name_and_code", description="企业名+统一社会信用代码 二要素验证")
async def verify_name_and_code(name: str, creditNo: str) -> str:
    """企业名称, 统一社会信用代码"""
    return api_get("/APIService/enterprise/checkEntCno", {"name": name, "creditNo": creditNo})


# ═══ 11. 公告 ═════════════════════════════════════════════

@mcp.tool(name="get_capital_reduction_notice", description="减资公告 — 企业减资公告内容/决定日期/公告日期")
async def get_capital_reduction_notice(keyword: str, skip: int = 0) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/notice/getReduceCapitalByName", {"keyword": keyword, "skip": str(skip)})


# ═══ 12. 风险/评分 ═════════════════════════════════════════

@mcp.tool(name="get_credit_score", description="启信分 — 基于公开大数据的综合评分")
async def get_credit_score(name: str, incl_branches: str = "0") -> str:
    """企业名称/统一社会信用代码/注册号"""
    return api_get("/APIService/creditScore/getCreditScore", {"name": name, "incl_branches": incl_branches})


@mcp.tool(name="get_enterprise_risk_scan", description="企业工商风险扫描 — 各维度风险条数统计")
async def get_enterprise_risk_scan(name: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getEnterpriseCountInfo", {"name": name})


@mcp.tool(name="get_enterprise_risk_summary", description="企业关联信息汇总 — 关联企业/受益所有人/税务异常/破产等")
async def get_enterprise_risk_summary(name: str) -> str:
    """企业全名/统一社会信用代码"""
    return api_get("/APIService/enterprise/getRiskCountInfo", {"name": name})


# ═══ 13. 特殊机构 ══════════════════════════════════════════

@mcp.tool(name="get_law_firm_info", description="律所基本信息")
async def get_law_firm_info(keyword: str) -> str:
    """律所全名/注册号/统一社会信用代码"""
    return api_get("/APIService/lawfirm/getLawfirmDetailByName", {"keyword": keyword})


@mcp.tool(name="get_social_organization_info", description="社会组织基本信息")
async def get_social_organization_info(keyword: str) -> str:
    """社会组织全名/注册号/统一社会信用代码"""
    return api_get("/APIService/association/getAssociationDetailByName", {"keyword": keyword})


@mcp.tool(name="get_hk_enterprise_info", description="香港企业信息")
async def get_hk_enterprise_info(keyword: str) -> str:
    """公司全名（中文或英文）"""
    return api_get("/APIService/hkenterprise/getHKDetailByName", {"keyword": keyword})


@mcp.tool(name="get_public_institution_info", description="事业单位基本信息")
async def get_public_institution_info(keyword: str) -> str:
    """事业单位全名/注册号/统一社会信用代码"""
    return api_get("/APIService/institution/getPublicInstitutionByName", {"keyword": keyword})


@mcp.tool(name="get_hospital_info", description="医院信息")
async def get_hospital_info(keyword: str) -> str:
    """医院全名/注册号/统一社会信用代码"""
    return api_get("/APIService/hospital/getHospitalDetailByName", {"keyword": keyword})


@mcp.tool(name="get_foundation_info", description="基金会基本信息")
async def get_foundation_info(keyword: str) -> str:
    """基金会全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getFoundationByName", {"keyword": keyword})


# ═══ 14. 小微企业 ═════════════════════════════════════════

@mcp.tool(name="get_micro_enterprise_info", description="小微企业信息")
async def get_micro_enterprise_info(keyword: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/micro/getMicroEntInfoByName", {"keyword": keyword})


@mcp.tool(name="create_micro_enterprise_job", description="小微企业-JOB申请 — 异步返回jobid")
async def create_micro_enterprise_job(keyword: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/micro/getMicroEntByName", {"keyword": keyword})


@mcp.tool(name="get_micro_enterprise_result", description="小微企业-详情数据 — 根据jobid获取结果")
async def get_micro_enterprise_result(jobid: str) -> str:
    """60.1返回的jobid"""
    return api_get("/APIService/micro/getMicroEntJobResult", {"jobid": jobid})


# ═══ 15. 地理/周边 ════════════════════════════════════════

@mcp.tool(name="get_nearby_enterprises", description="附近企业查询")
async def get_nearby_enterprises(keyword: str, distance: int, skip: int = 0) -> str:
    """企业全名, 搜索范围(KM)"""
    return api_get("/APIService/nearbyEnterprises/getNearbyEnterpriseByName", {"keyword": keyword, "distance": str(distance), "skip": str(skip)})


@mcp.tool(name="get_nearby_count", description="周边企业总数 — 根据坐标查询")
async def get_nearby_count(longitude: float, latitude: float, radius: int) -> str:
    """经度, 纬度, 半径(1/3/5/10 KM)"""
    return api_post("/APIService/enterprise/getStatisticsByPoint", {"longitude": longitude, "latitude": latitude, "radius": radius})


@mcp.tool(name="get_nearby_details", description="周边企业详情 — 根据坐标获取附近企业列表")
async def get_nearby_details(longitude: float, latitude: float, radius: int, skip: int = 0) -> str:
    """经度, 纬度, 半径"""
    return api_post("/APIService/enterprise/getEnterprisesByPoint", {"longitude": longitude, "latitude": latitude, "radius": radius, "skip": str(skip)})


@mcp.tool(name="get_enterprise_coordinates", description="企业坐标 — 高德/百度地图经纬度")
async def get_enterprise_coordinates(name: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/enterprise/getLongitudeAndLatitude", {"name": name})


@mcp.tool(name="get_enterprises_by_phone", description="同电话企业 — 根据电话查相关企业")
async def get_enterprises_by_phone(phone: str) -> str:
    """联系电话"""
    return api_get("/APIService/enterprise/getPseronEntRelation", {"phone": phone})


@mcp.tool(name="get_above_scale_enterprise", description="规上企业信息")
async def get_above_scale_enterprise(keyword: str) -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/techinnovate/getAboveEnt", {"keyword": keyword})


@mcp.tool(name="get_new_enterprises", description="新增企业 — 根据省份代码查询新增企业")
async def get_new_enterprises(province_code: str, **kw) -> str:
    """省份代码"""
    return api_get("/APIService/enterprise/getNewEnt", make_query(province_code=province_code, **kw))


# ═══ 16. 综合报告 ═════════════════════════════════════════

@mcp.tool(name="get_full_enterprise_report", description="企业基础工商信息报告 — 工商综合信息（照面/股东/人员/变更/经营异常等）")
async def get_full_enterprise_report(keyword: str, is_history: str = "0") -> str:
    """企业全名/注册号/统一社会信用代码"""
    return api_get("/APIService/reportData/getAllEntInfoByName", {"keyword": keyword, "is_history": is_history})



# ═══ 17. 搜索查询 ══════════════════════════════════════════════

@mcp.tool(name="advanced_search", description="企业高级搜索 — 根据企业名称关键字获取企业列表")
async def advanced_search(keyword: str, skip: int = 0) -> str:
    """企业高级搜索 — 根据企业名称关键字获取企业列表"""
    return api_get("/APIService/search/advanceSearchNew", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="fuzzy_search", description="企业模糊搜索 — 根据关键词对企业进行模糊搜索")
async def fuzzy_search(keyword: str, skip: int = 0) -> str:
    """企业模糊搜索 — 根据关键词对企业进行模糊搜索"""
    return api_get("/APIService/v2/search/advSearch", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="search_trademark", description="商标信息搜索 — 根据商标名称/注册号/申请人搜索商标信息")
async def search_trademark(keyword: str, skip: int = 0) -> str:
    """商标信息搜索 — 根据商标名称/注册号/申请人搜索商标信息"""
    return api_get("/APIService/trademark/getTrademarkByKeyword", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="search_bidding", description="招投标信息搜索 — 搜索招投标ID、标题、招标单位、中标单位等")
async def search_bidding(keyword: str, skip: int = 0) -> str:
    """招投标信息搜索 — 搜索招投标ID、标题、招标单位、中标单位等"""
    return api_get("/APIService/operation/getBiddingListBySearch", make_query(keyword=keyword, skip=str(skip) if skip else None))


# ═══ 17. 司法风险 ══════════════════════════════════════════════

@mcp.tool(name="get_case_filing_list", description="立案信息 — 企业立案信息，包括立案ID、开庭日期、案件状态、承办人、当事人等")
async def get_case_filing_list(keyword: str, skip: int = 0) -> str:
    """立案信息 — 企业立案信息，包括立案ID、开庭日期、案件状态、承办人、当事人等"""
    return api_get("/APIService/case/getCaseDetailListByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_being_executed_list", description="被执行企业 — 企业被执行信息，包括执行ID、执行状态、执行金额、立案日期等")
async def get_being_executed_list(name: str, skip: int = 0) -> str:
    """被执行企业 — 企业被执行信息，包括执行ID、执行状态、执行金额、立案日期等"""
    return api_get("/APIService/execution/getExecutedpersonListByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_dishonest_executed_list", description="失信被执行企业 — 企业失信信息，包括执行法院、法定代表人、被执行人履行情况等")
async def get_dishonest_executed_list(keyword: str, skip: int = 0) -> str:
    """失信被执行企业 — 企业失信信息，包括执行法院、法定代表人、被执行人履行情况等"""
    return api_get("/APIService/execution/getExecutionListByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_court_hearing_list", description="开庭公告 — 企业开庭公告，包括法庭、开庭日期、案号、案由、原告、被告等")
async def get_court_hearing_list(name: str, skip: int = 0) -> str:
    """开庭公告 — 企业开庭公告，包括法庭、开庭日期、案号、案由、原告、被告等"""
    return api_get("/APIService/courtnotice/getCourtNoticeByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_court_announcement_list", description="法院公告 — 企业法院公告，包括公告类型、内容、发布日期、当事人等")
async def get_court_announcement_list(name: str, skip: int = 0) -> str:
    """法院公告 — 企业法院公告，包括公告类型、内容、发布日期、当事人等"""
    return api_get("/APIService/notice/getNoticeListByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_service_announcement", description="送达公告 — 包括法庭、案号、案由、详情等")
async def get_service_announcement(keyword: str, skip: int = 0) -> str:
    """送达公告 — 包括法庭、案号、案由、详情等"""
    return api_get("/APIService/notice/getServiceCheckByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_bribery_judgments", description="行贿违法 — 企业行贿违法类裁判文书，包括判决基本信息及链接等")
async def get_bribery_judgments(name: str, skip: int = 0) -> str:
    """行贿违法 — 企业行贿违法类裁判文书，包括判决基本信息及链接等"""
    return api_get("/APIService/lawsuit/getBriberyLawsuitByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_consumption_restrictions", description="限制高消费 — 企业限制高消费信息，包括限制高消费企业信息、案由等")
async def get_consumption_restrictions(keyword: str, skip: int = 0) -> str:
    """限制高消费 — 企业限制高消费信息，包括限制高消费企业信息、案由等"""
    return api_get("/APIService/risk/getRestrictedConsumer", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_judicial_auctions", description="司法拍卖 — 企业司法拍卖信息，包括拍品介绍、起拍价、拍卖日期等")
async def get_judicial_auctions(name: str, skip: int = 0) -> str:
    """司法拍卖 — 企业司法拍卖信息，包括拍品介绍、起拍价、拍卖日期等"""
    return api_get("/APIService/auction/getAuctionsListByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_bankruptcy_cases", description="破产案件 — 破产案件信息，包括案件号、案件类型、申请人、被申请人及管理机构等")
async def get_bankruptcy_cases(name: str, skip: int = 0) -> str:
    """破产案件 — 破产案件信息，包括案件号、案件类型、申请人、被申请人及管理机构等"""
    return api_get("/APIService/bankruptcy/getBankruptcyListByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_bankruptcy_notices", description="破产公告 — 破产公告信息，包括公告标题、公告类型、公开时间及正文等")
async def get_bankruptcy_notices(keyword: str, skip: int = 0) -> str:
    """破产公告 — 破产公告信息，包括公告标题、公告类型、公开时间及正文等"""
    return api_get("/APIService/bankruptcy/getBankruptcyNoticesByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_price_evaluation", description="询价评估 — 查询企业是否存在询价评估情况，包括案号、标的物、询价结果等")
async def get_price_evaluation(keyword: str, skip: int = 0) -> str:
    """询价评估 — 查询企业是否存在询价评估情况，包括案号、标的物、询价结果等"""
    return api_get("/APIService/judicial/getPriceEvaluationByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


# ═══ 18. 经营风险 ══════════════════════════════════════════════

@mcp.tool(name="get_administrative_penalties", description="行政处罚 — 企业行政处罚信息，包括处罚类型、内容、时间及决定机关等")
async def get_administrative_penalties(keyword: str, skip: int = 0) -> str:
    """行政处罚 — 企业行政处罚信息，包括处罚类型、内容、时间及决定机关等"""
    return api_get("/APIService/v2/adminPunish/getAdminPunishByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_enforcement_closure_cases", description="终本案件 — 企业终本案件信息，包括执行案号、终本日期、执行标的、未履行金额等")
async def get_enforcement_closure_cases(keyword: str, skip: int = 0) -> str:
    """终本案件 — 企业终本案件信息，包括执行案号、终本日期、执行标的、未履行金额等"""
    return api_get("/APIService/risk/getTerminationCaseList", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_chattel_mortgage", description="动产抵押 — 包括被担保债券数额种类、抵押物相关描述等")
async def get_chattel_mortgage(name: str, skip: int = 0) -> str:
    """动产抵押 — 包括被担保债券数额种类、抵押物相关描述等"""
    return api_get("/APIService/v2/mortgage/getMortgagesByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_equity_pledge", description="股权出质 — 企业股权出质信息，包括出质人、出质股权、质权人等")
async def get_equity_pledge(name: str, skip: int = 0) -> str:
    """股权出质 — 企业股权出质信息，包括出质人、出质股权、质权人等"""
    return api_get("/APIService/v2/equityPledge/getEquityQualitiesByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_equity_freeze", description="股权冻结 — 企业股权冻结信息，包括被执行人相关信息以及冻结金额、原因等")
async def get_equity_freeze(name: str, skip: int = 0) -> str:
    """股权冻结 — 企业股权冻结信息，包括被执行人相关信息以及冻结金额、原因等"""
    return api_get("/APIService/v2/judicialFreeze/getJudicialFreezeByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_business_anomalies", description="经营异常 — 企业经营异常信息，企业被列入或移出的原因和时间，以及做出决定的机关等")
async def get_business_anomalies(keyword: str, skip: int = 0) -> str:
    """经营异常 — 企业经营异常信息，企业被列入或移出的原因和时间，以及做出决定的机关等"""
    return api_get("/APIService/enterprise/getAbnormals", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_serious_violations", description="严重违法 — 企业工商严重违法信息，企业被列入或移出的原因和时间等")
async def get_serious_violations(name: str, skip: int = 0) -> str:
    """严重违法 — 企业工商严重违法信息，企业被列入或移出的原因和时间等"""
    return api_get("/APIService/enterprise/getSeriousIllegalByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_tax_arrears", description="欠税信息 — 企业欠税信息，包括纳税人类型、纳税人识别号、欠税税种、余额等")
async def get_tax_arrears(name: str, skip: int = 0) -> str:
    """欠税信息 — 企业欠税信息，包括纳税人类型、纳税人识别号、欠税税种、余额等"""
    return api_get("/APIService/overduetax/getOverDueTaxByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_tax_arrears_summary", description="欠税合计 — 根据企业全名/注册号/统一社会信用代码获得企业欠税合计金额")
async def get_tax_arrears_summary(keyword: str, skip: int = 0) -> str:
    """欠税合计 — 根据企业全名/注册号/统一社会信用代码获得企业欠税合计金额"""
    return api_get("/APIService/overduetax/getOverDueTaxStat", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_irregular_taxpayer", description="非正常户 — 企业非正常户信息，包括纳税人识别号、认定原因、欠税种类及金额等")
async def get_irregular_taxpayer(keyword: str, skip: int = 0) -> str:
    """非正常户 — 企业非正常户信息，包括纳税人识别号、认定原因、欠税种类及金额等"""
    return api_get("/APIService/risk/getAbnormalEnterpriseByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_major_tax_violations", description="重大税收违法 — 企业重大税收违法信息，包括案件性质、主要违法事实等")
async def get_major_tax_violations(keyword: str, skip: int = 0) -> str:
    """重大税收违法 — 企业重大税收违法信息，包括案件性质、主要违法事实等"""
    return api_get("/APIService/overduetax/getTaxCaseByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_product_complaints", description="产品投诉情况 — 投诉对象、问题、详情、进度、涉及金额等信息")
async def get_product_complaints(name: str, skip: int = 0) -> str:
    """产品投诉情况 — 投诉对象、问题、详情、进度、涉及金额等信息"""
    return api_get("/APIService/product/getProComplaint", make_query(name=name, skip=str(skip) if skip else None))


# ═══ 19. 经营信息 ══════════════════════════════════════════════

@mcp.tool(name="get_administrative_licenses", description="行政许可 — 工商行政许可信息，包括许可文件编号、名称、机关及期限等")
async def get_administrative_licenses(name: str, skip: int = 0) -> str:
    """行政许可 — 工商行政许可信息，包括许可文件编号、名称、机关及期限等"""
    return api_get("/APIService/administrativeLicense/getAdministrativeLicenseListByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_inspection_records", description="抽查检查 — 企业抽查检查信息，包括检查编号以及实施机关等")
async def get_inspection_records(name: str, skip: int = 0) -> str:
    """抽查检查 — 企业抽查检查信息，包括检查编号以及实施机关等"""
    return api_get("/APIService/checkup/getCheckupListByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_tax_credit_grade", description="纳税A级 — 企业历年A级纳税人记录，包括企业信用年份及信用等级等")
async def get_tax_credit_grade(keyword: str, skip: int = 0) -> str:
    """纳税A级 — 企业历年A级纳税人记录，包括企业信用年份及信用等级等"""
    return api_get("/APIService/creditgrade/getCreditGradeByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_bidding_list", description="招投标列表 — 企业招投标列表，包括招投标ID、标题、招标单位、中标单位等")
async def get_bidding_list(name: str, skip: int = 0) -> str:
    """招投标列表 — 企业招投标列表，包括招投标ID、标题、招标单位、中标单位等"""
    return api_get("/APIService/operation/getBiddingListByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_bidding_detail", description="招投标详情 — 招投标详情，中标单位列表，以及具体招标信息正文及来源等")
async def get_bidding_detail(keyword: str, skip: int = 0) -> str:
    """招投标详情 — 招投标详情，中标单位列表，以及具体招标信息正文及来源等"""
    return api_get("/APIService/operation/getBiddingDetail", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_recruitment_list", description="招聘信息 — 企业招聘信息，包括招聘企业名称、职位、薪水、职位描述等")
async def get_recruitment_list(name: str, skip: int = 0) -> str:
    """招聘信息 — 企业招聘信息，包括招聘企业名称、职位、薪水、职位描述等"""
    return api_get("/APIService/v2/recruitment/getRecruitmentListByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_customs_enterprise", description="进出口企业查询 — 企业海关进出口企业登记信息，包括海关编号、注册海关、经营类别等")
async def get_customs_enterprise(name: str, skip: int = 0) -> str:
    """进出口企业查询 — 企业海关进出口企业登记信息，包括海关编号、注册海关、经营类别等"""
    return api_get("/APIService/customs/getCustomsListByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_simplified_cancellation", description="简易注销 — 简易注销信息列表，包括登记机关、异议信息、简易注销结果等")
async def get_simplified_cancellation(name: str, skip: int = 0) -> str:
    """简易注销 — 简易注销信息列表，包括登记机关、异议信息、简易注销结果等"""
    return api_get("/APIService/logout/getLogoutInfo", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_entity_credit_rating", description="主体信用评级 — 企业历年主体信用评级类型、信用等级、评级机构等")
async def get_entity_credit_rating(name: str, skip: int = 0) -> str:
    """主体信用评级 — 企业历年主体信用评级类型、信用等级、评级机构等"""
    return api_get("/APIService/credit/getEntCreditRating", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_bond_credit_rating", description="债券信用评级 — 企业历年债券评级类型、信用等级、评级机构等")
async def get_bond_credit_rating(name: str, skip: int = 0) -> str:
    """债券信用评级 — 企业历年债券评级类型、信用等级、评级机构等"""
    return api_get("/APIService/credit/getBondCreditRating", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_dual_random_inspections", description="双随机抽查 — 包括抽查名称、抽查类型、抽查机关等")
async def get_dual_random_inspections(name: str, skip: int = 0) -> str:
    """双随机抽查 — 包括抽查名称、抽查类型、抽查机关等"""
    return api_get("/APIService/checkup/getDoubleCheckupsByName", make_query(name=name, skip=str(skip) if skip else None))


# ═══ 20. 知识产权 ══════════════════════════════════════════════

@mcp.tool(name="get_ip_statistics", description="知识产权统计 — 根据企业名称/统一社会信用代码/注册号获取知识产权统计信息")
async def get_ip_statistics(name: str, skip: int = 0) -> str:
    """知识产权统计 — 根据企业名称/统一社会信用代码/注册号获取知识产权统计信息"""
    return api_get("/APIService/patent/getIntPropertyStat", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_trademark_list", description="商标列表 — 企业商标列表信息，包括商标名称、企业名称、状态等")
async def get_trademark_list(name: str, skip: int = 0) -> str:
    """商标列表 — 企业商标列表信息，包括商标名称、企业名称、状态等"""
    return api_get("/APIService/trademark/getTrademarkByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_trademark_detail", description="商标详细 — 企业商标详细信息，包括商标名称、申请时间、申请人、流程状态等")
async def get_trademark_detail(keyword: str, skip: int = 0) -> str:
    """商标详细 — 企业商标详细信息，包括商标名称、申请时间、申请人、流程状态等"""
    return api_get("/APIService/trademark/getTrademarkDetailByNumber", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_patent_list", description="专利列表 — 企业专利列表信息，包括专利ID、名称、类型等")
async def get_patent_list(name: str, skip: int = 0) -> str:
    """专利列表 — 企业专利列表信息，包括专利ID、名称、类型等"""
    return api_get("/APIService/patent/getPatentListByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_patent_detail", description="专利详细 — 企业专利详细信息，包括专利ID、名称、类型等基本信息及详细内容")
async def get_patent_detail(keyword: str, skip: int = 0) -> str:
    """专利详细 — 企业专利详细信息，包括专利ID、名称、类型等基本信息及详细内容"""
    return api_get("/APIService/patent/getPatentDetailByNumber", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_telecom_license", description="电信许可 — 根据企业全名/注册号/统一社会信用代码获得企业电信许可相关信息")
async def get_telecom_license(name: str, skip: int = 0) -> str:
    """电信许可 — 根据企业全名/注册号/统一社会信用代码获得企业电信许可相关信息"""
    return api_get("/APIService/cert/getTelecLicByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_financial_qualifications", description="金融资质 — 根据企业全名/注册号/统一社会信用代码获得金融资质相关信息")
async def get_financial_qualifications(name: str, skip: int = 0) -> str:
    """金融资质 — 根据企业全名/注册号/统一社会信用代码获得金融资质相关信息"""
    return api_get("/APIService/cert/getFinCertByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_copyright_list", description="著作权 — 企业作品著作权信息，包括著作ID、名称、类型、登记批准时间等")
async def get_copyright_list(name: str, skip: int = 0) -> str:
    """著作权 — 企业作品著作权信息，包括著作ID、名称、类型、登记批准时间等"""
    return api_get("/APIService/copyright/getCopyrightByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_software_copyright_list", description="软件著作权 — 企业软件著作权信息，包括软件著作ID、名称、类型、登记批准时间等")
async def get_software_copyright_list(name: str, skip: int = 0) -> str:
    """软件著作权 — 企业软件著作权信息，包括软件著作ID、名称、类型、登记批准时间等"""
    return api_get("/APIService/copyright/getCopyrightSoftByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_domain_list", description="域名信息 — 企业备案域名信息，包括网站名称、域名等")
async def get_domain_list(name: str, skip: int = 0) -> str:
    """域名信息 — 企业备案域名信息，包括网站名称、域名等"""
    return api_get("/APIService/domain/getDomainByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_qualification_list", description="资质信息 — 企业资质证书信息，包括资质证书类型、证书编号、发证截止日期等")
async def get_qualification_list(name: str, skip: int = 0) -> str:
    """资质信息 — 企业资质证书信息，包括资质证书类型、证书编号、发证截止日期等"""
    return api_get("/APIService/certificate/getCertificateByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_qualification_detail", description="资质证书详情 — 通过证书编号或者kind_id获取资质证书详情")
async def get_qualification_detail(keyword: str, skip: int = 0) -> str:
    """资质证书详情 — 通过证书编号或者kind_id获取资质证书详情"""
    return api_get("/APIService/certificate/getCertificateDetailByKind", make_query(keyword=keyword, skip=str(skip) if skip else None))


# ═══ 21. 企业评分 ══════════════════════════════════════════════

@mcp.tool(name="get_credit_score_detail", description="启信分详情 — 包含企业资本背景、企业规模、成长性、知识产权、经营质量、风险状况的行业排名信息")
async def get_credit_score_detail(name: str, skip: int = 0) -> str:
    """启信分详情 — 包含企业资本背景、企业规模、成长性、知识产权、经营质量、风险状况的行业排名信息"""
    return api_get("/APIService/creditScore/getCreditScoreDetail", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_credit_score_trend", description="启信分波动 — 获取启信分波动变化")
async def get_credit_score_trend(name: str, skip: int = 0) -> str:
    """启信分波动 — 获取启信分波动变化"""
    return api_get("/APIService/creditScore/getCreditScoreChange", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_shell_company_index", description="企业空壳指数 — 识别套牌公司、僵尸企业、皮包公司等非正常经营企业的指数")
async def get_shell_company_index(name: str, skip: int = 0) -> str:
    """企业空壳指数 — 识别套牌公司、僵尸企业、皮包公司等非正常经营企业的指数"""
    return api_get("/APIService/shellEnt/getShellEntInfoByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_shell_company_detail", description="企业空壳指数详情 — 空壳指数详细分析，包括经营场所、资产形态、企业人员、经营活动等维度")
async def get_shell_company_detail(name: str, skip: int = 0) -> str:
    """企业空壳指数详情 — 空壳指数详细分析，包括经营场所、资产形态、企业人员、经营活动等维度"""
    return api_get("/APIService/shellEnt/getShellEntDetailInfoByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_judicial_risk_score", description="司法风险评分 — 根据企业全名/注册号/统一社会信用代码获得司法风险评分")
async def get_judicial_risk_score(name: str, skip: int = 0) -> str:
    """司法风险评分 — 根据企业全名/注册号/统一社会信用代码获得司法风险评分"""
    return api_get("/APIService/score/getEntJusticeScore", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_judicial_risk_score_detail", description="司法风险评分详情 — 根据企业全名/注册号/统一社会信用代码获得司法风险评分详情")
async def get_judicial_risk_score_detail(name: str, skip: int = 0) -> str:
    """司法风险评分详情 — 根据企业全名/注册号/统一社会信用代码获得司法风险评分详情"""
    return api_get("/APIService/score/getEntJusticeScoreDetail", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_innovation_score", description="企业科技创新能力评分 — 根据企业名称、注册号、统一社会信用代码获取科技创新能力评分")
async def get_innovation_score(name: str, skip: int = 0) -> str:
    """企业科技创新能力评分 — 根据企业名称、注册号、统一社会信用代码获取科技创新能力评分"""
    return api_get("/APIService/techinnovate/getTechIndexScoreRank", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_innovation_score_detail", description="企业科技创新能力评分详情 — 企业科创力得分详情")
async def get_innovation_score_detail(name: str, skip: int = 0) -> str:
    """企业科技创新能力评分详情 — 企业科创力得分详情"""
    return api_get("/APIService/techinnovate/getTechInnovateIndexScoreByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_innovation_score_indicators", description="企业科技创新能力评分模型指标 — IPC分类数量、PCT申请量、产学研合作等科创详情")
async def get_innovation_score_indicators(name: str, skip: int = 0) -> str:
    """企业科技创新能力评分模型指标 — IPC分类数量、PCT申请量、产学研合作等科创详情"""
    return api_get("/APIService/techinnovate/getTechInnovateScoreDetail", make_query(name=name, skip=str(skip) if skip else None))


# ═══ 22. 企业标签 ══════════════════════════════════════════════

@mcp.tool(name="get_hightech_enterprise", description="科技型企业 — 科技型企业类型、发布单位的行政类别、认定年份、认定状态等")
async def get_hightech_enterprise(name: str, skip: int = 0) -> str:
    """科技型企业 — 科技型企业类型、发布单位的行政类别、认定年份、认定状态等"""
    return api_get("/APIService/enterprise/getTechEnt", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_startup_characteristics", description="企业特点（初创企业） — 根据企业名称返回该企业特点，如是否为初创企业")
async def get_startup_characteristics(name: str, skip: int = 0) -> str:
    """企业特点（初创企业） — 根据企业名称返回该企业特点，如是否为初创企业"""
    return api_get("/APIService/enterprise/getCharacteristicTags", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_enterprise_labels", description="企业信息标签 — 通过企业名称获取企业信息标签")
async def get_enterprise_labels(keyword: str, skip: int = 0) -> str:
    """企业信息标签 — 通过企业名称获取企业信息标签"""
    return api_get("/APIService/enterprise/getEnterpriseInfolabels", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_business_portrait", description="主营业务 — 企业主营业务画像")
async def get_business_portrait(name: str, skip: int = 0) -> str:
    """主营业务 — 企业主营业务画像"""
    return api_get("/APIService/enterprise/getEntPortraitByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_regional_designation", description="地区认定标签 — 用于金融机构涉农业务中企业所属地区的判定")
async def get_regional_designation(keyword: str, skip: int = 0) -> str:
    """地区认定标签 — 用于金融机构涉农业务中企业所属地区的判定"""
    return api_get("/APIService/enterprise/getSupervisionTypeByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


# ═══ 23. 企业发展 ══════════════════════════════════════════════

@mcp.tool(name="get_core_team", description="核心团队 — 企业核心团队信息，包括姓名、职位、教育经历和工作经历等")
async def get_core_team(name: str, skip: int = 0) -> str:
    """核心团队 — 企业核心团队信息，包括姓名、职位、教育经历和工作经历等"""
    return api_get("/APIService/baseInfo/getCoreMember", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_products", description="产品信息 — 企业产品信息，包括项目名称、logo链接、项目地址、运营状态等")
async def get_products(name: str, skip: int = 0) -> str:
    """产品信息 — 企业产品信息，包括项目名称、logo链接、项目地址、运营状态等"""
    return api_get("/APIService/baseInfo/getProject", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_competitors", description="竞品信息 — 企业竞品信息，包括竞品名称、所属企业、竞品简介等")
async def get_competitors(name: str, skip: int = 0) -> str:
    """竞品信息 — 企业竞品信息，包括竞品名称、所属企业、竞品简介等"""
    return api_get("/APIService/enterprise/getEntCompetitionByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_investment_portfolio", description="投资机构与投资项目查询 — 通过机构名称查询投资机构的对外投资项目信息（主要支持风投）")
async def get_investment_portfolio(name: str, skip: int = 0) -> str:
    """投资机构与投资项目查询 — 通过机构名称查询投资机构的对外投资项目信息（主要支持风投）"""
    return api_get("/APIService/institution/investInfo", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_industry_chain_position", description="企业所属产业链环节 — 企业所属产业链详情信息")
async def get_industry_chain_position(name: str, skip: int = 0) -> str:
    """企业所属产业链环节 — 企业所属产业链详情信息"""
    return api_get("/APIService/KI/getIndProByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_strategic_emerging_industry", description="战略新兴产业 — 根据企业名称获取所在战略新兴产业")
async def get_strategic_emerging_industry(keyword: str, skip: int = 0) -> str:
    """战略新兴产业 — 根据企业名称获取所在战略新兴产业"""
    return api_get("/APIService/enterprise/getEmergingIndustryByKeyword", make_query(keyword=keyword, skip=str(skip) if skip else None))


# ═══ 24. 集团信息 ══════════════════════════════════════════════

@mcp.tool(name="get_group_investment", description="集团对外投资信息 — 包括集团名称、对外投资企业数、对外投资企业信息等")
async def get_group_investment(name: str, skip: int = 0) -> str:
    """集团对外投资信息 — 包括集团名称、对外投资企业数、对外投资企业信息等"""
    return api_get("/APIService/group/getGroupInvestInfoByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_group_investors", description="集团投资方信息 — 包括集团名称、投资方总数、投资方名称、类型、总投资金额等")
async def get_group_investors(name: str, skip: int = 0) -> str:
    """集团投资方信息 — 包括集团名称、投资方总数、投资方名称、类型、总投资金额等"""
    return api_get("/APIService/group/getGroupPartnerInfoByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_group_graph", description="集团图谱 — 根据企业名称获取企业所属集团图谱信息，包括集团内成员名称、类型等")
async def get_group_graph(name: str, skip: int = 0) -> str:
    """集团图谱 — 根据企业名称获取企业所属集团图谱信息，包括集团内成员名称、类型等"""
    return api_get("/APIService/group/getGroupRelationInfoByName", make_query(name=name, skip=str(skip) if skip else None))


# ═══ 25. 证券信息 ══════════════════════════════════════════════

@mcp.tool(name="get_stock_info", description="股票信息 — 企业股票信息，包括股票简称、股票代码、交易市场、上市状态等")
async def get_stock_info(name: str, skip: int = 0) -> str:
    """股票信息 — 企业股票信息，包括股票简称、股票代码、交易市场、上市状态等"""
    return api_get("/APIService/stock/getStockInfoByName", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_listed_company_profile", description="上市公司概况 — 上市企业概况信息")
async def get_listed_company_profile(name: str, skip: int = 0) -> str:
    """上市公司概况 — 上市企业概况信息"""
    return api_get("/APIService/qc/getEntProfile", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_shareholder_count", description="股东人数 — 上市企业股东人数信息，包括前十大股东持股合计、股东总户数等")
async def get_shareholder_count(name: str, skip: int = 0) -> str:
    """股东人数 — 上市企业股东人数信息，包括前十大股东持股合计、股东总户数等"""
    return api_get("/APIService/qc/getShareholderNumList", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_top_ten_shareholders", description="十大股东 — 上市企业十大股东信息，包括股东名称、股份类型、持股比例等")
async def get_top_ten_shareholders(name: str, skip: int = 0) -> str:
    """十大股东 — 上市企业十大股东信息，包括股东名称、股份类型、持股比例等"""
    return api_get("/APIService/qc/getTopTenPartnerList", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_top_ten_circulating_shareholders", description="十大流通股东 — 上市企业十大流通股东信息")
async def get_top_ten_circulating_shareholders(name: str, skip: int = 0) -> str:
    """十大流通股东 — 上市企业十大流通股东信息"""
    return api_get("/APIService/qc/getTopTenCirPartnerList", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_listed_company_executives", description="上市公司高管 — 上市企业高管信息，包括姓名、出生日期、性别、薪资、简历等")
async def get_listed_company_executives(name: str, skip: int = 0) -> str:
    """上市公司高管 — 上市企业高管信息，包括姓名、出生日期、性别、薪资、简历等"""
    return api_get("/APIService/qc/getEmployeeList", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_share_structure", description="股本结构 — 上市企业股本结构信息，总股本、已流通股份、已流通股份占比等")
async def get_share_structure(name: str, skip: int = 0) -> str:
    """股本结构 — 上市企业股本结构信息，总股本、已流通股份、已流通股份占比等"""
    return api_get("/APIService/qc/getStockStruct", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_share_changes", description="股本变动 — 上市企业股本变动信息，包括股本变动原因及限售持股等")
async def get_share_changes(name: str, skip: int = 0) -> str:
    """股本变动 — 上市企业股本变动信息，包括股本变动原因及限售持股等"""
    return api_get("/APIService/qc/getStockChangeList", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_top_ten_shareholder_changes", description="十大股东持股变动 — 上市企业十大股东持股变动信息")
async def get_top_ten_shareholder_changes(name: str, skip: int = 0) -> str:
    """十大股东持股变动 — 上市企业十大股东持股变动信息"""
    return api_get("/APIService/qc/getTop10PartnerChangeList", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_listed_company_announcements", description="上市公司公告 — 上市企业公告信息，包括定期报告、财务报告、融资公告等")
async def get_listed_company_announcements(name: str, skip: int = 0) -> str:
    """上市公司公告 — 上市企业公告信息，包括定期报告、财务报告、融资公告等"""
    return api_get("/APIService/qc/getANList", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_employee_composition", description="上市公司员工构成 — 上市企业员工构成信息，包括职工总数、各岗位人员、不同学历人员等")
async def get_employee_composition(name: str, skip: int = 0) -> str:
    """上市公司员工构成 — 上市企业员工构成信息，包括职工总数、各岗位人员、不同学历人员等"""
    return api_get("/APIService/qc/getWorksNoList", make_query(name=name, skip=str(skip) if skip else None))


@mcp.tool(name="get_external_guarantees", description="对外担保 — 上市企业对外担保信息，包括担保方、被担保方基本信息等")
async def get_external_guarantees(name: str, skip: int = 0) -> str:
    """对外担保 — 上市企业对外担保信息，包括担保方、被担保方基本信息等"""
    return api_get("/APIService/qc/getGuaranteeList", make_query(name=name, skip=str(skip) if skip else None))


# ═══ 26. 地产建筑 ══════════════════════════════════════════════

@mcp.tool(name="get_construction_qualification", description="建筑企业资质查询 — 包括资质证书号、资质类别、资质名称、资质范围等")
async def get_construction_qualification(keyword: str, skip: int = 0) -> str:
    """建筑企业资质查询 — 包括资质证书号、资质类别、资质名称、资质范围等"""
    return api_get("/APIService/constructEnterprise/getConstructEntQualifyByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_construction_misconduct", description="建筑企业不良行为 — 包括诚信记录编号、处罚类型、处罚结果、处罚事由等")
async def get_construction_misconduct(keyword: str, skip: int = 0) -> str:
    """建筑企业不良行为 — 包括诚信记录编号、处罚类型、处罚结果、处罚事由等"""
    return api_get("/APIService/constructEnterprise/getConstructEntBadBehaviorByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_construction_blacklist", description="建筑企业黑名单 — 包括黑名单记录编号、认定依据、认定部门、列入日期、移除日期等")
async def get_construction_blacklist(keyword: str, skip: int = 0) -> str:
    """建筑企业黑名单 — 包括黑名单记录编号、认定依据、认定部门、列入日期、移除日期等"""
    return api_get("/APIService/constructEnterprise/getConstructEntBlacklistByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_construction_plan_permit", description="建设工程规划许可证 — 包括建设单位、证书编号、项目名称、核发日期等")
async def get_construction_plan_permit(keyword: str, skip: int = 0) -> str:
    """建设工程规划许可证 — 包括建设单位、证书编号、项目名称、核发日期等"""
    return api_get("/APIService/realestate/getPlanEngineerLicenseListByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_completion_acceptance", description="工程竣工验收信息 — 包括建设单位、项目名称、施工单位、备案部门、竣工备案日期等")
async def get_completion_acceptance(keyword: str, skip: int = 0) -> str:
    """工程竣工验收信息 — 包括建设单位、项目名称、施工单位、备案部门、竣工备案日期等"""
    return api_get("/APIService/realestate/getEngineerCompleteCheckListByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_idle_land", description="土地闲置信息 — 包括土地使用权人、土地位置、宗地面积、闲置原因等")
async def get_idle_land(keyword: str, skip: int = 0) -> str:
    """土地闲置信息 — 包括土地使用权人、土地位置、宗地面积、闲置原因等"""
    return api_get("/APIService/realestate/getLandIdleListByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_land_use_plan_permit", description="建设用地规划许可证 — 包括用地单位、用地位置、用地面积、核发日期等")
async def get_land_use_plan_permit(keyword: str, skip: int = 0) -> str:
    """建设用地规划许可证 — 包括用地单位、用地位置、用地面积、核发日期等"""
    return api_get("/APIService/realestate/getPlanLandLicenseListByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_presale_projects", description="预售项目信息 — 包括开发企业、坐落位置、准许销售面积等")
async def get_presale_projects(keyword: str, skip: int = 0) -> str:
    """预售项目信息 — 包括开发企业、坐落位置、准许销售面积等"""
    return api_get("/APIService/realestate/getHousePresellListByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_land_transactions", description="土地成交信息 — 包括受让方名称、土地位置、出让年限、宗地面积、土地成交价等")
async def get_land_transactions(keyword: str, skip: int = 0) -> str:
    """土地成交信息 — 包括受让方名称、土地位置、出让年限、宗地面积、土地成交价等"""
    return api_get("/APIService/realestate/getLandDealListByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_land_allocations", description="土地划拨信息 — 包括土地使用者名称、宗地位置、项目名称、宗地面积等")
async def get_land_allocations(keyword: str, skip: int = 0) -> str:
    """土地划拨信息 — 包括土地使用者名称、宗地位置、项目名称、宗地面积等"""
    return api_get("/APIService/realestate/getLandAllotListByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_land_primary_development", description="土地一级开发信息 — 包括主体名称、批准文号、项目名称等")
async def get_land_primary_development(keyword: str, skip: int = 0) -> str:
    """土地一级开发信息 — 包括主体名称、批准文号、项目名称等"""
    return api_get("/APIService/realestate/getLandExploitListByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_land_acquisitions", description="土地征收信息 — 包括用地单位、项目名称、用地位置、用地面积等")
async def get_land_acquisitions(keyword: str, skip: int = 0) -> str:
    """土地征收信息 — 包括用地单位、项目名称、用地位置、用地面积等"""
    return api_get("/APIService/realestate/getLandCollectListByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


# ═══ 27. 业务场景（综合报告） ════════════════════════════════════════

@mcp.tool(name="get_executive_insight", description="董监高信息洞察 — 通过企业名称加人名获取董监高相关信息")
async def get_executive_insight(keyword: str, skip: int = 0) -> str:
    """董监高信息洞察 — 通过企业名称加人名获取董监高相关信息"""
    return api_get("/APIService/reportData/getAllPersonInfo", make_query(keyword=keyword, skip=str(skip) if skip else None))


@mcp.tool(name="get_cooperation_risk_screening", description="合作风险排查 — 企业综合风险排查，一键获取企业在工商、司法、税务等各类风险信息")
async def get_cooperation_risk_screening(keyword: str, skip: int = 0) -> str:
    """合作风险排查 — 企业综合风险排查，一键获取企业在工商、司法、税务等各类风险信息"""
    return api_get("/APIService/reportData/getAllRiskInfoByName", make_query(keyword=keyword, skip=str(skip) if skip else None))


# ═══ 28. 特色专区 ══════════════════════════════════════════════

@mcp.tool(name="get_comprehensive_risk_events", description="综合风险事件 — 企业风险类型、风险内容、风险事件、风险等级、业务披露事件等")
async def get_comprehensive_risk_events(keyword: str, skip: int = 0) -> str:
    """综合风险事件 — 企业风险类型、风险内容、风险事件、风险等级、业务披露事件等"""
    return api_get("/APIService/risk/getEntRisk", make_query(keyword=keyword, skip=str(skip) if skip else None))


# ═══ Server 启动 ═══════════════════════════════════════════

def run_cli():
    """CLI entry point."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run_cli()
