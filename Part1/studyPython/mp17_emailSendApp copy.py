# 이메일 보내기 앱

import smtplib # SMTP 단순 전자우편 전송 프로토콜
from email.mime.text import MIMEText # 대용량 이메일 전송 확장자 규약 (이미지, 글)

send_email = '이메일'
send_pass = '비밀번호'

recv_email = '이메일'

smtp_name = 'smtp.naver.com'
smtp_port = 587 # 이메일이 지나가는 고속도로

text = ''' 이걸 여시다니 이번만 봐드렸습니다. 행복하세요 ♥ '''

msg = MIMEText(text)
msg['Subject'] = '회사에서 보면 큰일남!'
msg['From'] = send_email # 보내는 메일
msg['To'] = recv_email # 받는 메일
print(msg.as_string())

mail = smtplib.SMTP(smtp_name, smtp_port) # SMTP 객체 생성
mail.starttls() # 전송 계층 보안 시작
mail.login(send_email ,send_pass)
mail.sendmail(send_email, recv_email, msg=msg.as_string())
mail.quit()
print('전송완료!')