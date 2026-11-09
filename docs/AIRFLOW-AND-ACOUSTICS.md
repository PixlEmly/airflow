# Airflow and acoustic screening

## Basis and current result

Main enclosure design allowance is 9,900CFM = 3 x 3,300CFM, conservatively above actual according to user. No measured static pressure or fan curves. Separate six-inch silencer duct excluded. All quoted velocities assume the full total passes uniformly across the full clear width; local jets, ground/tree effects and nonuniform utilization are unresolved.

Current lined finished width 92.88in, half-depth opening 8.86in; A=W*g/144=5.713ft2. V=Q/A=1,733fpm. Previous baffles already included face-lining allowance, so do not add another two inches to their 80mm thickness. Wall/end lining reduced area by 12.0%. Actual narrow paths at hood inlet, turns and discharge can govern performance beyond this nominal section.

At standard air density, velocity pressure Pv=(V/4005)^2 = 0.187in water. An estimated fitting loss would be deltaP=K*Pv. K=1,3,5 would give 0.19,0.56,0.94in water ONLY AS SENSITIVITY EXAMPLES. These are not validated coefficients, not a claimed plausible range, not total system pressure predictions and not fan backpressure limits. Losses require coefficients referenced to appropriate local velocities plus friction and system effects. Ambient density and actual exhaust temperature affect pressure. At similar flow pattern, halving Q quarters pressure loss. Actual delivered Q is determined by each fan curve and connected system.

## Bottom opening versus vent area

| Opening | Geometric area |
|---|---:|
| Two nominal 10-inch round vents | 1.09 ft² combined |
| Large hood's modeled downward outlet (0.52 × 0.28 m) | 1.57 ft² |
| Combined area served by the enclosure | 2.66 ft² |
| Option 4 clear bottom opening | 5.71 ft² |

The lowest baffle sits flush with the base and occupies half of the 11.43 ft² lined footprint. The remaining slot is 92.88 × 8.86 inches, or about 2.15 times the combined area of the three vents it serves. Including the separate 6-inch roof duct adds 0.20 ft², bringing the all-vent tally to 2.85 ft². That duct bypasses the enclosure.

The hood outlet is a model estimate. This comparison uses geometric area. Pressure loss also depends on the baffle turns and the discharge path beneath the enclosure.

## Separate 6-inch duct extension

Fan identified by the user as Kemper 92104131 (92 104 131). Confirm the branch it serves. The [exact-part reseller listing](https://weldingmart.com/products/kemper-exhaust-fan-115v-1250-cfm-1-5hp-92104131) identifies a 115 V, 60 Hz, 1.5 hp unit and gives conflicting airflow figures (1,140 CFM in the specifications and 1,250 CFM in the title). Request the exact 60 Hz pressure-flow curve from Kemper. Installed airflow and available pressure remain unverified. The enclosure's 9,900 CFM allowance applies separately.

For a proposed 20-foot soffit run, using 6-inch ID, standard-density air, Darcy friction factor 0.02 and one additional elbow with illustrative K=0.5:

| Branch airflow | Added straight-run loss | Added loss with one extra elbow |
|---:|---:|---:|
| 200 CFM | 0.052 in. water | 0.084 in. water |
| 400 CFM | 0.207 in. water | 0.336 in. water |
| 800 CFM | 0.828 in. water | 1.345 in. water |

Count any additional corner and vertical run length. If an existing elbow is relocated, count the change in fitting loss. These estimates exclude silencer loss and describe added pressure at fixed flow. See [ASHRAE duct design](https://handbook.ashrae.org/Handbooks/F25/IP/F25_Ch21/F25_Ch21_ip.aspx).

Measure branch CFM and static pressure at a flush wall tap just upstream of the extension, referenced to sheltered outdoor air. Repeat with a temporary extension at the same fan speed and load. Two static taps across the fan measure static pressure rise. Check pressure definitions and velocity pressure corrections before comparing with a published curve. For hot engine exhaust, follow the equipment manufacturer's pressure tap location, test load and allowable backpressure.

## Other options

Only 4 is internally designed. To screen alternatives, retain 80mm lined baffles and assume all three lie below the lowest modeled hood outlet (Z=1.184m). An optimistic vertical gap bound is (hoodZ-base-3*thickness)/2, leaving ZERO hood-approach clearance and bottom baffle flush with base. This is not an acceptable finished layout, but shows the available space: option1 3.58in; option2 0.58in; option3 6.58in. Option4 has enough vertical room for its 8.86in tip gaps. Option5 has about 7.89in tips and nominal 1,946fpm. Greater opening under the box can coexist with worse restriction within it.

Restoring previous nominal area with current lined width needs 10.07in clear tip and vertical gaps. Symmetric half-depth geometry plus 1in front/back lining would require bare interior depth22.14in, about2.42in more than current. This affects tree clearance. Smaller baffle projection could enlarge tips without more depth but may open a direct sound path; it is not a free improvement.

## Acoustic status

The [Rotax dyno noise baseline](ROTAX-NOISE-BASELINE.md) records the user's rough peak readings, outlet identities and test conditions.

See the [current reference report](../XLR8-option-4-acoustic-construction-review.pdf) for the octave-band screening calculations and the separate LD6 ratings. No installed reduction has been measured. Half-depth tips have no overlap. Orientation reversal preserves nominal area and turn count but changes inlet/outlet alignment; current orientation is a provisional geometric preference, not a measured acoustic advantage. Need source spectrum, receiver location, reduction target, actual acoustic lining data and casing leakage/transmission assumptions. Low-frequency performance cannot be inferred from high-frequency absorption or bend count. Sound generated by turbulent flow also contributes.

The specified Option 4 lining is 1-inch Owens Corning Type 703 Fiberglas with FRK facing. The manufacturer's published sound absorption coefficients are:

| 125 Hz | 250 Hz | 500 Hz | 1 kHz | 2 kHz | 4 kHz | NRC |
|---:|---:|---:|---:|---:|---:|---:|
| 0.18 | 0.75 | 0.58 | 0.72 | 0.62 | 0.35 | 0.65 |

These are material absorption coefficients, so they cannot be added to the LD 6 silencer's dB ratings or used as enclosure insertion loss. The 250 Hz band includes the suspected 244 Hz component. Confirm facing orientation, retention and suitability for the actual airflow, temperature and moisture before installation. [Owens Corning 700 Series submittal](https://ww2.owenscorning.com/comminsul/documents/Fiberglas700Series.pdf)

## References consulted

- [AMCA, pressures in a ventilation/fan system](https://www.amca.org/assets/resources/public/assets/uploads/FINAL-_Pressures_in_a_Ventilation_and_Fan_System.pdf): operating point and system losses.
- [CaptiveAire, air systems design](https://www.captiveaire.com/manuals/airsystemdesign/designairsystems.htm): velocity pressure formula.
- [ASHRAE, Fans](https://handbook.ashrae.org/Handbooks/S24/IP/S24_Ch21/S24_Ch21_ip.aspx): matching fan pressure to system requirements.
- [ASHRAE, noise and vibration control](https://handbook.ashrae.org/Handbooks/A23/IP/A23_Ch49/a23_ch49_ip.aspx): insertion loss, system effects, pressure drop and generated sound.
- [Johns Manville SuperDuct RC](https://www.jm.com/content/dam/jm/global/en/insulation-systems/products/assets/data-sheet/jm-hvac-superduct-rc-ds-en.pdf): example distinction between FSK exterior and coated airstream surface. This is an example, not the selected FRK product.

Independent testing, manufacturer data or a qualified airflow/acoustic evaluation is needed before treating dimensions as final.
