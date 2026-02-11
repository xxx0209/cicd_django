from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

# Role 상수 정의
ROLE_CHOICES = [
    ('USER', '일반 회원'),
    ('ADMIN', '관리자'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # User와 1:1 관계
    address = models.CharField(max_length=255, blank=False, verbose_name="주소")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    regdate = models.DateField(default=timezone.now, verbose_name="등록 일자")

    # 추가 유효성 검증 예시
    password_validator = RegexValidator(
        regex=r'^(?=.*[A-Z])(?=.*[!@#$%]).{8,255}$',
        message='비밀번호는 8자리 이상, 대문자 1개 이상, 특수문자(!@#$%) 포함해야 합니다.'
    )


    class Meta:
        db_table = "profiles"

    def __str__(self):
        return f"{self.user.username} - {self.role}"
