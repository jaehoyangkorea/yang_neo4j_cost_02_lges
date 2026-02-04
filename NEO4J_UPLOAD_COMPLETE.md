# ✅ Neo4j 업로드 완료!

## 📊 업로드된 데이터

### 노드 (Nodes)
- **Cause**: 14개 - 원가차이 원인 코드
- **Material**: 24개 - 배터리 원부재료 (양극재, 음극재, 전해질 등)
- **Product**: 11개 - 배터리 제품 (EV 7개, ESS 4개)
- **ProductionOrder**: 150개 - 생산오더 (3개월)
- **Variance**: 445개 - 원가차이 분석
- **WorkCenter**: 20개 - 작업장 (전극 제조, 셀 조립, 화성, 팩 조립)

### 관계 (Relationships)
- **CAUSED_BY**: 445개 - Variance → Cause (차이의 원인)
- **CONSUMES**: 1,322개 - ProductionOrder → Material (자재 소비)
- **HAS_VARIANCE**: 445개 - ProductionOrder → Variance (차이 발생)
- **PRODUCES**: 150개 - ProductionOrder → Product (제품 생산)
- **USES_MATERIAL**: 143개 - Product → Material (BOM)

**총 노드**: 664개  
**총 관계**: 2,505개

---

## 💰 최대 원가차이 발생 오더 Top 5

1. **PO-2024-0119**: 871,372,323원
2. **PO-2024-0058**: 864,294,697원
3. **PO-2024-0053**: 771,730,744원
4. **PO-2024-0016**: 734,387,424원
5. **PO-2024-0148**: 696,846,706원

---

## 🎯 다음 단계

### 1. 시각화 및 분석

#### Flask API 서버 시작
```bash
python visualization/graph_api_server.py
```

#### 브라우저에서 접속
```
http://localhost:5000
```

### 2. Neo4j Browser에서 직접 쿼리

#### Neo4j Aura 접속
- URI: `neo4j+s://761c1872.databases.neo4j.io`
- Username: `neo4j`
- Password: `.env 파일 참조`

#### 유용한 쿼리

**전체 그래프 구조 보기**
```cypher
MATCH (n)
RETURN n
LIMIT 100
```

**특정 생산오더의 원가차이 분석**
```cypher
MATCH path = (po:ProductionOrder {id: 'PO-2024-0119'})-[*1..2]-(n)
RETURN path
```

**원가차이 원인별 통계**
```cypher
MATCH (v:Variance)-[:CAUSED_BY]->(c:Cause)
RETURN c.description as 원인,
       count(*) as 발생건수,
       sum(v.variance_amount) as 총차이금액
ORDER BY 총차이금액 DESC
```

**제품별 BOM 조회**
```cypher
MATCH (p:Product {id: 'EV-NCM811-100'})-[r:USES_MATERIAL]->(m:Material)
RETURN p.name as 제품,
       m.name as 자재,
       m.type as 자재유형,
       r.quantity as 소요량,
       m.standard_price as 단가
ORDER BY r.quantity * m.standard_price DESC
```

---

## 📁 프로젝트 구조

```
yang_neo4j_cost_02_LGES/
├── data/                          # 현재 사용 중인 데이터 (배터리)
│   ├── rdb_tables/
│   └── neo4j_import/
├── data_scenarios/                # 시나리오별 데이터
│   ├── battery/                   # 배터리 시나리오 ✅
│   │   ├── rdb_tables/
│   │   └── neo4j_import/
│   └── semiconductor/             # 반도체 시나리오 (준비 중)
├── neo4j/
│   └── data_loader.py            # Neo4j 데이터 로더
├── visualization/
│   └── graph_api_server.py       # Flask API 서버
├── upload_to_neo4j.py            # 자동 업로드 스크립트
└── verify_neo4j.py               # 데이터 검증 스크립트
```

---

## 🔄 시나리오 전환 방법

나중에 반도체 데이터도 사용하고 싶다면:

```bash
# 현재 data 폴더 백업
mv data data_backup_battery

# 반도체 데이터로 교체
cp -r data_scenarios/semiconductor data/

# Neo4j 업로드
python upload_to_neo4j.py
```

---

## 📝 참고 문서

- `data/DATA_SUMMARY.md` - 배터리 데이터 상세 요약
- `data/NEO4J_UPLOAD_GUIDE.md` - Neo4j 업로드 가이드
- `data_scenarios/README.md` - 시나리오별 설명
- `ANALYSIS_SCENARIO.md` - 분석 시나리오 가이드

---

**작성일**: 2024-02-04  
**Neo4j 인스턴스**: semiconductor-cost-analysis (배터리 데이터 로드됨)  
**상태**: ✅ 완료
