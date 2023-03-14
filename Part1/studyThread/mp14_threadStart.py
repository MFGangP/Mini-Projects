# 스레드 학습
# 기본 프로세스 하나, 서브스레드 다섯개 동시에 진행
import threading
import time

# Thread를 상속받은 백그라운드 작업 클래스
class BackGroundWorker(threading.Thread):
    # 생성자
    def __init__(self, names: str) -> None:
        super().__init__()
        self._name = f'{threading.current_thread().name} : {names}'
    
    def run(self) -> None:
        print(f'BackGroundWorker start : {self._name}')
        # time.sleep(2)
        print(f'BackGroundWorker end : {self._name}')

if __name__ == '__main__':
    print('메인 스레드 시작') # 기본 프로세스 == 메인 스레드

    for i in range(5):
        name = f'서브스레드 {i}'
        th = BackGroundWorker(name)
        th.start() # run이 실행됨

    print('기본 프로세스 종료')
