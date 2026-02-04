# LG에너지솔루션 배터리 원가 데이터세트 요약

## 📊 생성된 데이터 개요

### 데이터 생성 정보
- **생성일**: 2024-02-04
- **데이터 기간**: 2024년 1월 ~ 3월 (3개월)
- **산업 분야**: 배터리 제조 (자동차 배터리, ESS 배터리)
- **목적**: 원가차이 분석 시나리오

### 주요 통계
- **제품**: 11개 (EV: 7개, ESS: 4개)
- **자재**: 24개
- **BOM**: 143개
- **작업장**: 20개 (전극 제조 → 셀 조립 → 화성/검사 → 팩 조립)
- **생산오더**: 150개
- **자재 투입 실적**: 1,950건
- **작업 실적**: 1,950건
- **원가 집계**: 450건
- **원가차이**: 445건

---

## 🔋 제품 구성

### EV 배터리 (자동차용) - 7개
| 제품코드 | 제품명 | 화학조성 | 용량 | 표준원가 |
|---------|--------|---------|------|---------|
| EV-NCM811-100 | NCM811 100kWh 배터리팩 | NCM811 | 100kWh | 45,000,000원 |
| EV-NCM811-80 | NCM811 80kWh 배터리팩 | NCM811 | 80kWh | 36,000,000원 |
| EV-NCM811-60 | NCM811 60kWh 배터리팩 | NCM811 | 60kWh | 27,000,000원 |
| EV-NCM622-75 | NCM622 75kWh 배터리팩 | NCM622 | 75kWh | 30,000,000원 |
| EV-NCM523-50 | NCM523 50kWh 배터리팩 | NCM523 | 50kWh | 22,000,000원 |
| EV-LFP-70 | LFP 70kWh 배터리팩 | LFP | 70kWh | 21,000,000원 |
| EV-LFP-55 | LFP 55kWh 배터리팩 | LFP | 55kWh | 16,500,000원 |

### ESS 배터리 (에너지저장장치) - 4개
| 제품코드 | 제품명 | 화학조성 | 용량 | 표준원가 |
|---------|--------|---------|------|---------|
| ESS-NCM-500 | NCM 500kWh ESS 배터리 | NCM622 | 500kWh | 180,000,000원 |
| ESS-NCM-250 | NCM 250kWh ESS 배터리 | NCM622 | 250kWh | 90,000,000원 |
| ESS-LFP-1000 | LFP 1000kWh ESS 배터리 | LFP | 1000kWh | 250,000,000원 |
| ESS-LFP-500 | LFP 500kWh ESS 배터리 | LFP | 500kWh | 125,000,000원 |

---

## 🧪 원부재료 구성 (24개)

### 1. 양극재 (Cathode Material) - 6개
- **NCM811 양극재** (180,000원/kg, 한국)
- **NCM811 양극재 (대체)** (195,000원/kg, 중국)
- **NCM622 양극재** (150,000원/kg, 한국)
- **NCM523 양극재** (130,000원/kg, 일본)
- **LFP 양극재** (45,000원/kg, 중국)
- **LFP 양극재 (대체)** (52,000원/kg, 중국)

### 2. 음극재 (Anode Material) - 3개
- **천연 흑연 음극재** (25,000원/kg, 중국)
- **인조 흑연 음극재** (35,000원/kg, 일본)
- **실리콘 음극재** (150,000원/kg, 한국)

### 3. 전해질 (Electrolyte) - 3개
- **LiPF6 전해질** (85,000원/L, 한국)
- **LiPF6 전해질 (대체)** (95,000원/L, 중국)
- **전해질 첨가제** (120,000원/L, 한국)

### 4. 분리막 (Separator) - 3개
- **PE 분리막** (8,500원/m2, 한국)
- **PP 분리막** (9,200원/m2, 일본)
- **세라믹 코팅 분리막** (12,000원/m2, 한국)

### 5. 집전체 (Current Collector) - 2개
- **알루미늄 박막** (12,000원/kg, 한국)
- **구리 박막** (25,000원/kg, 한국)

### 6. 바인더 및 용매 - 2개
- **PVDF 바인더** (35,000원/kg, 일본)
- **NMP 용매** (8,500원/L, 중국)

### 7. 케이스 및 부품 - 5개
- **알루미늄 케이스** (45,000원/EA, 한국)
- **스틸 케이스** (35,000원/EA, 한국)
- **BMS 모듈** (280,000원/EA, 한국)
- **냉각 시스템** (150,000원/EA, 한국)
- **버스바** (18,000원/EA, 한국)

---

## 🏭 작업장 구성 (20개)

