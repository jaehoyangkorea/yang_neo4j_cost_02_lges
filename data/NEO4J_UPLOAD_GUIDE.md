# Neo4j 데이터 업로드 가이드

## 📋 사전 준비

### 1. Neo4j 연결 정보 설정
`.env` 파일에 Neo4j 연결 정보를 입력하세요.

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password
NEO4J_DATABASE=neo4j
```

### 2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

---

## 🚀 데이터 업로드 방법

### 방법 1: Python 스크립트 사용 (권장)

```bash
# Neo4j 데이터 로더 실행
python neo4j/data_loader.py
```

이 스크립트는 다음 작업을 자동으로 수행합니다:
1. 기존 데이터 삭제 (선택사항)
2. 제약조건 및 인덱스 생성
3. 노드 데이터 업로드
4. 관계 데이터 업로드
5. 데이터 검증

### 방법 2: Cypher 스크립트 직접 실행

#### Step 1: 기존 데이터 삭제 (선택)
```cypher
// 모든 노드와 관계 삭제
MATCH (n) DETACH DELETE n;
```

#### Step 2: 제약조건 생성
```cypher
// 제품 ID 유니크 제약조건
CREATE CONSTRAINT product_id IF NOT EXISTS
FOR (p:Product) REQUIRE p.id IS UNIQUE;

// 자재 ID 유니크 제약조건
CREATE CONSTRAINT material_id IF NOT EXISTS
FOR (m:Material) REQUIRE m.id IS UNIQUE;

// 작업장 ID 유니크 제약조건
CREATE CONSTRAINT workcenter_id IF NOT EXISTS
FOR (w:WorkCenter) REQUIRE w.id IS UNIQUE;

// 생산오더 ID 유니크 제약조건
CREATE CONSTRAINT order_id IF NOT EXISTS
FOR (o:ProductionOrder) REQUIRE o.id IS UNIQUE;

// 원가차이 ID 유니크 제약조건
CREATE CONSTRAINT variance_id IF NOT EXISTS
FOR (v:Variance) REQUIRE v.id IS UNIQUE;

