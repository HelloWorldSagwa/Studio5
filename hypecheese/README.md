# HYPE CHEESE static section

Existing Studio5 repository and Vercel deployment are retained. No web framework, runtime database, analytics package, new hosting project, or new account form was added.

## Public paths

- `/hypecheese/`: introduction and document directory
- `/hypecheese/guide.html`: current local-test product guide
- `/hypecheese/terms.html`: terms
- `/hypecheese/privacy.html`: privacy notice
- `/hypecheese/collection.html`: separate signup collection/use consent
- `/hypecheese/marketing.html`: separate optional marketing-push consent
- `/hypecheese/notices/`: public notices
- `/hypecheese/updates/`: published app-version changes; currently empty
- `/hypecheese/feed.json`: shared public source consumed by the app

All policy documents carry `2026-09-14-local-v1`, effective and last-modified date September 14, 2026, and explicitly apply to the current local test. These are not an assertion that cloud processing, paid product release, or the full production legal review has been completed. App consent records must store the version actually accepted; do not retroactively rewrite older accepted versions.

## Publishing a notice or update

Edit `feed.json`, keeping stable IDs for existing entries. `publishedAt` and `updatedAt` are ISO 8601 UTC timestamps. Public detail URLs must stay on `https://studio5-ashy.vercel.app/hypecheese/`.

For notices, put the article paragraphs in `content/<id>.json`; the shared feed provides the title, summary, category, date, and URL. The optional `link` is an internal HYPE CHEESE path. For updates, use `version` and `changes` with `added`, `improved`, and `fixed` string arrays in the feed. Only record released versions and actual changes. Empty updates are intentional, not placeholder releases.

Run from the repository root:

```sh
python3 scripts/render-hypecheese-feed.py
python3 scripts/check-hypecheese.py
```

Commit the feed, content, generated list/detail HTML, and the app's matching bundled fallback together when publication changes. No JavaScript is required to read any document. The feed is public: never add personal notification contents, user IDs, chat text, or private account data.

The general guide and policy HTML are edited directly. `scripts/hypecheese_layout.py` is the shared shell used for generated news pages; keep navigation/footer consistent when updating static document pages.

## Reference lock and content evidence

- Primary visual target: the existing HYPE CHEESE app and supplied dark hamburger screenshot. Preserve near-black canvas, white headings, orange action/brand accent, restrained gray separators, and the actual existing app icon.
- Secondary target: existing Studio5 project cards and document pages. Keep the Projects structure, shared project-card classes, navigation back to Studio5, and familiar policy metadata.
- Craft references: Refero `typography.md` and `craft-details.md`: short line lengths, readable Korean body type, semantic headings and tables, visible keyboard focus, mobile tap targets, anchors, reduced-motion support, and print reading.
- Assets: the app's existing `hype-cheese-app-icon.png`, copied unchanged. No QA transcripts, personal screenshots, generated model samples, or hidden prompt resources are published.
- Current app sources reviewed: `Models.swift` (memory sections, output/token and cost settings); `SwiftDataSAIRepository.swift` (room scopes, local data, attendance); `StoreKitSayPurchaseService.swift` (test/real purchase distinction); `StoryCoverGenerationService.swift` and public `LMStudioChatService.swift` boundaries (AI transfer); `SignupLegalDocumentView.swift` (local policies and consent roles). The private common prompt resource was not opened.
- Public operator source: existing Studio5 `index.html` and `paymentdeclaration/privacy.html` at baseline commit `aff7695`, confirming Studio5 / 김성현 / 897-78-00494 / 2024-부산진-1049 / studiofiveteam@gmail.com. No unverified business address or phone number was invented.
- Legal primary references checked 2026-09-14: [Personal Information Protection Act Art. 30](https://www.law.go.kr/lsLinkCommonInfo.do?lsJoLnkSeq=1029331583), [Act on Consumer Protection in Electronic Commerce](https://www.law.go.kr/lsInfoP.do?ancYnChk=0&lsId=009318). These guide disclosure structure and preserve statutory cancellation/refund rights; no arbitrary retention periods or blanket refund exclusion were created.

The current LM Studio endpoint may use HTTP and logs/retention are not established by client code. The notice discloses that limit. A future cloud model, hosting/processor arrangement, export, retention period, learning use, or paid product requires concrete processing terms and a corresponding policy/consent update before introduction.

Additional primary references checked: [Information and Communications Network Act Art. 50(3), separate night-marketing consent](https://law.go.kr/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1030434421), [KISA privacy reporting contact](https://privacy.kisa.or.kr/).
