from function import Simulator, HTMLContent

print("[INFO] 성적 계산 중... ")
simulator = Simulator()
grade = simulator.get_grades()

print("[INFO] 웹 페이저 생성 중... ")
html = HTMLContent(grade)
html.open()

print("[INFO] 종료 대기 중...\n")