// 원인 코드 유니크 제약조건
CREATE CONSTRAINT cause_code IF NOT EXISTS
FOR (c:Cause) REQUIRE c.code IS UNIQUE;
```

#### Step 3: 노드 데이터 로드

**Product 노드**
```cypher
LOAD CSV WITH HEADERS FROM 'file:///products.csv' AS row
CREATE (p:Product {
  id: row.id,
  name: row.name,
  type: row.type,
  chemistry: row.chemistry,
  capacity: toFloat(row.capacity),
  standard_cost: toFloat(row.standard_cost),
  active: toBoolean(row.active)
});
```

**Material 노드**
```cypher
LOAD CSV WITH HEADERS FROM 'file:///materials.csv' AS row
CREATE (m:Material {
  id: row.id,
  name: row.name,
  type: row.type,
  unit: row.unit,
  standard_price: toFloat(row.standard_price),
  supplier_cd: row.supplier_cd,
  origin: row.origin,
  active: toBoolean(row.active)
});
```

**WorkCenter 노드**
```cypher
LOAD CSV WITH HEADERS FROM 'file:///work_centers.csv' AS row
CREATE (w:WorkCenter {
  id: row.id,
  name: row.name,
  process_type: row.process_type,
  labor_rate_per_hour: toFloat(row.labor_rate_per_hour),
  overhead_rate_per_hour: toFloat(row.overhead_rate_per_hour),
  capacity_per_hour: toInteger(row.capacity_per_hour),
  location: row.location,
  active: toBoolean(row.active)
});
```

**ProductionOrder 노드**
```cypher
LOAD CSV WITH HEADERS FROM 'file:///production_orders.csv' AS row
CREATE (o:ProductionOrder {
  id: row.id,
  product_cd: row.product_cd,
  order_type: row.order_type,
  planned_qty: toInteger(row.planned_qty),
  actual_qty: toInteger(row.actual_qty),
  good_qty: toInteger(row.good_qty),
  scrap_qty: toInteger(row.scrap_qty),
  yield_rate: toFloat(row.yield_rate),
  order_date: date(row.order_date),
  start_date: date(row.start_date),
  finish_date: date(row.finish_date),
  status: row.status
});
```

**Variance 노드**
```cypher
LOAD CSV WITH HEADERS FROM 'file:///variances.csv' AS row
CREATE (v:Variance {
  id: row.id,
  order_no: row.order_no,
  cost_element: row.cost_element,
  variance_type: row.variance_type,
  variance_amount: toFloat(row.variance_amount),
  variance_percent: toFloat(row.variance_percent),
  severity: row.severity,
  cause_code: row.cause_code,
  analysis_date: date(row.analysis_date)
});
```

**Cause 노드**
```cypher
LOAD CSV WITH HEADERS FROM 'file:///causes.csv' AS row
CREATE (c:Cause {
  code: row.code,
  category: row.category,
  variance_type: row.variance_type,
  description: row.description,
  responsible_dept: row.responsible_dept,
  detail: row.detail
});
```

#### Step 4: 관계 데이터 로드

**USES_MATERIAL (Product → Material)**
```cypher
LOAD CSV WITH HEADERS FROM 'file:///rel_uses_material.csv' AS row
MATCH (p:Product {id: row.from})
MATCH (m:Material {id: row.to})
CREATE (p)-[:USES_MATERIAL {
  quantity: toFloat(row.quantity),
  unit: row.unit
}]->(m);
```

**PRODUCES (ProductionOrder → Product)**
```cypher
LOAD CSV WITH HEADERS FROM 'file:///rel_produces.csv' AS row
MATCH (o:ProductionOrder {id: row.from})
MATCH (p:Product {id: row.to})
CREATE (o)-[:PRODUCES]->(p);
```

**CONSUMES (ProductionOrder → Material)**
```cypher
LOAD CSV WITH HEADERS FROM 'file:///rel_consumes.csv' AS row
MATCH (o:ProductionOrder {id: row.from})
MATCH (m:Material {id: row.to})
CREATE (o)-[:CONSUMES {
  planned_qty: toFloat(row.planned_qty),
  actual_qty: toFloat(row.actual_qty),
  unit: row.unit,
  is_alternative: row.is_alternative
}]->(m);
```

**WORKS_AT (ProductionOrder → WorkCenter)**
```cypher
LOAD CSV WITH HEADERS FROM 'file:///rel_works_at.csv' AS row
MATCH (o:ProductionOrder {id: row.from})
MATCH (w:WorkCenter {id: row.to})
CREATE (o)-[:WORKS_AT {
  standard_time_min: toFloat(row.standard_time_min),
  actual_time_min: toFloat(row.actual_time_min),
  efficiency_rate: toFloat(row.efficiency_rate),
  worker_count: toInteger(row.worker_count)
}]->(w);
```

**HAS_VARIANCE (ProductionOrder → Variance)**
```cypher
LOAD CSV WITH HEADERS FROM 'file:///rel_has_variance.csv' AS row
MATCH (o:ProductionOrder {id: row.from})
MATCH (v:Variance {id: row.to})
CREATE (o)-[:HAS_VARIANCE]->(v);
```

**CAUSED_BY (Variance → Cause)**
```cypher
LOAD CSV WITH HEADERS FROM 'file:///rel_caused_by.csv' AS row
MATCH (v:Variance {id: row.from})
MATCH (c:Cause {code: row.to})
CREATE (v)-[:CAUSED_BY]->(c);
```

---

## ✅ 데이터 검증

### 노드 수 확인
```cypher
MATCH (n)
RETURN labels(n)[0] as NodeType, count(*) as Count
ORDER BY NodeType;
```

예상 결과:
- Product: 11
- Material: 24
- WorkCenter: 20
- ProductionOrder: 150
- Variance: 445
- Cause: 14

### 관계 수 확인
```cypher
MATCH ()-[r]->()
RETURN type(r) as RelationType, count(*) as Count
ORDER BY RelationType;
```

### 전체 그래프 구조 확인
```cypher
MATCH (n)
RETURN n
LIMIT 100;
```

---

## 🔍 유용한 쿼리

### 1. 원가차이가 큰 생산오더 TOP 10
```cypher
MATCH (po:ProductionOrder)-[:HAS_VARIANCE]->(v:Variance)
WITH po, sum(v.variance_amount) as total_variance
ORDER BY abs(total_variance) DESC
LIMIT 10
RETURN po.id as 생산오더,
       po.product_cd as 제품,
       po.planned_qty as 계획수량,
       po.actual_qty as 실적수량,
       total_variance as 총원가차이;
