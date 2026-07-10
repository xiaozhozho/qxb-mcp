import asyncio
import json
import hashlib
import time
import logging

import httpx
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("qx-mcp")

APPKEY = "86f566b8-e0cb-43f3-a2db-33af1f6def9e"
SECRET_KEY = "778ef325-2ec2-4fb4-9b96-ae3fe0cdc8b2"
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
    return api_get("/APIService/relation/getRelatedRelation", make_query(name=name, relationship_type=relationship_type, relationship_level=relationship_level))


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


# ═══ Server 启动 ═══════════════════════════════════════════

def run_cli():
    """CLI entry point."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run_cli()