### A동 - 전극 제조 공정 (5개)
1. **전극 슬러리 믹싱 라인 1, 2** (ELECTRODE_MIXING)
2. **전극 코팅 라인 1, 2** (ELECTRODE_COATING)
3. **전극 프레싱 라인 1** (ELECTRODE_PRESSING)

### B동 - 셀 조립 공정 (5개)
4. **셀 스태킹 라인 1, 2** (CELL_STACKING)
5. **셀 웰딩 라인 1** (CELL_WELDING)
6. **전해액 주입 라인 1** (ELECTROLYTE_INJECTION)
7. **셀 실링 라인 1** (CELL_SEALING)

### C동 - 화성 및 검사 (4개)
8. **화성 공정 라인 1, 2** (FORMATION) - 4시간 소요
9. **에이징 공정 라인 1** (AGING) - 8시간 소요
10. **셀 검사 라인 1** (INSPECTION)

### D동 - 팩 조립 (4개)
11. **모듈 조립 라인 1, 2** (MODULE_ASSEMBLY)
12. **팩 조립 라인 1, 2** (PACK_ASSEMBLY)

### E동 - 최종 검사 (2개)
13. **최종 검사 라인 1, 2** (FINAL_TEST)

---

## 💰 원가차이 분석 결과

### 전체 원가차이
- **총 차이 금액**: 37,896,251,537원 (약 379억원)
- **평균 차이율**: 16.37%

### 심각도별 분포
| 심각도 | 건수 | 비율 |
|--------|------|------|
| HIGH (15% 초과) | 188건 | 42.2% |
| MEDIUM (8-15%) | 87건 | 19.6% |
| LOW (8% 미만) | 170건 | 38.2% |

### 원가요소별 차이
| 원가요소 | 차이 금액 | 비율 |
|---------|----------|------|
| 재료비 (MATERIAL) | 33,859,507,614원 | 89.4% |
| 노무비 (LABOR) | 2,384,358,901원 | 6.3% |
| 경비 (OVERHEAD) | 1,652,697,191원 | 4.3% |

---

## 🔍 원가차이 원인 분석

### 재료비 차이 원인 (7개)
| 원인코드 | 차이유형 | 원인 설명 | 담당부서 |
|---------|---------|----------|---------|
| MAT_PRICE_INCREASE | PRICE | 원자재 가격 상승 | 구매팀 |
| SUPPLIER_CHANGED | PRICE | 공급업체 변경 | 구매팀 |
| ALTERNATIVE_MATERIAL | PRICE | 대체자재 사용 | 구매팀 |
| QUALITY_DEFECT | QUANTITY | 자재 품질 불량 | 품질팀 |
| MATERIAL_WASTE | QUANTITY | 자재 낭비 | 생산팀 |
| PROCESS_YIELD_LOW | QUANTITY | 공정 수율 저하 | 생산팀 |
| PRODUCTION_QTY_DIFF | VOLUME | 생산량 차이 | 생산관리팀 |

### 노무비 차이 원인 (5개)
| 원인코드 | 차이유형 | 원인 설명 | 담당부서 |
|---------|---------|----------|---------|
| OVERTIME_WORK | RATE | 초과 근무 | 생산팀 |
| SKILL_PREMIUM | RATE | 숙련공 투입 | 생산팀 |
| NEW_WORKER | EFFICIENCY | 신규 작업자 | 생산팀 |
| EQUIPMENT_FAILURE | EFFICIENCY | 설비 고장 | 설비팀 |
| PROCESS_COMPLEXITY | EFFICIENCY | 공정 복잡도 | 생산팀 |

### 경비 차이 원인 (2개)
| 원인코드 | 차이유형 | 원인 설명 | 담당부서 |
|---------|---------|----------|---------|
| LOW_UTILIZATION | VOLUME | 가동률 저하 | 생산관리팀 |
| ENERGY_COST_UP | SPENDING | 에너지 비용 상승 | 관리팀 |

---

## 📈 분석 시나리오 예시

### 시나리오 1: 재료비 단가차이 분석
**생산오더**: PO-2024-0007 (EV-NCM811-80, 50개)
- **원가차이**: +426,633,197원 (16.37%)
- **차이유형**: PRICE (단가차이)
- **원인**: ALTERNATIVE_MATERIAL (대체자재 사용)
- **상세**: 주자재(NCM811 양극재) 품절로 대체자재 긴급 사용
  - 정상 단가: 180,000원/kg
  - 대체 단가: 195,000원/kg
  - 차이: +15,000원/kg (8.3% 증가)