```

### 2. 특정 제품의 BOM 조회
```cypher
MATCH (p:Product {id: 'EV-NCM811-100'})-[r:USES_MATERIAL]->(m:Material)
RETURN p.name as 제품명,
       m.name as 자재명,
       m.type as 자재유형,
       r.quantity as 소요량,
       r.unit as 단위,
       m.standard_price as 단가,
       r.quantity * m.standard_price as 금액
ORDER BY 금액 DESC;
```

### 3. 원가차이 원인별 통계
```cypher
MATCH (v:Variance)-[:CAUSED_BY]->(c:Cause)
RETURN c.description as 원인,
       c.category as 원가요소,
       count(*) as 발생건수,
       sum(v.variance_amount) as 총차이금액,
       avg(v.variance_percent) as 평균차이율
ORDER BY 총차이금액 DESC;
```

### 4. 특정 생산오더의 전체 원가 흐름 추적
```cypher
MATCH path = (po:ProductionOrder {id: 'PO-2024-0001'})-[*1..2]-(n)
RETURN path;
```

### 5. 대체자재 사용 현황
```cypher
MATCH (po:ProductionOrder)-[r:CONSUMES]->(m:Material)
WHERE r.is_alternative = 'Y'
RETURN po.id as 생산오더,
       m.name as 대체자재,
       r.actual_qty as 투입량,
       r.unit as 단위
ORDER BY po.id;
```

### 6. 설비별 작업 효율 분석
```cypher
MATCH (po:ProductionOrder)-[r:WORKS_AT]->(w:WorkCenter)
WITH w, avg(r.efficiency_rate) as avg_efficiency, count(*) as work_count
RETURN w.name as 작업장,
       w.process_type as 공정유형,
       work_count as 작업건수,
       round(avg_efficiency, 2) as 평균효율
ORDER BY avg_efficiency;
```

---

## 🛠️ 문제 해결

### 문제 1: CSV 파일을 찾을 수 없음
**오류**: `Couldn't load the external resource`

**해결책**:
1. Neo4j Desktop 사용시: `import` 폴더에 CSV 파일 복사
2. Neo4j Aura 사용시: Python 스크립트 사용 (방법 1)
3. 파일 경로 확인: `file:///` 프로토콜 사용

### 문제 2: 메모리 부족
**오류**: `OutOfMemoryError`

**해결책**:
```bash
# neo4j.conf에서 힙 메모리 증가
dbms.memory.heap.initial_size=2G
dbms.memory.heap.max_size=4G
```

### 문제 3: 중복 노드 생성
**해결책**: 제약조건이 제대로 생성되었는지 확인
```cypher
SHOW CONSTRAINTS;
```

---

## 📊 성능 최적화

### 인덱스 생성 (선택사항)
```cypher
// 생산오더 날짜 인덱스
CREATE INDEX order_date IF NOT EXISTS
FOR (o:ProductionOrder) ON (o.order_date);

// 원가차이 심각도 인덱스
CREATE INDEX variance_severity IF NOT EXISTS
FOR (v:Variance) ON (v.severity);

// 자재 유형 인덱스
CREATE INDEX material_type IF NOT EXISTS
FOR (m:Material) ON (m.type);
```

---

## 📝 다음 단계

데이터 업로드가 완료되면:
1. **데이터 검증**: 위의 검증 쿼리 실행
2. **시각화**: Flask API 서버 시작
3. **분석**: 대시보드에서 원가차이 분석

```bash
# Flask API 서버 시작
python visualization/graph_api_server.py

# 브라우저에서 접속
http://localhost:5000
```

---

**작성일**: 2024-02-04
**버전**: 1.0
