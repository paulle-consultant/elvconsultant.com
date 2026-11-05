# Diamond Controls product facts (source of truth for BMS posts)

Source: Mitsubishi Electric Asia, "Catalog Diamond Controls" (2023) and "DCM-8044/DCM-8044-D with IO Modules" (2024), supplied by Paul Le. Only state specs listed here. Anything else: say "theo datasheet hãng" without a number, or look it up on an official Mitsubishi Electric / Tridium page and cite it.

## Platform
- Diamond Controls = Mitsubishi Electric Asia BMS line built on Tridium Niagara Framework.
- Mitsubishi Electric Vietnam BMS offer: ICONICS GENESIS (energy management, alarms, FDD, carbon reporting), Niagara N4, PLC and DDC controllers, inverters. Vendor claim: centralised management can cut energy use up to 30%; supports LEED, WELL, EDGE, LOTUS. https://buildingsolutions.mitsubishi-electric.vn/en/bms/

## DCM 9000 (Niagara 4.13+)
- NXP i.MX8M+ quad core, 2 GB LPDDR4, 8 GB micro-SD, Wi-Fi 5 (client/WAP/off), USB-C debug.
- 2 isolated RS-485 (selectable bias/termination), 2 × 10/100/1000 Ethernet, secure boot, batteryless RTC.
- 24 VAC 24 VA min or 24 VDC 1 A (24 W) min. Operating -20 to 60 °C, 5–95% RH non-condensing, MTTF 10 years+.
- Certs: UL 916, C-UL, CE EN 61326-1, RCM, FCC Part 15, RoHS, CCC, Open Energy Management Class 2.
- Expansion: up to 4 modules (NPB-8000-LON ×4, NPB-8000-232 ×4, NPB-8000-2X-485 ×2). IO: up to 16 IO-R-16 or 8 IO-R-34; one IO-R-34 powers four IO-R-16.
- IO-R-16: 8 UI, 4 Form A relay DO, 4 AO 0–10 VDC. IO-R-34: 16 UI, 10 relay DO, 8 AO 0–10 VDC.
- Licences: DCM-9005 (5 devices/250 points), DCM-9010 (10/500), DCM-9025 (25/1,250), DCM-9100 (100/5,000), DCM-9200 (200/10,000); upgrades DEVICE-10/25/50; DCM-9000-DEMO (500 devices, non-production). All Tridium drivers included on 9005–9200.
- Accessories: WPM-8000 power supply. DIN rail EN50022 35 mm, DIN43880 enclosures.

## DCM 8000 (Niagara AX 3.8u1+ / Niagara 4.1+)
- TI AM3352 1 GHz Cortex-A8, 1 GB DDR3, micro-SD 4 GB (2 GB user), Wi-Fi 802.11a/b/g/n, USB-A, 2 isolated RS-485, 2 × 10/100 Ethernet, secure boot.
- Up to 4 expansion modules (232/LON/485). Same environment and certs class as DCM 9000 (UL 916, CE, FCC, RCM, CCC, RoHS).

## DCM-8446 (RS-485 DDC)
- 22 points: 8 UI, 4 DI, 4 AO, 6 DO. ARM Cortex 32-bit, fully programmable, HVAC logic, timer, alarm handler, RTC with CR1220 battery, password.
- UI: 0–10 V / 0–5 V (±0.01 V), 4–20 / 0–20 mA (±0.01 mA), 0–50 kΩ, NTC 10K type 2/3, 3K, 20K (±0.1 °C), true DI. 12-bit ADC with PGA.
- DI: dry contact, non-isolated. DO: relay SPST NO 30 VDC 1 A / 125 VAC 0.5 A. AO: 12-bit, 0–20/4–20 mA (max 500 Ω), 0–10 V.
- 1 × RS-485, BACnet MS/TP (9.6–76.8 kbps) or Modbus RTU (9.6–115.2 kbps).
- 24 VAC ±5% or 24 VDC +20/-10%, <10 W. 0–55 °C. 166 × 134 × 62 mm, 365 g, UL94 ABS+PC.
- Combos (30 points): +IO-0800 → 8AI/12DI/4AO/6DO; +IO-6020 → 14AI/4DI/6AO/6DO; +IO-0008 → 8AI/4DI/4AO/14DO.
- GW-112 (left slot) makes it an IP controller: 2 × RS-485, 1 × 10/100 Ethernet, BACnet IP / Modbus TCP, web config. COM1: MS/TP / RTU / Modbus master (max 4 devices of 8446 series). COM2: Modbus bridge or BACnet router (max 32 devices). Niagara 4 can download programs via APM (Advanced Programming Module).

## Remote IO (RS-485, BACnet MS/TP or Modbus RTU, DIP address)
- IO-0800-485: 8 DI dry contact isolated 3.7 kV.
- IO-6020-485: 6 UI (12-bit PGA) + 2 AO.
- IO-0008-485: 8 DO relay SPST NO 30 VDC 1 A / 125 VAC 0.5 A.
- 24 VAC ±5% / 24 VDC, <10 W, 86 × 134 × 62 mm, 183 g.

## DCM-8044 / DCM-8044-D (IP DDC, -D has LCD)
- 16 points: 8 UI, 4 DO, 4 AO. Certs CE, FCC, BTL. RTC with battery.
- UI: 0–10/0–5 V, 4–20/0–20 mA, 0–30k/0–10k/0–1.5k Ω, NTC 10K type 2/3, 3K, 20K; true DI by jumper. DO relay SPST NO 24 VAC/DC 1 A. AO 0–20/4–20 mA (max 800 Ω), 0–10 V.
- RS-485: Modbus RTU / BACnet MS/TP, 9.6–115.2 kbps. Ethernet 10/100: BACnet IP, Modbus TCP, HTTP/FTP.
- Roles: Modbus master (max 4 devices: DCM-8446, IO-0008/0800/6020-485), Modbus bridge, BACnet router. Basic APM programming.
- Expansion (right slot, one module): IO-V6002 (6 UI + 2 DO), IO-V0800 (8 DI).
- 24 VAC +20/-15% or 24 VDC ±5%, <10 W, 0–55 °C, 151 × 116 × 40 mm, 500 g.
- Max combos: 8044+IO-V6002+4×DCM8446 = 46 UI/16 DI/20 AO/28 DO; 8044+4×IO-0008 = 8 UI/0/4 AO/36 DO; 8044+4×IO-0800 = 8 UI/32 DI/4 AO/4 DO.

## Market and regulation facts already verified (Nov 2026)
- Vietnam building automation market ≈ USD 221 M (2025), 243 M (2026), 312 M (2032), CAGR 4.25%; Honeywell, Siemens, Schneider, JCI, ABB ≈ 40% share. Source: MarkNtel Advisors.
- Law 77/2025/QH15 (amends energy efficiency law), effective 1 Jan 2026: designated energy users keep compliant metering, energy balance, annual and 5-year plans; ESCO defined; green credit incentives. Source: LuatVietnam.
- Daikin agreed to acquire HCMC BMS integrator Anh Nguyen (Dec 2025). Source: Refindustry.
- QCVN 09:2017/BXD: energy-efficient buildings code, buildings ≥ 2,500 m².
