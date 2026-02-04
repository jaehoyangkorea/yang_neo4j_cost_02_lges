"""
LG에너지솔루션 배터리 원가 데이터 생성기

배터리 생산 원가차이 분석을 위한 데이터 생성:
- 제품: 자동차 배터리(NCM, LFP), ESS 배터리
- 원부재료: 양극재, 음극재, 전해질, 분리막, 케이스 등
- 원가차이: 재료비(수량, 단가, 생산량), 노무비, 경비
- 원인: 품질문제, 대체자재, 업체변경, 설비고장, 작업자비효율
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random
import os

# 시드 설정 (재현성)
random.seed(42)
np.random.seed(42)
fake = Faker('ko_KR')
Faker.seed(42)

# 출력 디렉토리
RDB_DIR = 'data/rdb_tables'
NEO4J_DIR = 'data/neo4j_import'

os.makedirs(RDB_DIR, exist_ok=True)
os.makedirs(NEO4J_DIR, exist_ok=True)

# ============================================================
# 1. 마스터 데이터 생성
# ============================================================

def generate_products():
    """배터리 제품 마스터 생성"""
    products = []
    
    # EV 배터리 (자동차용)
    ev_batteries = [
        # NCM 계열 (니켈-코발트-망간)
        ('EV-NCM811-100', 'NCM811 100kWh 배터리팩', 'EV', 'NCM811', 100.0, 45000000),
        ('EV-NCM811-80', 'NCM811 80kWh 배터리팩', 'EV', 'NCM811', 80.0, 36000000),
        ('EV-NCM811-60', 'NCM811 60kWh 배터리팩', 'EV', 'NCM811', 60.0, 27000000),
        ('EV-NCM622-75', 'NCM622 75kWh 배터리팩', 'EV', 'NCM622', 75.0, 30000000),
        ('EV-NCM523-50', 'NCM523 50kWh 배터리팩', 'EV', 'NCM523', 50.0, 22000000),
        # LFP 계열 (리튬인산철)
        ('EV-LFP-70', 'LFP 70kWh 배터리팩', 'EV', 'LFP', 70.0, 21000000),
        ('EV-LFP-55', 'LFP 55kWh 배터리팩', 'EV', 'LFP', 55.0, 16500000),
    ]
    
    # ESS 배터리 (에너지저장장치)
    ess_batteries = [
        ('ESS-NCM-500', 'NCM 500kWh ESS 배터리', 'ESS', 'NCM622', 500.0, 180000000),
        ('ESS-NCM-250', 'NCM 250kWh ESS 배터리', 'ESS', 'NCM622', 250.0, 90000000),
        ('ESS-LFP-1000', 'LFP 1000kWh ESS 배터리', 'ESS', 'LFP', 1000.0, 250000000),
        ('ESS-LFP-500', 'LFP 500kWh ESS 배터리', 'ESS', 'LFP', 500.0, 125000000),
    ]
    
    all_batteries = ev_batteries + ess_batteries
    
    for product_cd, name, product_type, chemistry, capacity, std_cost in all_batteries:
        products.append({
            'product_cd': product_cd,
            'product_name': name,
            'product_type': product_type,
            'battery_chemistry': chemistry,
            'capacity_kwh': capacity,
            'standard_cost': std_cost,
            'active_flag': 'Y',
            'created_date': '2024-01-01'
        })
    
    df = pd.DataFrame(products)
    print(f"[OK] 제품 마스터 생성: {len(df)}개 (EV: {len(ev_batteries)}, ESS: {len(ess_batteries)})")
    return df

def generate_materials():
    """배터리 원부재료 마스터 생성 (단순화 버전 - 5개)"""
    materials = []
    
    # 5가지 핵심 자재만 생성
    core_materials = [
        # 양극재 (Cathode Material)
        ('MAT-CATHODE', '양극재', 'CATHODE', 'KG', 150000, 'SUP-CAT-01', '한국'),
        
        # 음극재 (Anode Material)
        ('MAT-ANODE', '음극재 (흑연)', 'ANODE', 'KG', 30000, 'SUP-ANO-01', '중국'),
        
        # 전해질 (Electrolyte)
        ('MAT-ELECTROLYTE', '전해질', 'ELECTROLYTE', 'L', 85000, 'SUP-ELE-01', '한국'),
        
        # 분리막 (Separator)
        ('MAT-SEPARATOR', '분리막', 'SEPARATOR', 'M2', 10000, 'SUP-SEP-01', '한국'),
        
        # 케이스 (Case)
        ('MAT-CASE', '배터리 케이스', 'CASE', 'EA', 40000, 'SUP-CAS-01', '한국'),
    ]
    
    for mat_cd, name, mat_type, unit, price, supplier, origin in core_materials:
        materials.append({
            'material_cd': mat_cd,
            'material_name': name,
            'material_type': mat_type,
            'unit': unit,
            'standard_price': price,
            'price_unit': 'KRW',
            'supplier_cd': supplier,
            'origin_country': origin,
            'active_flag': 'Y'
        })
    
    df = pd.DataFrame(materials)
    print(f"[OK] 자재 마스터 생성: {len(df)}개 (단순화)")
    return df

def generate_bom(products_df, materials_df):
    """BOM (Bill of Materials) 생성 (단순화 버전 - 5개 자재)"""
    boms = []
    bom_id = 1
    
    for idx, product in products_df.iterrows():
        product_cd = product['product_cd']
        capacity = product['capacity_kwh']
        
        # 1. 양극재
        boms.append({
            'bom_id': bom_id,
            'product_cd': product_cd,
            'material_cd': 'MAT-CATHODE',
            'quantity': round(1.5 * capacity, 2),
            'unit': 'KG',
            'valid_from': '2024-01-01',
            'valid_to': None,
            'bom_level': 1
        })
        bom_id += 1
        
        # 2. 음극재
        boms.append({
            'bom_id': bom_id,
            'product_cd': product_cd,
            'material_cd': 'MAT-ANODE',
            'quantity': round(1.2 * capacity, 2),
            'unit': 'KG',
            'valid_from': '2024-01-01',
            'valid_to': None,
            'bom_level': 1
        })
        bom_id += 1
        
        # 3. 전해질
        boms.append({
            'bom_id': bom_id,
            'product_cd': product_cd,
            'material_cd': 'MAT-ELECTROLYTE',
            'quantity': round(0.8 * capacity, 2),
            'unit': 'L',
            'valid_from': '2024-01-01',
            'valid_to': None,
            'bom_level': 1
        })
        bom_id += 1
        
        # 4. 분리막
        boms.append({
            'bom_id': bom_id,
            'product_cd': product_cd,
            'material_cd': 'MAT-SEPARATOR',
            'quantity': round(25.0 * capacity, 2),
            'unit': 'M2',
            'valid_from': '2024-01-01',
            'valid_to': None,
            'bom_level': 1
        })
        bom_id += 1
        
        # 5. 케이스
        boms.append({
            'bom_id': bom_id,
            'product_cd': product_cd,
            'material_cd': 'MAT-CASE',
            'quantity': 1,
            'unit': 'EA',
            'valid_from': '2024-01-01',
            'valid_to': None,
            'bom_level': 1
        })
        bom_id += 1
    
    df = pd.DataFrame(boms)
    print(f"[OK] BOM 생성: {len(df)}개 (제품당 5개 자재)")
    return df

def generate_work_centers():
    """작업장(워크센터) 마스터 생성 (3개로 단순화)"""
    work_centers = [
        # 1번: 전극 제조 (양극재, 음극재, 전해질 사용)
        ('WC-01', '전극 제조 라인 (양극재/음극재/전해질)', 'ELECTRODE', 45000, 85000, 300, 'A동'),
        
        # 2번: 분리막 처리
        ('WC-02', '분리막 처리 라인', 'SEPARATOR', 50000, 95000, 200, 'B동'),
        
        # 3번: 케이스 조립
        ('WC-03', '케이스 조립 라인', 'CASE_ASSEMBLY', 48000, 90000, 150, 'C동'),
    ]
    
    wc_list = []
    for wc_cd, name, proc_type, labor, overhead, capacity, location in work_centers:
        wc_list.append({
            'workcenter_cd': wc_cd,
            'workcenter_name': name,
            'process_type': proc_type,
            'labor_rate_per_hour': labor,
            'overhead_rate_per_hour': overhead,
            'capacity_per_hour': capacity,
            'location': location,
            'active_flag': 'Y'
        })
    
    df = pd.DataFrame(wc_list)
    print(f"[OK] 작업장 마스터 생성: {len(df)}개 (단순화)")
    return df

def generate_routing(products_df, work_centers_df):
    """라우팅 (제조 공정 순서) 생성 (3개 워크센터)"""
    routings = []
    routing_id = 1
    
    # 공정 순서 정의 (단순화 - 3단계)
    process_sequence = [
        ('ELECTRODE', 10, 600.0, 60.0),        # 1단계: 전극 제조 (10분)
        ('SEPARATOR', 20, 300.0, 30.0),        # 2단계: 분리막 처리 (5분)
        ('CASE_ASSEMBLY', 30, 900.0, 45.0),    # 3단계: 케이스 조립 (15분)
    ]
    
    for idx, product in products_df.iterrows():
        product_cd = product['product_cd']
        capacity = product['capacity_kwh']
        
        for proc_type, seq, base_time, setup_time in process_sequence:
            # 해당 공정의 작업장 선택
            wc_candidates = work_centers_df[work_centers_df['process_type'] == proc_type]
            if len(wc_candidates) == 0:
                continue
            
            wc_cd = wc_candidates.sample(1)['workcenter_cd'].values[0]
            
            # 표준시간 계산 (용량에 비례)
            # 큰 배터리는 시간이 더 걸림
            time_factor = 1.0 + (capacity - 60) / 200.0
            std_time = base_time * time_factor
            
            routings.append({
                'routing_id': routing_id,
                'product_cd': product_cd,
                'operation_seq': seq,
                'workcenter_cd': wc_cd,
                'standard_time_sec': round(std_time, 1),
                'setup_time_min': setup_time,
                'valid_from': '2024-01-01',
                'valid_to': None
            })
            routing_id += 1
    
    df = pd.DataFrame(routings)
    print(f"[OK] 라우팅 생성: {len(df)}개")
    return df

# ============================================================
# 2. 트랜잭션 데이터 생성
# ============================================================

def generate_production_orders(products_df):
    """생산오더 생성 (제품당 3개씩)"""
    orders = []
    start_date = datetime(2024, 1, 1)
    order_id = 1
    
    # 각 제품당 3개의 오더 생성
    for idx, product in products_df.iterrows():
        product_cd = product['product_cd']
        
        for i in range(3):
            # 날짜 생성 (1월~3월, 월별로 분산)
            month_offset = i  # 0, 1, 2개월
            days_offset = random.randint(0, 25)
            order_date = start_date + timedelta(days=(month_offset * 30 + days_offset))
            
            # 계획 수량
            if product['product_type'] == 'EV':
                planned_qty = random.choice([50, 80, 100, 120, 150])
            else:  # ESS
                planned_qty = random.choice([10, 15, 20, 25, 30])
            
            # 실적 수량 (계획 대비 ±8%)
            actual_qty = int(planned_qty * random.uniform(0.92, 1.08))
            
            # 수율 (92% ~ 98%)
            yield_rate = random.uniform(0.92, 0.98)
            
            # 양품/불량 수량
            good_qty = int(actual_qty * yield_rate)
            scrap_qty = actual_qty - good_qty
            
            # 완료일 (오더일 + 3~7일)
            finish_date = order_date + timedelta(days=random.randint(3, 7))
            
            orders.append({
                'order_no': f'PO-2024-{order_id:04d}',
                'product_cd': product_cd,
                'order_type': 'NORMAL',
                'planned_qty': planned_qty,
                'actual_qty': actual_qty,
                'good_qty': good_qty,
                'scrap_qty': scrap_qty,
                'order_date': order_date.strftime('%Y-%m-%d'),
                'start_date': order_date.strftime('%Y-%m-%d'),
                'finish_date': finish_date.strftime('%Y-%m-%d'),
                'status': 'CLOSED'
            })
            order_id += 1
    
    df = pd.DataFrame(orders)
    print(f"[OK] 생산오더 생성: {len(df)}개 (제품당 3개)")
    return df

def generate_material_consumption(production_orders_df, bom_df, materials_df):
    """자재 투입 실적 생성 (단순화 버전)"""
    consumptions = []
    consumption_id = 1
    
    for idx, order in production_orders_df.iterrows():
        order_no = order['order_no']
        product_cd = order['product_cd']
        planned_qty = order['planned_qty']
        actual_qty = order['actual_qty']
        scrap_qty = order['scrap_qty']
        
        # 해당 제품의 BOM 조회
        product_bom = bom_df[bom_df['product_cd'] == product_cd]
        
        for _, bom_item in product_bom.iterrows():
            material_cd = bom_item['material_cd']
            planned_qty_per_unit = bom_item['quantity']
            unit = bom_item['unit']
            
            # 계획 소요량
            planned_total = planned_qty_per_unit * planned_qty
            
            # 실제 투입량 계산
            # 시나리오 1: 불량 발생시 추가 투입 필요
            loss_factor = 1.0 + (scrap_qty / planned_qty) * 0.8
            
            # 시나리오 2: 재료 품질 문제로 과다 사용 (10% 확률)
            if random.random() < 0.10:
                quality_factor = random.uniform(1.05, 1.15)
            else:
                quality_factor = 1.0
            
            # 시나리오 3: 작업자 숙련도에 따른 차이 (±3%)
            skill_factor = random.uniform(0.97, 1.03)
            
            actual_total = (planned_qty_per_unit * planned_qty * 
                           loss_factor * quality_factor * skill_factor)
            
            consumptions.append({
                'consumption_id': consumption_id,
                'order_no': order_no,
                'material_cd': material_cd,
                'actual_material_cd': material_cd,
                'planned_qty': round(planned_total, 4),
                'actual_qty': round(actual_total, 4),
                'unit': unit,
                'is_alternative': 'N',
                'consumption_date': order['finish_date']
            })
            consumption_id += 1
    
    df = pd.DataFrame(consumptions)
    print(f"[OK] 자재 투입 실적 생성: {len(df)}개")
    return df

def generate_operation_actual(production_orders_df, routing_df, work_centers_df):
    """작업 실적 생성 (효율, 설비 고장 시나리오 포함)"""
    actuals = []
    actual_id = 1
    
    for idx, order in production_orders_df.iterrows():
        order_no = order['order_no']
        product_cd = order['product_cd']
        planned_qty = order['planned_qty']
        actual_qty = order['actual_qty']
        order_date = order['order_date']
        
        # 해당 제품의 라우팅 조회
        product_routing = routing_df[routing_df['product_cd'] == product_cd].sort_values('operation_seq')
        
        current_date = datetime.strptime(order_date, '%Y-%m-%d')
        
        for _, routing_item in product_routing.iterrows():
            workcenter_cd = routing_item['workcenter_cd']
            operation_seq = routing_item['operation_seq']
            standard_time_sec = routing_item['standard_time_sec']
            
            # 시나리오 1: 작업자 숙련도 (80% ~ 105%)
            worker_efficiency = random.uniform(0.80, 1.05)
            
            # 시나리오 2: 설비 상태 (5% 확률로 고장/노후화로 효율 저하)
            if random.random() < 0.05:
                equipment_efficiency = random.uniform(0.70, 0.85)
            else:
                equipment_efficiency = random.uniform(0.95, 1.02)
            
            # 실제 작업시간 계산
            total_efficiency = worker_efficiency * equipment_efficiency
            actual_time_per_unit = standard_time_sec / total_efficiency
            total_time_min = (actual_time_per_unit * actual_qty) / 60.0
            
            # 작업자 수 (공정에 따라 다름)
            process_type = routing_item['workcenter_cd'].split('-')[1]
            if 'FORMATION' in process_type or 'AGING' in process_type:
                worker_count = 1  # 자동화 공정
            else:
                worker_count = random.choice([2, 3, 4])
            
            actuals.append({
                'actual_id': actual_id,
                'order_no': order_no,
                'workcenter_cd': workcenter_cd,
                'operation_seq': operation_seq,
                'standard_time_min': round((standard_time_sec * actual_qty) / 60.0, 2),
                'actual_time_min': round(total_time_min, 2),
                'actual_qty': actual_qty,
                'efficiency_rate': round(total_efficiency * 100, 2),
                'work_date': current_date.strftime('%Y-%m-%d'),
                'worker_count': worker_count
            })
            actual_id += 1
            
            # 다음 공정으로 (화성, 에이징은 시간이 오래 걸림)
            if 'FORMATION' in workcenter_cd:
                current_date += timedelta(hours=12)
            elif 'AGING' in workcenter_cd:
                current_date += timedelta(hours=24)
            else:
                current_date += timedelta(hours=2)
    
    df = pd.DataFrame(actuals)
    print(f"[OK] 작업 실적 생성: {len(df)}개")
    return df

def calculate_cost_accumulation(production_orders_df, material_consumption_df, materials_df, 
                                operation_actual_df, work_centers_df, bom_df, routing_df):
    """원가 집계 계산 (재료비, 노무비, 경비)"""
    costs = []
    cost_id = 1
    
    for idx, order in production_orders_df.iterrows():
        order_no = order['order_no']
        product_cd = order['product_cd']
        planned_qty = order['planned_qty']
        actual_qty = order['actual_qty']
        
        # === 재료비 계산 ===
        # 계획 재료비
        product_bom = bom_df[bom_df['product_cd'] == product_cd]
        planned_material_cost = 0
        for _, bom_item in product_bom.iterrows():
            material_cd = bom_item['material_cd']
            material_price = materials_df[materials_df['material_cd'] == material_cd]['standard_price'].values[0]
            planned_material_cost += bom_item['quantity'] * material_price * planned_qty
        
        # 실적 재료비
        order_consumption = material_consumption_df[material_consumption_df['order_no'] == order_no]
        actual_material_cost = 0
        for _, cons in order_consumption.iterrows():
            # 실제 사용한 자재의 가격
            actual_mat_cd = cons['actual_material_cd']
            material_price = materials_df[materials_df['material_cd'] == actual_mat_cd]['standard_price'].values[0]
            
            # 가격 변동 시뮬레이션 (±8%)
            price_variance = random.uniform(0.92, 1.08)
            actual_price = material_price * price_variance
            
            actual_material_cost += cons['actual_qty'] * actual_price
        
        costs.append({
            'cost_id': cost_id,
            'order_no': order_no,
            'cost_element': 'MATERIAL',
            'cost_type': None,
            'planned_cost': round(planned_material_cost, 2),
            'actual_cost': round(actual_material_cost, 2),
            'variance': round(actual_material_cost - planned_material_cost, 2),
            'calculation_date': order['finish_date']
        })
        cost_id += 1
        
        # === 노무비 계산 ===
        # 계획 노무비
        product_routing = routing_df[routing_df['product_cd'] == product_cd]
        planned_labor_cost = 0
        for _, routing_item in product_routing.iterrows():
            wc_cd = routing_item['workcenter_cd']
            labor_rate = work_centers_df[work_centers_df['workcenter_cd'] == wc_cd]['labor_rate_per_hour'].values[0]
            std_time_hour = routing_item['standard_time_sec'] / 3600.0
            planned_labor_cost += std_time_hour * labor_rate * planned_qty
        
        # 실적 노무비
        order_actual = operation_actual_df[operation_actual_df['order_no'] == order_no]
        actual_labor_cost = 0
        for _, oper in order_actual.iterrows():
            wc_cd = oper['workcenter_cd']
            labor_rate = work_centers_df[work_centers_df['workcenter_cd'] == wc_cd]['labor_rate_per_hour'].values[0]
            actual_time_hour = oper['actual_time_min'] / 60.0
            actual_labor_cost += actual_time_hour * labor_rate * oper['worker_count']
        
        costs.append({
            'cost_id': cost_id,
            'order_no': order_no,
            'cost_element': 'LABOR',
            'cost_type': None,
            'planned_cost': round(planned_labor_cost, 2),
            'actual_cost': round(actual_labor_cost, 2),
            'variance': round(actual_labor_cost - planned_labor_cost, 2),
            'calculation_date': order['finish_date']
        })
        cost_id += 1
        
        # === 경비 계산 ===
        # 계획 경비
        planned_overhead_cost = 0
        for _, routing_item in product_routing.iterrows():
            wc_cd = routing_item['workcenter_cd']
            overhead_rate = work_centers_df[work_centers_df['workcenter_cd'] == wc_cd]['overhead_rate_per_hour'].values[0]
            std_time_hour = routing_item['standard_time_sec'] / 3600.0
            planned_overhead_cost += std_time_hour * overhead_rate * planned_qty
        
        # 실적 경비
        actual_overhead_cost = 0
        for _, oper in order_actual.iterrows():
            wc_cd = oper['workcenter_cd']
            overhead_rate = work_centers_df[work_centers_df['workcenter_cd'] == wc_cd]['overhead_rate_per_hour'].values[0]
            actual_time_hour = oper['actual_time_min'] / 60.0
            actual_overhead_cost += actual_time_hour * overhead_rate
        
        costs.append({
            'cost_id': cost_id,
            'order_no': order_no,
            'cost_element': 'OVERHEAD',
            'cost_type': None,
            'planned_cost': round(planned_overhead_cost, 2),
            'actual_cost': round(actual_overhead_cost, 2),
            'variance': round(actual_overhead_cost - planned_overhead_cost, 2),
            'calculation_date': order['finish_date']
        })
        cost_id += 1
    
    df = pd.DataFrame(costs)
    print(f"[OK] 원가 집계 생성: {len(df)}개")
    return df

def generate_variance_analysis(cost_accumulation_df, production_orders_df, 
                                material_consumption_df, operation_actual_df):
    """원가차이 분석 생성 (Production Order당 3개: 재료비차이, 노무비차이, 경비차이)"""
    variances = []
    variance_id = 1
    
    # 새로운 원인 코드 (단순화)
    material_causes = ['품질_불량', '대체자재_사용']
    labor_causes = ['인력_숙련도', '외주_사용']
    overhead_causes = ['설비_고장', '자재_사용_증가']
    
    # Production Order별로 정확히 3개의 variance 생성
    for order_no in production_orders_df['order_no']:
        # 해당 오더의 원가 데이터 조회
        order_costs = cost_accumulation_df[cost_accumulation_df['order_no'] == order_no]
        
        for _, cost in order_costs.iterrows():
            variance_amount = cost['variance']
            cost_element = cost['cost_element']
            
            # 차이 유형 및 원인 결정
            if cost_element == 'MATERIAL':
                variance_name = '재료비차이'
                variance_type = 'DIFF'
                # 수량 차이 비율 확인
                order_consumption = material_consumption_df[
                    material_consumption_df['order_no'] == order_no
                ]
                total_planned = order_consumption['planned_qty'].sum()
                total_actual = order_consumption['actual_qty'].sum()
                qty_diff_pct = ((total_actual - total_planned) / total_planned * 100) if total_planned > 0 else 0
                
                # 품질 불량이 더 자주 발생하도록
                if abs(qty_diff_pct) > 5:
                    cause_code = '품질_불량'
                else:
                    cause_code = random.choice(material_causes)
                
            elif cost_element == 'LABOR':
                variance_name = '노무비차이'
                variance_type = 'DIFF'
                # 작업 효율 확인
                order_operations = operation_actual_df[
                    operation_actual_df['order_no'] == order_no
                ]
                avg_efficiency = order_operations['efficiency_rate'].mean()
                
                # 효율이 낮으면 인력 숙련도 문제
                if avg_efficiency < 85:
                    cause_code = '인력_숙련도'
                else:
                    cause_code = random.choice(labor_causes)
                
            else:  # OVERHEAD
                variance_name = '경비차이'
                variance_type = 'DIFF'
                cause_code = random.choice(overhead_causes)
            
            # 차이율 계산
            if cost['planned_cost'] != 0:
                variance_percent = (variance_amount / cost['planned_cost']) * 100
            else:
                variance_percent = 0
            
            # 심각도 (차이 금액 기준)
            abs_amount = abs(variance_amount)
            if abs_amount > 10000000:  # 1천만원 이상
                severity = 'HIGH'
            elif abs_amount > 5000000:  # 5백만원 이상
                severity = 'MEDIUM'
            else:
                severity = 'LOW'
            
            variances.append({
                'variance_id': variance_id,
                'order_no': order_no,
                'variance_name': variance_name,  # 추가: 한글 이름
                'cost_element': cost_element,
                'variance_type': variance_type,
                'variance_amount': round(variance_amount, 2),
                'variance_percent': round(variance_percent, 4),
                'cause_code': cause_code,
                'severity': severity,
                'analysis_date': cost['calculation_date']
            })
            variance_id += 1
    
    df = pd.DataFrame(variances)
    print(f"[OK] 원가차이 분석 생성: {len(df)}개 (재료비/노무비/경비차이)")
    return df

def generate_cause_code():
    """원인 코드 마스터 생성 (단순화 - 6개)"""
    causes = [
        # 재료비차이 원인 (2개)
        ('품질_불량', 'MATERIAL', 'DIFF', '자재 품질 불량 (QUALITY_DEFECT)', '품질팀',
         '입고 자재의 품질 문제로 재작업 및 폐기 발생'),
        ('대체자재_사용', 'MATERIAL', 'DIFF', '대체자재 사용', '구매팀',
         '주자재 품절로 단가가 높은 대체자재 긴급 사용'),
        
        # 노무비차이 원인 (2개)
        ('인력_숙련도', 'LABOR', 'DIFF', '인력 숙련도', '생산팀',
         '신규 작업자 또는 미숙련 인력 투입으로 작업 효율 저하'),
        ('외주_사용', 'LABOR', 'DIFF', '외주 인력 사용', '생산팀',
         '정규직 대비 높은 단가의 외주 인력 투입'),
        
        # 경비차이 원인 (2개)
        ('설비_고장', 'OVERHEAD', 'DIFF', '설비 고장', '설비팀',
         '설비 고장 및 노후화로 작업 지연 및 유지보수 비용 증가'),
        ('자재_사용_증가', 'OVERHEAD', 'DIFF', '자재 사용 증가', '생산팀',
         '생산량 증가 또는 비효율로 인한 간접 자재 사용 증가'),
    ]
    
    cause_list = []
    for code, category, var_type, short_desc, dept, detail_desc in causes:
        cause_list.append({
            'cause_code': code,
            'cause_category': category,
            'variance_type': var_type,
            'cause_description': short_desc,
            'responsible_dept': dept,
            'detail_description': detail_desc
        })
    
    df = pd.DataFrame(cause_list)
    print(f"[OK] 원인 코드 생성: {len(df)}개 (단순화)")
    return df

def generate_quality_defects():
    """품질 불량 상세 데이터 생성 (5개 자재)"""
    defects = [
        ('QD-001', '양극재_불순물', '품질_불량', '양극재', '불순물 함유율 기준 초과', 'HIGH', 
         '2024-01-15', 'SUP-CAT-01', '입고검사에서 Fe 불순물 0.05% 검출 (기준 0.02%)'),
        ('QD-002', '양극재_결정구조', '품질_불량', '양극재', '결정 구조 불균일', 'HIGH',
         '2024-03-08', 'SUP-CAT-01', 'XRD 분석 결과 결정화도 82% (기준 90% 이상)'),
        ('QD-003', '음극재_입도', '품질_불량', '음극재 (흑연)', '입도 분포 불량', 'MEDIUM',
         '2024-02-18', 'SUP-ANO-01', 'D50 입도 18.5μm (기준 15±2μm)'),
        ('QD-004', '전해질_수분', '품질_불량', '전해질', '수분 함량 기준 초과', 'HIGH',
         '2024-01-22', 'SUP-ELE-01', '수분 함량 45ppm (기준 20ppm 이하)'),
        ('QD-005', '전해질_이물', '품질_불량', '전해질', '이물질 혼입', 'LOW',
         '2024-03-15', 'SUP-ELE-01', '10μm 이상 파티클 검출'),
        ('QD-006', '분리막_두께편차', '품질_불량', '분리막', '두께 편차 불량', 'MEDIUM',
         '2024-02-05', 'SUP-SEP-01', '두께 편차 ±3μm (기준 ±1.5μm)'),
        ('QD-007', '분리막_기공', '품질_불량', '분리막', '기공율 불량', 'MEDIUM',
         '2024-02-28', 'SUP-SEP-01', '기공율 38% (기준 40±2%)'),
    ]
    
    defect_list = []
    for defect_id, defect_type, cause_code, material, description, severity, detect_date, supplier, detail in defects:
        defect_list.append({
            'defect_id': defect_id,
            'defect_type': defect_type,
            'cause_code': cause_code,
            'material_name': material,
            'defect_description': description,
            'severity': severity,
            'detection_date': detect_date,
            'supplier_cd': supplier,
            'detail': detail
        })
    
    df = pd.DataFrame(defect_list)
    print(f"[OK] 품질 불량 데이터 생성: {len(df)}개")
    return df

def generate_equipment_failures():
    """설비 고장 데이터 생성"""
    failures = [
        ('EF-001', 'WC-COATING-01', '설비_고장', '코팅 헤드 고장', 
         '2024-01-18', '2024-01-19', 18.5, 'HIGH',
         '코팅 헤드 노즐 막힘으로 불균일 코팅 발생'),
        ('EF-002', 'WC-FORMATION-02', '설비_고장', '화성 챔버 온도 제어 불량',
         '2024-01-25', '2024-01-26', 28.0, 'HIGH',
         '온도 센서 고장으로 화성 온도 45°C → 52°C 상승'),
        ('EF-003', 'WC-STACKING-01', '설비_고장', '스태킹 로봇 위치 오차',
         '2024-02-08', '2024-02-08', 6.5, 'MEDIUM',
         '로봇 캘리브레이션 오류로 적층 위치 ±0.5mm 오차'),
        ('EF-004', 'WC-MIXING-02', '설비_고장', '믹서 모터 베어링 마모',
         '2024-02-14', '2024-02-16', 42.0, 'HIGH',
         '베어링 마모로 진동 증가 및 믹싱 불균일'),
        ('EF-005', 'WC-WELDING-01', '설비_고장', '레이저 출력 저하',
         '2024-02-22', '2024-02-23', 22.0, 'MEDIUM',
         '레이저 광원 노화로 용접 강도 15% 저하'),
        ('EF-006', 'WC-PRESSING-01', '설비_고장', '프레스 압력 불안정',
         '2024-03-05', '2024-03-06', 18.0, 'MEDIUM',
         '유압 펌프 누유로 압력 변동 ±5%'),
        ('EF-007', 'WC-INSPECTION-01', '설비_고장', '검사 장비 센서 고장',
         '2024-03-12', '2024-03-12', 4.5, 'LOW',
         '전압 측정 센서 드리프트로 측정 오차 발생'),
    ]
    
    failure_list = []
    for failure_id, wc_cd, cause_code, failure_type, start_date, end_date, downtime, severity, description in failures:
        failure_list.append({
            'failure_id': failure_id,
            'workcenter_cd': wc_cd,
            'cause_code': cause_code,
            'failure_type': failure_type,
            'failure_start': start_date,
            'failure_end': end_date,
            'downtime_hours': downtime,
            'severity': severity,
            'description': description
        })
    
    df = pd.DataFrame(failure_list)
    print(f"[OK] 설비 고장 데이터 생성: {len(df)}개")
    return df

def generate_material_market_prices():
    """자재 시황 데이터 생성 (5개 자재)"""
    market_data = []
    materials = [
        ('MAT-CATHODE', '양극재', [
            ('2024-01-01', 150000, 'STABLE', '안정적 공급', '니켈 가격 안정'),
            ('2024-02-01', 156000, 'INCREASE', '가격 상승', '중국 생산 감소로 공급 부족'),
            ('2024-03-01', 162000, 'INCREASE', '가격 급등', '니켈 LME 가격 15% 상승'),
        ]),
        ('MAT-ANODE', '음극재 (흑연)', [
            ('2024-01-01', 30000, 'STABLE', '안정적', '중국 공급 안정'),
            ('2024-02-01', 29000, 'DECREASE', '가격 하락', '중국 춘절 이후 생산 증가'),
            ('2024-03-01', 31000, 'INCREASE', '가격 반등', '수요 증가로 반등'),
        ]),
        ('MAT-ELECTROLYTE', '전해질', [
            ('2024-01-01', 85000, 'STABLE', '안정', '정상 공급'),
            ('2024-02-01', 88000, 'INCREASE', '가격 상승', '원료인 불화수소 가격 상승'),
            ('2024-03-01', 91000, 'INCREASE', '상승 지속', '중국 환경 규제 강화'),
        ]),
        ('MAT-SEPARATOR', '분리막', [
            ('2024-01-01', 10000, 'STABLE', '안정', '정상 공급'),
            ('2024-02-01', 10300, 'INCREASE', '소폭 상승', '원가 증가'),
            ('2024-03-01', 10600, 'INCREASE', '상승 추세', '고성능 분리막 수요 증가'),
        ]),
        ('MAT-CASE', '배터리 케이스', [
            ('2024-01-01', 40000, 'STABLE', '안정', '알루미늄 가격 안정'),
            ('2024-02-01', 41000, 'INCREASE', '가격 상승', '원자재 가격 인상'),
            ('2024-03-01', 42000, 'INCREASE', '강세 지속', '글로벌 알루미늄 수요 증가'),
        ]),
    ]
    
    market_id = 1
    for material_cd, material_name, price_history in materials:
        for date, price, trend, market_condition, note in price_history:
            market_data.append({
                'market_id': f'MP-{market_id:04d}',
                'material_cd': material_cd,
                'material_name': material_name,
                'price_date': date,
                'market_price': price,
                'price_trend': trend,
                'market_condition': market_condition,
                'note': note
            })
            market_id += 1
    
    df = pd.DataFrame(market_data)
    print(f"[OK] 자재 시황 데이터 생성: {len(df)}개 (5개 자재)")
    return df

# ============================================================
# 3. 메인 실행
# ============================================================

def main():
    print("=" * 70)
    print("LG에너지솔루션 배터리 원가 데이터 생성 (개선버전)")
    print("=" * 70)
    
    # 마스터 데이터 생성
    print("\n[1단계] 마스터 데이터 생성")
    products_df = generate_products()
    materials_df = generate_materials()
    bom_df = generate_bom(products_df, materials_df)
    work_centers_df = generate_work_centers()
    routing_df = generate_routing(products_df, work_centers_df)
    cause_code_df = generate_cause_code()
    
    # 새로운 마스터 데이터
    quality_defects_df = generate_quality_defects()
    equipment_failures_df = generate_equipment_failures()
    material_market_df = generate_material_market_prices()
    
    # 트랜잭션 데이터 생성
    print("\n[2단계] 트랜잭션 데이터 생성")
    production_orders_df = generate_production_orders(products_df)
    material_consumption_df = generate_material_consumption(
        production_orders_df, bom_df, materials_df
    )
    operation_actual_df = generate_operation_actual(
        production_orders_df, routing_df, work_centers_df
    )
    
    # 원가 데이터 생성
    print("\n[3단계] 원가 데이터 생성")
    cost_accumulation_df = calculate_cost_accumulation(
        production_orders_df, material_consumption_df, materials_df,
        operation_actual_df, work_centers_df, bom_df, routing_df
    )
    variance_analysis_df = generate_variance_analysis(
        cost_accumulation_df, production_orders_df, 
        material_consumption_df, operation_actual_df
    )
    
    # RDB 테이블 형식으로 저장
    print("\n[4단계] RDB 테이블 CSV 저장")
    products_df.to_csv(f'{RDB_DIR}/product_master.csv', index=False, encoding='utf-8-sig')
    materials_df.to_csv(f'{RDB_DIR}/material_master.csv', index=False, encoding='utf-8-sig')
    bom_df.to_csv(f'{RDB_DIR}/bom.csv', index=False, encoding='utf-8-sig')
    work_centers_df.to_csv(f'{RDB_DIR}/work_center.csv', index=False, encoding='utf-8-sig')
    routing_df.to_csv(f'{RDB_DIR}/routing.csv', index=False, encoding='utf-8-sig')
    production_orders_df.to_csv(f'{RDB_DIR}/production_order.csv', index=False, encoding='utf-8-sig')
    material_consumption_df.to_csv(f'{RDB_DIR}/material_consumption.csv', index=False, encoding='utf-8-sig')
    operation_actual_df.to_csv(f'{RDB_DIR}/operation_actual.csv', index=False, encoding='utf-8-sig')
    cost_accumulation_df.to_csv(f'{RDB_DIR}/cost_accumulation.csv', index=False, encoding='utf-8-sig')
    variance_analysis_df.to_csv(f'{RDB_DIR}/variance_analysis.csv', index=False, encoding='utf-8-sig')
    cause_code_df.to_csv(f'{RDB_DIR}/cause_code.csv', index=False, encoding='utf-8-sig')
    quality_defects_df.to_csv(f'{RDB_DIR}/quality_defects.csv', index=False, encoding='utf-8-sig')
    equipment_failures_df.to_csv(f'{RDB_DIR}/equipment_failures.csv', index=False, encoding='utf-8-sig')
    material_market_df.to_csv(f'{RDB_DIR}/material_market_prices.csv', index=False, encoding='utf-8-sig')
    
    print(f"[OK] RDB 테이블 저장 완료: {RDB_DIR}/")
    
    # Neo4j 임포트용 데이터 저장
    print("\n[5단계] Neo4j 임포트 CSV 저장")
    
    # Product 노드
    products_neo = products_df.copy()
    products_neo.rename(columns={
        'product_cd': 'id', 
        'product_name': 'name', 
        'product_type': 'type',
        'battery_chemistry': 'chemistry',
        'capacity_kwh': 'capacity'
    }, inplace=True)
    products_neo['active'] = products_neo['active_flag'] == 'Y'
    products_neo = products_neo[['id', 'name', 'type', 'chemistry', 'capacity', 'standard_cost', 'active']]
    products_neo.to_csv(f'{NEO4J_DIR}/products.csv', index=False)
    
    # Material 노드
    materials_neo = materials_df.copy()
    materials_neo.rename(columns={
        'material_cd': 'id', 
        'material_name': 'name',
        'material_type': 'type',
        'origin_country': 'origin'
    }, inplace=True)
    materials_neo['active'] = materials_neo['active_flag'] == 'Y'
    materials_neo = materials_neo[['id', 'name', 'type', 'unit', 'standard_price', 
                                     'supplier_cd', 'origin', 'active']]
    materials_neo.to_csv(f'{NEO4J_DIR}/materials.csv', index=False)
    
    # WorkCenter 노드
    work_centers_neo = work_centers_df.copy()
    work_centers_neo.rename(columns={
        'workcenter_cd': 'id', 
        'workcenter_name': 'name'
    }, inplace=True)
    work_centers_neo['active'] = work_centers_neo['active_flag'] == 'Y'
    work_centers_neo = work_centers_neo[[
        'id', 'name', 'process_type', 'labor_rate_per_hour', 
        'overhead_rate_per_hour', 'capacity_per_hour', 'location', 'active'
    ]]
    work_centers_neo.to_csv(f'{NEO4J_DIR}/work_centers.csv', index=False)
    
    # ProductionOrder 노드
    po_neo = production_orders_df.copy()
    po_neo.rename(columns={'order_no': 'id'}, inplace=True)
    po_neo['yield_rate'] = (po_neo['good_qty'] / po_neo['actual_qty'] * 100).round(2)
    po_neo.to_csv(f'{NEO4J_DIR}/production_orders.csv', index=False)
    
    # Variance 노드 (이미 variance_name 포함)
    var_neo = variance_analysis_df.copy()
    var_neo['id'] = var_neo['variance_id'].apply(lambda x: f'VAR-{x:05d}')
    
    var_neo = var_neo[[
        'id', 'variance_name', 'order_no', 'cost_element', 'variance_type', 'variance_amount', 
        'variance_percent', 'severity', 'cause_code', 'analysis_date'
    ]]
    var_neo.to_csv(f'{NEO4J_DIR}/variances.csv', index=False)
    
    # Cause 노드
    cause_neo = cause_code_df.copy()
    cause_neo.rename(columns={
        'cause_code': 'code', 
        'cause_category': 'category',
        'cause_description': 'description',
        'detail_description': 'detail'
    }, inplace=True)
    cause_neo.to_csv(f'{NEO4J_DIR}/causes.csv', index=False)
    
    # QualityDefect 노드
    defect_neo = quality_defects_df.copy()
    defect_neo.rename(columns={'defect_id': 'id'}, inplace=True)
    defect_neo.to_csv(f'{NEO4J_DIR}/quality_defects.csv', index=False)
    
    # EquipmentFailure 노드
    failure_neo = equipment_failures_df.copy()
    failure_neo.rename(columns={'failure_id': 'id'}, inplace=True)
    failure_neo.to_csv(f'{NEO4J_DIR}/equipment_failures.csv', index=False)
    
    # MaterialMarket 노드
    market_neo = material_market_df.copy()
    market_neo.rename(columns={'market_id': 'id'}, inplace=True)
    market_neo.to_csv(f'{NEO4J_DIR}/material_markets.csv', index=False)
    
    # 관계 데이터
    # USES_MATERIAL 관계 (Product -> Material)
    uses_material = bom_df[['product_cd', 'material_cd', 'quantity', 'unit']].copy()
    uses_material.rename(columns={'product_cd': 'from', 'material_cd': 'to'}, inplace=True)
    uses_material.to_csv(f'{NEO4J_DIR}/rel_uses_material.csv', index=False)
    
    # PRODUCES 관계 (ProductionOrder -> Product)
    produces = production_orders_df[['order_no', 'product_cd']].copy()
    produces.rename(columns={'order_no': 'from', 'product_cd': 'to'}, inplace=True)
    produces.to_csv(f'{NEO4J_DIR}/rel_produces.csv', index=False)
    
    # HAS_VARIANCE 관계 (ProductionOrder -> Variance)
    has_variance = variance_analysis_df[['order_no', 'variance_id']].copy()
    has_variance['variance_id'] = has_variance['variance_id'].apply(lambda x: f'VAR-{x:05d}')
    has_variance.rename(columns={'order_no': 'from', 'variance_id': 'to'}, inplace=True)
    has_variance.to_csv(f'{NEO4J_DIR}/rel_has_variance.csv', index=False)
    
    # CAUSED_BY 관계 (Variance -> Cause)
    caused_by = variance_analysis_df[['variance_id', 'cause_code']].dropna().copy()
    caused_by['variance_id'] = caused_by['variance_id'].apply(lambda x: f'VAR-{x:05d}')
    caused_by.rename(columns={'variance_id': 'from', 'cause_code': 'to'}, inplace=True)
    caused_by.to_csv(f'{NEO4J_DIR}/rel_caused_by.csv', index=False)
    
    # CONSUMES 관계 (ProductionOrder -> Material, 실제 소비)
    consumes = material_consumption_df[[
        'order_no', 'actual_material_cd', 'planned_qty', 'actual_qty', 'unit', 'is_alternative'
    ]].copy()
    consumes.rename(columns={'order_no': 'from', 'actual_material_cd': 'to'}, inplace=True)
    consumes.to_csv(f'{NEO4J_DIR}/rel_consumes.csv', index=False)
    
    # WORKS_AT 관계 (ProductionOrder -> WorkCenter)
    works_at = operation_actual_df[[
        'order_no', 'workcenter_cd', 'standard_time_min', 'actual_time_min', 
        'efficiency_rate', 'worker_count'
    ]].copy()
    works_at.rename(columns={'order_no': 'from', 'workcenter_cd': 'to'}, inplace=True)
    works_at.to_csv(f'{NEO4J_DIR}/rel_works_at.csv', index=False)
    
    # HAS_DEFECT 관계 (Cause -> QualityDefect)
    has_defect = quality_defects_df[['cause_code', 'defect_id']].copy()
    has_defect.rename(columns={'cause_code': 'from', 'defect_id': 'to'}, inplace=True)
    has_defect.to_csv(f'{NEO4J_DIR}/rel_has_defect.csv', index=False)
    
    # HAS_FAILURE 관계 (Cause -> EquipmentFailure)
    has_failure = equipment_failures_df[['cause_code', 'failure_id']].copy()
    has_failure.rename(columns={'cause_code': 'from', 'failure_id': 'to'}, inplace=True)
    has_failure.to_csv(f'{NEO4J_DIR}/rel_has_failure.csv', index=False)
    
    # MARKET_PRICE 관계 (Material -> MaterialMarket)
    market_price = material_market_df[['material_cd', 'market_id']].copy()
    market_price.rename(columns={'material_cd': 'from', 'market_id': 'to'}, inplace=True)
    market_price.to_csv(f'{NEO4J_DIR}/rel_market_price.csv', index=False)
    
    print(f"[OK] Neo4j 임포트 파일 저장 완료: {NEO4J_DIR}/")
    
    # 요약 통계
    print("\n" + "=" * 70)
    print("데이터 생성 완료 - 요약")
    print("=" * 70)
    print(f"제품: {len(products_df)}개 (EV: {len(products_df[products_df['product_type']=='EV'])}, "
          f"ESS: {len(products_df[products_df['product_type']=='ESS'])})")
    print(f"자재: {len(materials_df)}개 (단순화: 양극재, 음극재, 전해질, 분리막, 케이스)")
    print(f"BOM: {len(bom_df)}개 (제품당 5개 자재)")
    print(f"작업장: {len(work_centers_df)}개")
    print(f"라우팅: {len(routing_df)}개")
    print(f"생산오더: {len(production_orders_df)}개 (제품당 3개)")
    print(f"자재 투입: {len(material_consumption_df)}개")
    print(f"작업 실적: {len(operation_actual_df)}개")
    print(f"원가 집계: {len(cost_accumulation_df)}개")
    print(f"원가차이: {len(variance_analysis_df)}개 (PO당 3개: 재료비, 노무비, 경비)")
    print(f"\n[추가 데이터]")
    print(f"품질 불량: {len(quality_defects_df)}개")
    print(f"설비 고장: {len(equipment_failures_df)}개")
    print(f"자재 시황: {len(material_market_df)}개")
    print(f"\n[원가차이 분석]")
    print(f"  - 총 차이 금액: {variance_analysis_df['variance_amount'].sum():,.0f} 원")
    print(f"  - 평균 차이율: {variance_analysis_df['variance_percent'].abs().mean():.2f}%")
    print(f"  - HIGH 심각도: {len(variance_analysis_df[variance_analysis_df['severity']=='HIGH'])}건")
    print(f"  - MEDIUM 심각도: {len(variance_analysis_df[variance_analysis_df['severity']=='MEDIUM'])}건")
    print(f"  - LOW 심각도: {len(variance_analysis_df[variance_analysis_df['severity']=='LOW'])}건")
    print("\n[원가요소별 차이]")
    for element in ['MATERIAL', 'LABOR', 'OVERHEAD']:
        element_data = cost_accumulation_df[cost_accumulation_df['cost_element'] == element]
        total_var = element_data['variance'].sum()
        print(f"  - {element}: {total_var:,.0f} 원")
    print("=" * 70)

if __name__ == "__main__":
    main()