### 시나리오 2: 재료비 수량차이 분석
**생산오더**: PO-2024-0012 (EV-NCM811-100, 120개)
- **원가차이**: 품질 불량으로 재료 과다 투입
- **차이유형**: QUANTITY (수량차이)
- **원인**: QUALITY_DEFECT (자재 품질 불량)
- **상세**: 입고된 음극재의 품질 문제로 재작업 발생
  - 계획 투입량: 120kg
  - 실제 투입량: 135kg
  - 차이: +15kg (12.5% 증가)

### 시나리오 3: 노무비 효율차이 분석
**생산오더**: PO-2024-0003 (EV-LFP-70, 120개)
- **원가차이**: +17,099,610원 (26.54%)
- **차이유형**: RATE (시간당 요율 차이)
- **원인**: OVERTIME_WORK (초과 근무)
- **상세**: 납기 준수를 위한 잔업 및 특근
  - 정상 노무비율: 45,000원/시간
  - 초과 근무율: 67,500원/시간 (1.5배)

### 시나리오 4: 설비 고장으로 인한 복합 차이
**생산오더**: PO-2024-0002
- **재료비**: 품질 불량으로 수량 증가
- **노무비**: 설비 고장으로 작업시간 증가 (효율 75%)
- **경비**: 설비 가동률 저하로 고정비 배부 증가
- **총 차이**: 약 1억원

---

## 📁 생성된 파일 목록

### RDB 테이블 형식 (`data/rdb_tables/`)
1. `product_master.csv` - 제품 마스터
2. `material_master.csv` - 자재 마스터
3. `bom.csv` - BOM (자재 소요량)
4. `work_center.csv` - 작업장 마스터
5. `routing.csv` - 라우팅 (공정 순서)
6. `production_order.csv` - 생산오더
7. `material_consumption.csv` - 자재 투입 실적
8. `operation_actual.csv` - 작업 실적
9. `cost_accumulation.csv` - 원가 집계
10. `variance_analysis.csv` - 원가차이 분석
11. `cause_code.csv` - 원인 코드 마스터

### Neo4j 임포트용 (`data/neo4j_import/`)
**노드 파일:**
- `products.csv` - Product 노드
- `materials.csv` - Material 노드
- `work_centers.csv` - WorkCenter 노드
- `production_orders.csv` - ProductionOrder 노드
- `variances.csv` - Variance 노드
- `causes.csv` - Cause 노드

**관계 파일:**
- `rel_uses_material.csv` - Product → Material (BOM)
- `rel_produces.csv` - ProductionOrder → Product
- `rel_consumes.csv` - ProductionOrder → Material (실제 소비)
- `rel_works_at.csv` - ProductionOrder → WorkCenter
- `rel_has_variance.csv` - ProductionOrder → Variance
- `rel_caused_by.csv` - Variance → Cause

---

## 🚀 다음 단계

### 1. Neo4j 업로드
```bash
# Neo4j 데이터 로더 실행
python neo4j/data_loader.py
```

### 2. 데이터 검증
```cypher
// 전체 노드 수 확인
MATCH (n) RETURN labels(n) as label, count(*) as count

// 생산오더별 원가차이 조회
MATCH (po:ProductionOrder)-[:HAS_VARIANCE]->(v:Variance)-[:CAUSED_BY]->(c:Cause)
RETURN po.id, v.variance_amount, c.description
ORDER BY v.variance_amount DESC
LIMIT 10
```

### 3. 시각화 및 분석
- Flask API 서버 시작: `python visualization/graph_api_server.py`
- 대시보드 접속: `http://localhost:5000`

---

## 💡 데이터 특징

### 1. 실제 시나리오 반영
- **대체자재 사용**: 5% 확률로 주자재 대신 대체자재 사용
- **품질 불량**: 10% 확률로 자재 품질 문제 발생
- **설비 고장**: 5% 확률로 설비 효율 저하 (70-85%)
- **작업자 숙련도**: 작업 효율 80-105% 범위

### 2. 계획 vs 실적 차이
- **생산 수량**: 계획 대비 ±8% 변동
- **자재 투입**: 불량률 반영 + 품질 문제 반영
- **작업 시간**: 숙련도 + 설비 상태 반영
- **가격 변동**: ±8% 시장 가격 변동

### 3. 추적 가능한 원인
- 각 원가차이마다 구체적인 원인 코드 할당
- 원인 코드에 담당 부서 및 상세 설명 포함
- 심각도(HIGH/MEDIUM/LOW) 자동 계산

---

## 📊 데이터 품질

- **일관성**: 모든 FK 관계 유효
- **완전성**: 필수 필드 모두 입력
- **정확성**: 실제 배터리 제조 프로세스 반영
- **재현성**: 시드(42) 고정으로 동일 데이터 재생성 가능

---

**생성 완료 시각**: 2024-02-04 10:04
**데이터 버전**: 1.0
**생성자**: generate_data.py
