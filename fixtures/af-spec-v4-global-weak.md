# CopyRight Shield v4.0 — Global Platform Spec

## 1. 목표
AI 생성 콘텐츠 저작권 안전 엔진을 한국 1위에서 세계적 B2B 플랫폼으로.

## 4. Phase 로드맵 (PRD 이후 18주)

### Phase 5 — Trust Foundation (3주)
- Multi-tenant 데이터 모델 — Org / User / ApiKey / AuditLog
- 인증 마이그레이션 — SITE_PASSWORD → OAuth (Google Workspace + Logto)
- Privacy 정책 — FERPA / GDPR / 한국 개인정보보호법

### Phase 6 — Public API v1 (3주)
- OpenAPI 3.1, API key UI, Rate limiting, Webhook, TypeScript SDK, Developer docs

### Phase 7 — LMS Integration (4주)
- LTI 1.3, Canvas, Google Classroom, Microsoft Teams Education, Schoology, SAML SSO

### Phase 8 — Corpus Marketplace (4주)
- 출판사 onboarding + KYC, Stripe Connect, AES-256-GCM, DRM access control

### Phase 9 — Compliance + GTM (4주)
- SOC 2 Type II 감사 시작, FERPA attestation, GDPR DPA, 한국 ISMS-P 검토

## 5. 가격 (App Factory 추정)
학원 ₩50–200만/년, 출판사 ₩500–2000만/년 (가정)

## 6. 다음 CLI 명령
```bash
app-factory implement --tier builder-mini-behavior \
  --modules "jtbd,mab,northstar,..." \
  --feature-focus "phase 5 trust foundation"
```

## 7. North Star
"월간 A등급 인증 건수: 1년차 50,000 / 3년차 1,000,000"

## 9. F23 — Secret Scan CI (병렬 트랙)
[section copy-pasted from another project — copyright-cleansing has no .github/workflows yet]
