# 2026-09-21 이용가이드 갱신

## 확인한 대화와 적용 기준

- `제미나이3플래시 무료티어 연동` (`01a0bdf2-b334-7233-9f97-89467b7485fb`): 최신 초안 자동 저장, 토큰·예상 요금, 직접 작성한 여러 시작 장면, 이름 기반 이미지, 채팅 하단 스탯. 9월 21일 실제 반영 내용과 완료 기록을 확인했다.
- `채팅 입력창 중복 문제 분석` (`01a0ada7-03ac-7323-86a2-9576efcbe866`): 두 채팅의 공통 입력·모델 선택·추천 답변.
- `홈 이용가이드 캐릭터 성별 적용` (`01a0a9f2-b2ae-7692-a7c7-c2fd66fb53b7`), `애셋 설정 UI 개선` (`01a0a2cd-7333-78e0-a6f5-f8ab027aa0ff`): 홈 가이드 진입, 애셋 분류, 소개 편집, 공지·알림 탭.
- `스토리챗에 메뉴 컴포넌트 적용` (`01a08b70-c6e9-7d92-ad37-d7850696097a`): 개인 설정, 가입 직후 진입, 취향 적용, 공통 설정 메뉴.
- `Estimate total input text volume` (`01a0b1ff-ce12-7b02-953c-f41c3be5a1a4`): 보상·가격 논의. 과거 대화의 Basic 35 / Deep 160과 스토리 차감 완료 주장은 현재 코드와 달라 그대로 안내하지 않았다.
- `시뮬레이터 검수 실시`의 대화 본문은 도구 조회 오류로 확보하지 못했다. 다른 대화와 구현·검증 문서로 확인 가능한 내용만 반영했다.

대화 중 제안보다 현재 코드와 최신 구현 기록을 우선했다. 기존 로컬 `guide.html` 수정 및 미완성 `create-guide.html`을 바탕으로 이어서 작성했으며, 실제로 촬영하지 않은 화면이나 실행 결과를 만들지 않았다.

## 구현 근거

기준 저장소: `../SAI` (이 Studio5 저장소의 형제 폴더).

- `Docs/Updates/2026-09-20-authoring-token-quote.md`: 자동 저장, 추정 토큰과 예상 요금, 글자 제한.
- `Docs/Updates/2026-09-21-manual-opening-scenes.md`: 상세용 공통 프롤로그, 직접 작성 시작, 탭별 저장과 새 플레이 선택.
- `Docs/Updates/2026-09-21-scene-images-and-chat-status.md`: 이미지 우선순위·중복 방지, 최신 스탯과 공개 목표.
- `SAI/Views/Create/StoryCreateViews.swift`, `SAI/Models/StoryAuthoringModels.swift`: 실제 제작 버튼·제한·예상 요금.
- `SAI/Views/Components/ConversationComposerView.swift`: 메시지 입력, 상황 설명, 이동, 모델, 추천 목록.
- `SAI/Views/Story/StoryViews.swift`, `SAI/Views/Create/StoryCastEditorViews.swift`: 이야기시작, 시작 선택, 등장 캐릭터, 이어하기.
- `SAI/Views/Chat/ConversationSettingsViews.swift`: 출력량 즉시 저장, 사용자 노트·기억의 명시적 저장.
- `SAI/Models/Models.swift`: 현재 모델 기본 비용 Basic 30 / Heart 60(할인 중, 정상120) / Deep120, 출석500→350, 21일 만료.
- `SAI/Data/SwiftDataSAIRepository.swift`: 캐릭터 메시지 차감과 스토리 행동 저장 구분. 현재 스토리 대화에는 치즈 차감이 없다.
- `SAI/Views/Home/HomeNewsPanel.swift`: 앱 소식함은 공지·알림 두 탭.

## 관련 문서와 앱 데이터

- 제작 매뉴얼, 홈페이지 진입 링크, 기존 가이드 공개 공지·피드를 함께 갱신했다. 공지 ID·최초 공개일은 보존하고 수정 시각을 추가했다. 새 앱 버전 출시를 꾸며내지 않았다.
- `SAI/SAI/Resources/hypecheese-feed.json`은 공개 피드와 일치하도록 갱신했다. 앱의 다른 진행 중 변경은 이 작업에 포함하지 않았다.
- 개인정보처리방침의 LM Studio 단독 처리 설명을 현재 Google Gemini 연결 사실로 보완했다. 앱은 공개 웹 문서를 직접 읽으므로 별도 본문 복사가 없다. 기존 가입 동의 버전과 범위는 소급 변경하지 않았다.
- 공급자 조건은 [Gemini API 약관](https://ai.google.dev/gemini-api/terms)을 2026-09-21 확인했다. 무료 서비스의 개선 활용·사람 검토 가능성을 조건부로 안내했다.

## 별도 출시 점검 사항

Gemini의 공식 약관은 18세 미만이 이용할 가능성이 있는 API 클라이언트도 제한한다. 현재 앱 가입은 14세 이상이며 실제 성인 인증 구현은 확인되지 않았다. 또한 현재 연결 프로젝트의 유료·무료 처리 조건, 처리 국가·보유기간, 동의 절차의 확정은 웹 사용법 정정만으로 완료되지 않는다. 이 작업에서 앱 가입 조건이나 기존 동의 기록을 임의로 변경하지 않았다.

시스템 단축어, 작가 시험 결과 화면, 정확한 서버 토큰 계측, 실제 용량 추가 과금·캐싱은 완료된 사용 기능으로 소개하지 않았다.

## 검증

- `python3 scripts/render-hypecheese-feed.py`
- `python3 scripts/check-hypecheese.py`: 경로·앵커, 문서 구조, 이미지 속성, 피드·공지 일치, 정책 기준 버전 검사.
- `git diff --check`
- 브라우저에서 1280px 데스크톱·390px 모바일 레이아웃, 목차, 제작 가이드 링크, 예시 복사를 확인했다. 가로 넘침·깨진 이미지·브라우저 오류가 없었다. 기존 Vercel 프로젝트의 main 자동 배포를 사용한다.
