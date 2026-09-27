# Retail gaze, CCTV twins, and ultrasonic cross-device tracking (uXDT)

*Overlay, compiled 2026-09-24. Lead: UwU Underground quote-tweet of Nils/@broodsugar (Auki/CactusXR) 22 Sep 2026 ([status/2102393363173691481](https://x.com/uwu_underground/status/2102393363173691481)). Treat the tweet as a lead, not a source. Primaries: Cactus/Auki product pages and 18 Sep 2026 community recap; PETS 2017 ultrasonic-beacon paper; FTC Mar 2016 SilverPush warning letters; LISNR/Shopkick vendor docs. Companions: [[spec-niantic-geospatial]], [[spec-telematics-insurance]], [[digitalid-device-ownership-erosion]], [[spec-palantir-surveillance]], [[catalog-recommended-links]].*

> **Frame.** Two layers that rhyme. **(1) 2026 product:** Auki's Cactus turns existing store CCTV + a phone-built digital twin into shelf-attention heatmaps (pose/head direction, not pupil tracking). **(2) 2014-17 stack:** ultrasonic cross-device tracking (uXDT) - inaudible 18-22 kHz tones in ads or store speakers, heard by app SDKs on phone mics, stitching TV/store/phone into one profile. The tweet's "stores shoot ultrasonic ad info to phones" is the second layer. Auki's demo is the first. They are **not the same product**. Both convert the shopper's body into merchandising data without extra dedicated hardware.
>
> **Discipline.** Vendor claims and academic/FTC records are **fact**. "This will revolutionize merchandising" is Cactus's claim. UwU's "one of us worked on this 8-ish years ago" is a **party anecdote**, not a citation. Overlay; excluded from proofs.

## 1. What the tweet actually said (party account)

Nils (@broodsugar, building with @Auki / @CactusXR) posted a demo: measure which part of a shelf gets attention using **normal CCTV** and a **digital twin made with a phone**. Cactus "will absolutely revolutionize" merchandising.

UwU Underground: one of them worked on related tech ~8 years ago using **phone signals, CCTV, BT, WiFi, 4/5G, and ultrasonic** to track movement. Fun fact: some stores shoot **ultrasonic ad info** to phones that listen - look up **Ultrasonic Tracking (uXDT)**.

Do not treat "one of us worked on it" as a source for any vendor, date, or deployment.

## 2. Cactus / Auki - CCTV into a spatial twin (fact of the product)

**Cactus** ([getcactus.ai](https://www.getcactus.ai/)) is Auki's retail copilot: phones, cameras, glasses, robots into one spatial map. Setup: QR "portals," phone-scan a 3D twin, barcode products onto shelves. Pitch: 15+ minutes saved per employee per day; **up to $500/month per location** (Auki 18 Sep 2026 recap). Built on the Auki protocol for collaborative spatial computing.

**18 Sep 2026 recap** (Auki): store cameras go into the same twin - pose, gaze, heatmap of what people look at; tie attention to SKUs and sales. If someone dwells, a robot can drive over. Merchandising: put hunted-for goods in ignored aisles. Robotics: BracketBot localized on a phone-built map; enroll next robot with a QR; Nils's number off existing customers **1,000-3,000 robots next year**; units from China and US in November.

**Honest limit on the demo:** Cactus is **not** a clinical eye-tracker. It estimates **body position + head orientation** and projects that into the twin (Fakewhale write-up 23 Sep 2026, matching Auki's own language). Accuracy depends on camera pose, lighting, calibration. Company demonstration, not a third-party accuracy audit.

**Both sides.** (A) Retailer: existing CCTV already films the floor; this is planogram ROI, not a new camera. (B) Shopper/privacy: security cameras become **always-on attention sensors** mapped to SKUs, then to robots that approach dwellers. No extra hardware is the point - the surveillance plant is already paid for.

## 3. uXDT - ultrasonic cross-device tracking (fact of the 2015-17 record)

**Mechanism:** a TV ad, webpage, or **store speaker** plays a tone in the **~18-22 kHz** band (above most adult hearing, inside phone-mic range). An app SDK with microphone permission hears it and reports the beacon, stitching **this TV / this aisle / this phone** into one advertising identity.

**Named vendors (documented):**

| Name | What | Grade |
|---|---|---|
| **SilverPush** | uXDT SDK in apps; TV-ad beacons; April 2015 claimed >18M devices. PETS 2017 reverse-engineered History GK: phone number, IMEI, Android ID, Google account, lat/long, often over **HTTP**. | **Fact** of the SDK and the paper |
| **Shopkick** | In-store ultrasonic beacons to confirm a walk-in and award points. PETS 2017: beacons in **4 of 35** stores in two European cities. Needs the app open. | **Fact** |
| **LISNR** | Radius SDK: proximity, ticketing, payments, "dynamic ad serving," retail presence. Vendor still sells this. | **Fact** of the product; "not covert tracking" is **their claim** |
| **Signal360 / CopSonic** | Same academic cluster. | **Fact** of citation |

**FTC, March 2016:** warning letters to developers of apps embedding SilverPush code that could monitor TV-ad beacons via the mic. Google Play later required disclosure of ultrasonic-beacon use. SilverPush publicly said it no longer used inaudible frequencies for smartphone ad detection. The **capability class** did not vanish - it moved into "proximity marketing" and pairing (Google Nearby / Chromecast used ultrasound among other channels to pair a phone to a TV).

**PETS 2017** (Arp et al.): 234 Android apps with ultrasonic-beacon code in a Play-store crawl; store beacons found; TV-ad beacons not found in their audio sample. That is the load-bearing measurement, not a 2026 census.

So the tweet's "some stores shoot ultrasonic ad info to phones that listen" is **true of Shopkick-class in-store beacons** (opt-in app) and **was true of SilverPush-class covert SDKs** until the FTC/Google squeeze. It is **not** a finding that Cactus uses ultrasound. Cactus's public stack is **vision + twin**. Mixing them is the lead's rhyme, not a wiring diagram.

## 4. How this sits on the map

| Layer | Object | Block |
|---|---|---|
| Phone as sensor | Mic hears beacons; later, phone builds the store twin | this block; [[digitalid-device-ownership-erosion]] |
| Cameras as sensors | CCTV -> pose/gaze -> SKU heatmap | Cactus; Niantic-class geospatial is a different camera plant ([[spec-niantic-geospatial]]) |
| Identity stitch | uXDT / LiveRamp-class people graphs | quiet-money LiveRamp/Acxiom notes |
| Car analog | Always-on phone SDK + OEM data sold to brokers | [[spec-telematics-insurance]] |
| Repair analog | Device you "own" still phones home | [[spec-rossmann-futo-ownership]] |

## 5. What is not asserted

- No claim Cactus is SilverPush, or that Auki ships ultrasonic ads.
- No claim UwU built Cactus or SilverPush. The 8-year anecdote stays unsourced.
- No 2026 census of how many stores still emit Shopkick-class tones.
- No claim the gaze heatmap identifies named shoppers. Auki's public demo is attention-in-space, not a face-to-loyalty-card join (that join would be a **separate** retailer CRM choice).
- Overlay only.

*Sources: [Cactus](https://www.getcactus.ai/); [Auki 18 Sep 2026 recap](https://www.auki.com/community/news/auki-community-update-recap-sep-18-2026); [PETS 2017 ultrasonic side channels](https://petsymposium.org/popets/2017/popets-2017-0020.pdf); [FTC SilverPush warning letters (Mar 2016)](https://www.ftc.gov/news-events/news/press-releases/2016/03/ftc-issues-warning-letters-app-developers-using-silverpush-code); [LISNR Radius](https://lisnr.com/radius-ultrasonic-sdk-3/). Lead (not a source): https://x.com/uwu_underground/status/2102393363173691481*
