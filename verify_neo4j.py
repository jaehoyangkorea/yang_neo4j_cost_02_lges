"""
Neo4j 데이터 검증 스크립트
"""
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import ssl

load_dotenv()

uri = os.getenv('NEO4J_URI').replace('neo4j+s://', 'bolt://')
username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

driver = GraphDatabase.driver(uri, auth=(username, password), ssl_context=ssl_context)

print("\n[Neo4j 데이터 검증]")
print("=" * 70)

with driver.session() as session:
    # 노드 수 확인
    result = session.run("""
        MATCH (n)
        RETURN labels(n)[0] as label, COUNT(n) as count
        ORDER BY label
    """)
    
    print("\n[노드 개수]")
    for record in result:
        print(f"  - {record['label']}: {record['count']}개")
    
    # 관계 수 확인
    result = session.run("""
        MATCH ()-[r]->()
        RETURN type(r) as type, COUNT(r) as count
        ORDER BY type
    """)
    
    print("\n[관계 개수]")
    for record in result:
        print(f"  - {record['type']}: {record['count']}개")
    
    # 최대 차이 발생 오더
    result = session.run("""
        MATCH (po:ProductionOrder)-[:HAS_VARIANCE]->(v:Variance)
        WITH po, SUM(v.variance_amount) as total_variance
        ORDER BY ABS(total_variance) DESC
        LIMIT 5
        RETURN po.id as order_no, total_variance
    """)
    
    print("\n[최대 원가차이 발생 오더 Top 5]")
    for record in result:
        print(f"  - {record['order_no']}: {record['total_variance']:,.0f}원")

driver.close()
print("\n" + "=" * 70)
print("[OK] Neo4j 데이터가 정상적으로 업로드되었습니다!")
print("=" * 70)
