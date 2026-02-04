"""
원가 분석 데이터 생성기 - 시나리오 선택

사용법:
  python data/generate_data_selector.py battery      # 배터리 데이터 생성
  python data/generate_data_selector.py semiconductor # 반도체 데이터 생성
"""

import sys
import os

def main():
    if len(sys.argv) < 2:
        print("=" * 70)
        print("원가 분석 데이터 생성기")
        print("=" * 70)
        print("\n사용법:")
        print("  python data/generate_data_selector.py battery      # 배터리 시나리오")
        print("  python data/generate_data_selector.py semiconductor # 반도체 시나리오")
        print("\n시나리오 설명:")
        print("  - battery: LG에너지솔루션 배터리 제조 (EV, ESS)")
        print("  - semiconductor: 반도체 패키징 (QFP, BGA, SOP 등)")
        sys.exit(1)
    
    scenario = sys.argv[1].lower()
    
    if scenario == 'battery':
        print("\n🔋 배터리 시나리오 선택됨")
        print("=" * 70)
        import generate_data_battery
        generate_data_battery.main()
        
    elif scenario == 'semiconductor':
        print("\n🔌 반도체 시나리오 선택됨")
        print("=" * 70)
        import generate_data_semiconductor
        generate_data_semiconductor.main()
        
    else:
        print(f"✗ 알 수 없는 시나리오: {scenario}")
        print("  'battery' 또는 'semiconductor'를 입력하세요.")
        sys.exit(1)

if __name__ == "__main__":
    main()
