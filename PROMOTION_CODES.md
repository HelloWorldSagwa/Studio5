# 결제선언 자체 프로모션 코드 운영

웹 활성화 주소: `https://studio5-ashy.vercel.app/paymentdeclaration/activate/`

Apple과 카카오 계정은 연결하지 않는다. 사용자가 웹에서 로그인한 정확한 Supabase `auth.uid()` 한 개에만 이용권이 적용된다.

## 1. 캠페인 만들기

Supabase SQL Editor에서 실행한다. `access_kind`는 기간제 `duration` 또는 평생 `lifetime`이다.

### 1년 + 창립 후원자

```sql
insert into schema_1.promotion_campaigns (
  slug,
  name,
  description,
  access_kind,
  duration_days,
  grants_founding_supporter
) values (
  'tumblbug-founder-1y-2026',
  '텀블벅 창립 후원자 1년 이용권',
  '텀블벅 후원자용 1년 이용권과 창립 후원자 배지',
  'duration',
  365,
  true
)
returning id;
```

### 평생 + 창립 후원자

```sql
insert into schema_1.promotion_campaigns (
  slug,
  name,
  description,
  access_kind,
  duration_days,
  grants_founding_supporter
) values (
  'tumblbug-founder-lifetime-2026',
  '텀블벅 창립 후원자 평생 이용권',
  '텀블벅 후원자용 평생 이용권과 창립 후원자 배지',
  'lifetime',
  null,
  true
)
returning id;
```

## 2. 일회용 코드 발급

캠페인 ID와 수량을 넣는다. 아래 예시는 100개를 만들며, 출력된 코드 원문은 이때 한 번만 보인다. 결과를 즉시 CSV로 안전하게 보관한다.

```sql
select *
from schema_1.generate_promotion_codes(
  '<campaign-id>'::uuid,
  100,
  now(),
  '2027-12-31 23:59:59+09'::timestamptz
);
```

DB에는 코드 원문이 아니라 SHA-256 해시만 저장된다. 코드는 `PD-XXXX-XXXX-XXXX-XXXX-XXXX` 형식이며 한 번만 사용할 수 있다.

## 3. 캠페인 또는 코드 중지

아직 쓰지 않은 캠페인 전체를 중지한다.

```sql
update schema_1.promotion_campaigns
set is_active = false,
    updated_at = now()
where slug = '<campaign-slug>';
```

특정 미사용 코드를 중지할 때는 코드 발급 결과의 `generated_code_id`를 사용한다.

```sql
update schema_1.promotion_codes
set revoked_at = now()
where id = '<generated-code-id>'::uuid
  and redeemed_at is null;
```

## 4. 이미 부여한 이용권 취소

지원 문의 등으로 특정 활성화 건을 취소해야 할 때만 사용한다.

```sql
update schema_1.promotion_entitlements
set revoked_at = now()
where code_id = '<generated-code-id>'::uuid
  and revoked_at is null;
```

`promotion_entitlements` 변경은 앱의 실시간 동기화 신호에도 반영된다.
