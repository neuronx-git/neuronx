# NeuronX Brand Guide

**Version**: 1.0
**Date**: 2026-04-11
**Status**: CANONICAL

---

## Brand Hierarchy

NeuronX is the **SaaS product**. Clients (VMC, etc.) have their **own branding**.

| Entity | Branding Applies To | Who Controls |
|--------|-------------------|-------------|
| NeuronX (SaaS) | Marketing website, admin tools, Chrome extension, docs | NeuronX team |
| VMC (Client) | Intake forms, emails, SMS, landing pages, client-facing UI | Per-tenant config |

---

## NeuronX Brand Identity (SaaS Provider)

### Colors
| Token | Hex | Usage |
|-------|-----|-------|
| **Navy** | `#0F172A` | Primary background, headers, text |
| **Coral** | `#E8380D` | Primary CTA, accents, highlights |
| **Gold** | `#D9A651` | Secondary accents, premium feel |
| **Cream** | `#FFFBF5` | Page background, cards |
| **Slate** | `#64748B` | Secondary text, muted content |
| **White** | `#FFFFFF` | Text on dark backgrounds |

### Typography
- **Font**: Inter (Google Fonts)
- **Headings**: Inter Bold (700)
- **Body**: Inter Regular (400)
- **UI Labels**: Inter Medium (500)

### Logo
- Square mark: Navy rounded rectangle with "NX" in coral
- Text logo: "NeuronX" in Inter Bold, navy color
- Favicon: Navy square with "N" in blue + emerald dot

### Design Principles
- Cream/coral palette inspired by Karbon (professional services SaaS)
- Rounded corners (2xl = 16px for cards, full for buttons)
- Subtle shadows (shadow-lg for hover states)
- Framer Motion animations (fade-in, slide-up)
- Mobile-first responsive design

---

## Client Branding (Per-Tenant)

Each client gets their own branded forms, emails, and landing pages.

### VMC (Visa Master Canada) — Pilot Client
| Token | Hex | Usage |
|-------|-----|-------|
| **Primary** | `#1E3A5F` | Chat bubbles, buttons, header |
| **Accent** | `#E8380D` | User responses, highlights |
| **Background** | `#F8FAFC` | Form background |

### How to Brand a New Client
1. Add entry to `neuronx-api/config/tenants.yaml`
2. Upload avatar to `neuronx-api/static/avatars/{slug}.png`
3. Set colors, bot name, GHL location ID
4. Push to GitHub → form automatically live at `/form/{slug}/onboarding`

---

## Where Branding Is Applied

| Asset | Brand | Config Source |
|-------|-------|--------------|
| neuronx.co website | NeuronX | `neuronx-web/` hardcoded |
| Chrome extension | NeuronX | `chrome-extension/popup.html` |
| `/form/{tenant}/onboarding` | Client (per tenant) | `config/tenants.yaml` |
| GHL emails/SMS | Client | GHL templates |
| VAPI voice agent | Client | VAPI assistant config |
| Metabase dashboards | NeuronX | Metabase theme settings |

---

## Note on APP/ Branding Kit

The file `APP/libs/ui-design-system/src/theme/branding-kit.ts` uses Blue #3b82f6 as primary.
This is the **legacy v1 reference codebase** (per CLAUDE.md: "reference only, not the build path").
The current NeuronX brand uses Coral #E8380D as primary.
If APP/ is ever resurrected, update `branding-kit.ts` to match this guide.
