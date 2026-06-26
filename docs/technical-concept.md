# Pathbox — Technical Concept

_Last updated: 2026-06-26_

See [repositioning.md](./repositioning.md) for the product strategy this supports.

## Design principle

The app does exactly one thing — log location in the background and hand you a
link. Everything hard is in **background-location reliability**, not features. Spend
the engineering budget there and keep the rest trivial.

## Stack

| Layer | Choice | Why |
|---|---|---|
| **Tracker app** | **Flutter**, single codebase → iOS + Android | One language, native background location, real app-store presence. A PWA can't track in the background on iOS, which disqualifies it. |
| **Background location (the hard part)** | `flutter_background_geolocation` (Transistorsoft) | Battle-tested. Handles iOS "Always Allow", Android 10+ background permissions, motion-triggered logging, battery management, and aggressive OEM battery-killers. This library *is* the product's reliability. |
| **Backend** | **Keep** Flask on Cloud Run + Firestore | Already works, near-zero ops. Add 2 endpoints. |
| **Viewer** | **Keep** server-rendered map at `/v/<token>` | Viewer needs no app and no account — a core selling point. Don't touch it. |

## Costs / licensing

- **`flutter_background_geolocation` (Transistorsoft): USD 399 one-time license.**
  This is the key paid dependency. It is what makes background tracking actually
  "just work" across iOS and Android; building this reliability in-house would cost
  far more in engineering time.
- Backend (Cloud Run + Firestore): existing, usage-based, negligible at low volume.

## Identity model (unchanged — already correct)

On first launch the app generates a random `device_token` (secret, used to **write**)
and a derived `public_token` (used in the share link to **read**). No account, no
email. The share link *is* the identity.

## Minimal functionality (the entire app)

- **One screen:** a large Start/Stop toggle + a status line ("Tracking on · synced 2 min ago").
- **One button:** "Share tracking link" → shows / copies the link.
- **One onboarding flow:** the permission walkthrough (iOS "Always Allow", Android
  background location + battery-optimization exemption). Getting this right is ~80%
  of "just works".
- **Settings:** delete my data, history retention.

## Backend changes (small)

```
POST   /api/v1/locations     # batched points, auth by device_token
GET    /v/<public_token>     # existing map viewer — unchanged
DELETE /api/v1/data          # self-serve wipe (closes the privacy gap)
```

Plus a Firestore TTL policy to auto-expire old points (retention limit = privacy
feature + cost control).

## Explicitly NOT in v1

Geofence alerts, SOS button, multiple devices, fall detection, native viewer app,
GPX export. All are post-validation. v1 = log + view + delete.

## The one real risk

Background location that survives reboots, OS battery optimization, and aggressive
Android OEMs is *the* engineering challenge — not the UI. The Transistorsoft library
de-risks it (see USD 399 cost above) but isn't free. Everything else is small.

## Migration note

This replaces the existing Android-only app (`de.casparwre.gpslogger`) with one
Flutter app reusing the current backend — so iOS comes for free and the biggest
market gap from the repositioning doc is closed.
