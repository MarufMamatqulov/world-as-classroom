"""
Pedagogical knowledge base providing comprehensive curriculum data across Physics,
Chemistry, Biology, Mathematics, History, and Technology for detected classroom objects.
Supports Uzbek, English, and Russian.
"""

MOCK_CATALOG = {
    "bicycle": {
        "en": {
            "name": "Bicycle",
            "name_en": "Bicycle",
            "category": "Transport & Mechanical Physics",
            "educational_hook": "A bicycle is a human-powered marvel that perfectly demonstrates Newton's laws, gear ratios, and biomechanics in action!",
            "subjects_list": ["Physics", "Mathematics", "Biology", "Chemistry", "Technology", "History"],
            "title": "The Physics & Engineering of the Bicycle",
            "summary": "Every time you pedal a bicycle, you turn chemical energy from your muscles into mechanical kinetic energy. From the balance of angular momentum in the wheels to the mechanical advantage of the gear derailleur, the bicycle is an open-air laboratory on wheels.",
            "modules": [
                {
                    "subject": "Physics",
                    "title": "Mechanics, Friction, and Energy Conversion",
                    "icon": "Atom",
                    "concepts": [
                        {
                            "headline": "Mechanical Advantage & Gear Ratios",
                            "explanation": "When the front chainring with 48 teeth drives a rear cog with 16 teeth, one pedal turn rotates the wheel 3 times (48/16 = 3:1 ratio). This trades pedal force for speed on flat roads.",
                            "formula": "Gear Ratio = N_front / N_rear",
                            "real_world_example": "Shifting to a smaller front gear when climbing steep hills reduces required pedal torque."
                        },
                        {
                            "headline": "Friction: The Essential Grip",
                            "explanation": "Static friction between rubber tires and asphalt propels the bike forward, while rolling resistance is minimized by high tire pressure.",
                            "formula": "F_friction ≤ μ · N",
                            "real_world_example": "Tire treads channel water away to prevent hydroplaning on rainy roads."
                        }
                    ],
                    "real_world_connection": "Modern high-speed trains and electric cars use the exact same gear-ratio and rolling-friction formulas tested on bicycles."
                },
                {
                    "subject": "Mathematics",
                    "title": "Circumference, Velocity, and Angular Speed",
                    "icon": "Calculator",
                    "concepts": [
                        {
                            "headline": "Distance per Wheel Revolution",
                            "explanation": "A standard 28-inch wheel has a diameter of ~71 cm, giving a circumference of C = 2 · π · r ≈ 2.23 meters. Each full rotation advances the rider 2.23 meters.",
                            "formula": "C = 2 · π · r",
                            "real_world_example": "If the wheel turns 4 times per second, the bike travels at 8.92 m/s (~32 km/h)."
                        }
                    ],
                    "real_world_connection": "Odometers and automotive speedometer sensors calculate vehicle speed using this wheel-circumference formula."
                },
                {
                    "subject": "Biology",
                    "title": "Human Biomechanics and Aerobic Energy",
                    "icon": "HeartPulse",
                    "concepts": [
                        {
                            "headline": "Muscular Force & Cellular Respiration",
                            "explanation": "The quadriceps, hamstrings, and calves contract sequentially. Your mitochondria burn glucose and oxygen to produce ATP, yielding ~25% mechanical efficiency with 75% dissipating as body heat.",
                            "formula": "C6H12O6 + 6O2 → 6CO2 + 6H2O + 32 ATP",
                            "real_world_example": "Sweating during hard cycling cools the body via evaporative heat loss."
                        }
                    ],
                    "real_world_connection": "Sports science utilizes watt-meters on pedals to monitor VO2-max and metabolic thresholds."
                },
                {
                    "subject": "Chemistry",
                    "title": "Materials Science: Alloys and Vulcanized Rubber",
                    "icon": "FlaskConical",
                    "concepts": [
                        {
                            "headline": "Vulcanized Rubber Polymers",
                            "explanation": "Natural latex is sticky and fragile until sulfur cross-links polymer chains during vulcanization, giving tires elastic recovery and temperature resistance.",
                            "formula": "Polyisoprene + Sulfur cross-links",
                            "real_world_example": "Tires stay elastic at -10°C and don't melt at +50°C."
                        }
                    ],
                    "real_world_connection": "Aircraft landing gear and prosthetic limbs utilize vulcanized elastomers and lightweight aluminum-scandium alloys."
                },
                {
                    "subject": "History",
                    "title": "The Evolution of Personal Mobility",
                    "icon": "Landmark",
                    "concepts": [
                        {
                            "headline": "From the Dandy Horse to Global Freedom",
                            "explanation": "Invented by Baron Karl von Drais in 1817 as the 'Laufmaschine' following the crop failure of 1816, the bicycle revolutionized personal transportation and supported early women's emancipation.",
                            "formula": "1817: Draisienne → 1885: Safety Bicycle",
                            "real_world_example": "Paved roads were originally championed by cyclists before automobiles existed!"
                        }
                    ],
                    "real_world_connection": "Urban planners today design eco-friendly smart cities centered around bicycle highways."
                },
                {
                    "subject": "Technology",
                    "title": "Modern Engineering & Electric Powertrains",
                    "icon": "Cpu",
                    "concepts": [
                        {
                            "headline": "Hydraulic Disc Brakes & Regenerative E-Bikes",
                            "explanation": "Pascal's principle in hydraulic disc brakes multiplies finger pressure into immense clamping force on steel rotors without rim wear.",
                            "formula": "P1 = P2 (F1/A1 = F2/A2)",
                            "real_world_example": "Modern e-bikes recharge batteries when rolling down slopes via regenerative braking."
                        }
                    ],
                    "real_world_connection": "Formula 1 cars and aircraft utilize the same high-pressure hydraulic braking physics."
                }
            ],
            "experiments": [
                {
                    "title": "Spinning Wheel Gyroscopic Stability Test",
                    "materials": ["Bicycle wheel removed from frame", "Sturdy string or rope (1 meter)"],
                    "steps": [
                        "Hold the axle of the bicycle wheel horizontally with both hands.",
                        "Have a friend spin the wheel as fast as possible.",
                        "Try quickly tilting the axle left and right—feel the mysterious resisting torque (gyroscopic precession)!",
                        "Tie one end of the string to only ONE side of the axle. Hold the string: the spinning wheel will remain upright and rotate horizontally instead of falling down!"
                    ],
                    "science_behind_it": "Conservation of angular momentum resists changes in the rotational axis, which explains how moving bicycles maintain dynamic stability.",
                    "safety_note": "Keep fingers away from spinning spokes."
                }
            ],
            "fun_facts": [
                {
                    "fact": "A bicycle is the most energetically efficient passenger vehicle on Earth.",
                    "why_cool": "A cyclist uses less energy to travel 1 km than a walking person, a bird in flight, or a car."
                },
                {
                    "fact": "Over 1 billion bicycles are in active use worldwide—double the number of cars!",
                    "why_cool": "In Amsterdam and Copenhagen, more than 40% of daily commutes are completed by bike."
                }
            ],
            "vocabulary": [
                {"term": "Angular Momentum", "definition": "A measure of the rotational motion of an object, conserved in closed systems."},
                {"term": "Gear Ratio", "definition": "The ratio between the number of teeth on the driving gear to the driven gear."},
                {"term": "Static Friction", "definition": "The frictional force that prevents surfaces from sliding past each other."},
                {"term": "Biomechanics", "definition": "The study of the mechanical laws relating to the movement or structure of living organisms."}
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "What happens when you shift to a higher gear ratio (e.g., from 2:1 to 3:1) on a flat road?",
                    "options": [
                        "You pedal with less effort and move slower",
                        "Each pedal stroke moves the bicycle further, but requires more pedal torque",
                        "The wheels produce zero friction with the ground",
                        "The bicycle becomes lighter"
                    ],
                    "correct_index": 1,
                    "explanation": "A higher gear ratio trades mechanical advantage for speed: one pedal turn rotates the wheel more times, advancing you further at the expense of higher pedal force.",
                    "subject": "Physics"
                },
                {
                    "id": 2,
                    "question": "What chemical process is used to make bicycle tires elastic, durable, and weather-resistant?",
                    "options": [
                        "Fermentation",
                        "Electrolysis",
                        "Vulcanization with sulfur cross-links",
                        "Photosynthesis"
                    ],
                    "correct_index": 2,
                    "explanation": "Vulcanization chemically bonds sulfur atoms between polyisoprene polymer chains, preventing rubber from becoming sticky in heat or brittle in cold.",
                    "subject": "Chemistry"
                },
                {
                    "id": 3,
                    "question": "Which physical principle explains why hydraulic disc brakes multiply finger pressure into powerful stopping force?",
                    "options": [
                        "Archimedes' principle",
                        "Pascal's principle (pressure is transmitted undiminished in enclosed fluid)",
                        "Newton's third law only",
                        "Bernoulli's equation"
                    ],
                    "correct_index": 1,
                    "explanation": "Pascal's principle states that pressure applied to an enclosed fluid is transmitted equally in all directions, so a small piston at the lever exerts massive force on larger brake caliper pistons.",
                    "subject": "Physics"
                },
                {
                    "id": 4,
                    "question": "If a bicycle wheel has a circumference of 2.2 meters, how far does it travel in 100 complete rotations?",
                    "options": [
                        "22 meters",
                        "110 meters",
                        "220 meters",
                        "440 meters"
                    ],
                    "correct_index": 2,
                    "explanation": "Total distance = Number of rotations × Circumference = 100 × 2.2 m = 220 meters.",
                    "subject": "Mathematics"
                }
            ]
        },
        "uz": {
            "name": "Velosiped",
            "name_en": "Bicycle",
            "category": "Transport va Mexanika Fizikasi",
            "educational_hook": "Velosiped — inson kuchi bilan harakatlanadigan haqiqiy mo'jiza! U Nyuton qonunlari, uzatma sonlari va inson biomexanikasini yaqqol ko'rsatib beradi.",
            "subjects_list": ["Fizika", "Matematika", "Biologiya", "Kimyo", "Texnologiya", "Tarix"],
            "title": "Velosiped Fizikasi va Muhandisligi: Qanday Harakatlanadi?",
            "summary": "Siz har safar velosiped pedalini bosganingizda, mushaklaringizdagi kimyoviy energiyani to'g'ridan-to'g'ri mexanik kinetik energiyaga aylantirasiz. G'ildiraklardagi burchak momenti saqlanishidan tortib zanjirli uzatma mexanizmigacha — velosiped haqiqiy ochiq osmon ostidagi fizika laboratoriyasidir.",
            "modules": [
                {
                    "subject": "Fizika",
                    "title": "Mexanika, Ishqalanish va Energiya Aylanishi",
                    "icon": "Atom",
                    "concepts": [
                        {
                            "headline": "Mexanik Yutuq va Uzatma Sonlari (Gear Ratios)",
                            "explanation": "Old zanjir yulduzchasi 48 ta tishli, orqadagisi 16 ta tishli bo'lsa, pedalning bir to'liq aylanishi g'ildirakni 3 marta aylantiradi (48/16 = 3:1). Bu tekis yo'lda tezlikni oshirishga imkon beradi.",
                            "formula": "Uzatma soni (i) = N_old / N_orqa",
                            "real_world_example": "Tik qiyaliklarga chiqayotganda old yulduzchani kichik, orqa yulduzchani katta qilsangiz, pedalni aylantirish osonlashadi."
                        },
                        {
                            "headline": "Ishqalanish: Harakatlantiruvchi Kuch",
                            "explanation": "G'ildirak shinasidagi rezina va asfalt o'rtasidagi tinchlikdagi ishqalanish kuchi velosipedni oldinga siljitadi. Shinalar qattiq damlanganda dumalanishdagi ishqalanish kamayadi.",
                            "formula": "F_ishqalanish ≤ μ · N",
                            "real_world_example": "Shina protektori (naqshi) yomg'irli havoda suvni chetga chiqarib, sirpanib ketishdan saqlaydi."
                        }
                    ],
                    "real_world_connection": "Tezyurar poyezdlar va elektromobillar velosipedda sinovdan o'tgan uzatma va ishqalanish tamoyillaridan foydalanadi."
                },
                {
                    "subject": "Matematika",
                    "title": "Aylana Uzunligi, Tezlik va Burchak Tezligi",
                    "icon": "Calculator",
                    "concepts": [
                        {
                            "headline": "G'ildirak Aylanishida Bosib O'tilgan Masofa",
                            "explanation": "Diametri 71 sm bo'lgan standart g'ildirakning aylanasi C = 2 · π · r ≈ 2.23 metrga teng. G'ildirak har bir to'liq aylanganda velosiped 2.23 metr oldinga siljiydi.",
                            "formula": "C = 2 · π · r  yoki  C = π · d",
                            "real_world_example": "Agar g'ildirak sekundiga 4 marta aylansa, velosiped tezligi 8.92 m/s (soatiga taxminan 32 km/soat) bo'ladi."
                        }
                    ],
                    "real_world_connection": "Avtomobil spidometri va navigatsiya tizimlari tezlikni aynan shu g'ildirak aylanasi formulasi orqali hisoblaydi."
                },
                {
                    "subject": "Biologiya",
                    "title": "Inson Biomexanikasi va Mushak Energiyasi",
                    "icon": "HeartPulse",
                    "concepts": [
                        {
                            "headline": "Mushak Qisqarishi va ATF Sintezi",
                            "explanation": "Son va boldir mushaklari ketma-ket qisqaradi. Mitoxondriyalar glyukoza va kisloroddan foydalanib ATF hosil qiladi. Inson energiyasining ~25% foydali ishga aylanadi, qolgan 75% esa issiqlik sifatida ajraladi.",
                            "formula": "C6H12O6 + 6O2 → 6CO2 + 6H2O + 32 ATF",
                            "real_world_example": "Velosipedda tez yurganda terlash tanani bug'lanish orqali sovitadi."
                        }
                    ],
                    "real_world_connection": "Sport tibbiyoti velosiped pedallaridagi datchiklar orqali yurak urishi va metabolizmni tahlil qiladi."
                },
                {
                    "subject": "Kimyo",
                    "title": "Materialshunoslik: Qotishmalar va Vulkanizatsiya",
                    "icon": "FlaskConical",
                    "concepts": [
                        {
                            "headline": "Vulkanizatsiyalangan Rezina",
                            "explanation": "Tabiiy kauchuk yopishqoq bo'ladi. Unga oltingugurt qo'shib qizdirilganda (vulkanizatsiya), polimer zanjirlar o'zaro ko'priklar hosil qiladi va shina elastik, issiq-sovuqqa chidamli bo'ladi.",
                            "formula": "Poliizopren + Oltingugurt ko'priklari (S)",
                            "real_world_example": "Shinalar -20°C sovuqda mo'rtlashib ketmaydi va +50°C issiqda erimaydi."
                        }
                    ],
                    "real_world_connection": "Samolyot shassisi va tibbiyot protezlarida engil alyuminiy-skandiy qotishmalari va vulkanizatsiya qilingan polimerlar ishlatiladi."
                },
                {
                    "subject": "Tarix",
                    "title": "Shaxsiy Harakatlanish Tarixi",
                    "icon": "Landmark",
                    "concepts": [
                        {
                            "headline": "Karl Drais 'Yuguruvchi Mashinasi'dan Zamonaviy Velosipedgacha",
                            "explanation": "1817-yilda nemis baroni Karl fon Drais otlar ochlik tufayli kamayib ketgach, birinchi yog'och velosipedni ixtiro qilgan. Keyinchalik bu transport insoniyat erkinligining ramziga aylandi.",
                            "formula": "1817: Drezina → 1885: Xavfsiz Velosiped (Rover)",
                            "real_world_example": "Shaharlardagi asfalt yo'llar dastlab avtomobillar uchun emas, balki velosipedchilar talabi bilan qurilgan!"
                        }
                    ],
                    "real_world_connection": "Bugungi kunda Kopengagen va Amsterdam kabi zamonaviy shaharlar velosiped ekotizimi asosida rejalashtirilmoqda."
                },
                {
                    "subject": "Texnologiya",
                    "title": "Zamonaviy Muhandislik va Gidravlik Tizimlar",
                    "icon": "Cpu",
                    "concepts": [
                        {
                            "headline": "Gidravlik Diskli Tormozlar",
                            "explanation": "Paskal qonuniga ko'ra, berk suyuqlikka berilgan bosim har tomonga bir xil tarqaladi. Barmog'ingizning kichik kuchi tormoz diskiga bir necha yuz kilogramm kuch bilan ta'sir qiladi.",
                            "formula": "P1 = P2  ⇒  F1 / S1 = F2 / S2",
                            "real_world_example": "Elektr velosipedlar pastlikka tushayotganda rekuperatsiya orqali batareyasini qayta zaryadlaydi."
                        }
                    ],
                    "real_world_connection": "Formula-1 poyga mashinalari va samolyot tormozlarida aynan shu yuqori bosimli gidravlika qonuni ishlaydi."
                }
            ],
            "experiments": [
                {
                    "title": "Aylanayotgan G'ildirak va Giroskop Effekti",
                    "materials": ["Velosipeddan yechilgan old g'ildirak", "Mustahkam arqon (1 metr)"],
                    "steps": [
                        "Velosiped g'ildiragining o'qidan ikki qo'lingiz bilan gorizontal ushlab turing.",
                        "Do'stingizdan g'ildirakni imkon qadar tez aylantirishini so'rang.",
                        "G'ildirakni o'ngga yoki chapga burishga harakat qilib ko'ring — qo'llaringizda g'alati qarshilik kuchini sezasiz!",
                        "Arqonni o'qning faqat BIR tomoniga bog'lab, havoda ushlang: g'ildirak pastga tushib ketmaydi, balki tik turgan holda sekin aylanadi!"
                    ],
                    "science_behind_it": "Burchak momenti (impuls momenti) saqlanish qonuni aylanish o'qining o'zgarishiga qarshilik ko'rsatadi. Velosiped harakatlanayotganda muvozanatni saqlashga aynan shu giroskop effekti va boshqaruv dinamikasi yordam beradi.",
                    "safety_note": "Aylanayotgan simlar orasiga barmoqlaringizni tiqmang."
                }
            ],
            "fun_facts": [
                {
                    "fact": "Velosiped — sayyoramizdagi eng tejamkor transport vositasidir.",
                    "why_cool": "1 kilometr masofani bosib o'tish uchun velosipedchi piyoda yuruvchi odamdan, uchayotgan qushdan yoki mashinadan ancha kam kaloriya sarflaydi!"
                },
                {
                    "fact": "Dunyoda 1 milliarddan ortiq velosiped bor — bu mashinalar sonidan deyarli ikki barobar ko'p!",
                    "why_cool": "Gollandiyada har bir aholiga o'rtacha 1.3 ta velosiped to'g'ri keladi."
                }
            ],
            "vocabulary": [
                {"term": "Burchak momenti", "definition": "Jismning aylanish harakatini ifodalovchi va berk tizimda saqlanuvchi fizik kattalik."},
                {"term": "Uzatma soni", "definition": "Yetakchi yulduzcha tishlari sonining yetaklanuvchi yulduzcha tishlari soniga nisbati."},
                {"term": "Tinchlikdagi ishqalanish", "definition": "Jism siljishini to'xtatib turuvchi va harakatlanish uchun tirgak bo'luvchi kuch."},
                {"term": "Biomexanika", "definition": "Tirik organizmlarning harakati va mushaklarining mexanik qonuniyatlarini o'rganuvchi fan."}
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Tekis yo'lda velosiped uzatmasini kattaroq songa o'tkazsangiz (masalan, 2:1 dan 3:1 ga), nima sodir bo'ladi?",
                    "options": [
                        "Pedalni aylantirish osonlashadi, lekin tezlik kamayadi",
                        "Pedalning bir aylanishida velosiped uzoqroq masofani bosib o'tadi, lekin ko'proq kuch talab qilinadi",
                        "G'ildirak yer bilan ishqalanishni butunlay to'xtatadi",
                        "Velosipedning og'irligi kamayadi"
                    ],
                    "correct_index": 1,
                    "explanation": "Katta uzatma soni kuchdan yutqazib, yo'ldan yutish tamoyiliga asoslanadi: pedalning bir to'liq aylanishi g'ildirakni 3 marta aylantiradi va tezlikni oshiradi.",
                    "subject": "Fizika"
                },
                {
                    "id": 2,
                    "question": "Velosiped shinalarini elastik, bardoshli va yorilib ketmaydigan qilish uchun qanday kimyoviy jarayon qo'llaniladi?",
                    "options": [
                        "Bijg'ish (fermentatsiya)",
                        "Elektroliz",
                        "Oltingugurt bilan vulkanizatsiyalash",
                        "Fotosintez"
                    ],
                    "correct_index": 2,
                    "explanation": "Vulkanizatsiya jarayonida oltingugurt atomlari kauchuk polimerlari o'rtasida mustahkam ko'priklar hosil qiladi, natijada rezina harorat o'zgarishlariga chidamli bo'ladi.",
                    "subject": "Kimyo"
                },
                {
                    "id": 3,
                    "question": "Gidravlik diskli tormozda barmoqning kichik kuchi bir necha yuz kilogrammlik tormoz kuchiga aylanishiga qaysi qonun sabab bo'ladi?",
                    "options": [
                        "Arximed qonuni",
                        "Paskal qonuni (suyuqlikdagi bosim barcha tomonga teng uzatiladi)",
                        "Faqat Nyutonning uchinchi qonuni",
                        "Bernulli tenglamasi"
                    ],
                    "correct_index": 1,
                    "explanation": "Paskal qonuniga binoan, kichik porshen orqali suyuqlikka berilgan bosim kattaroq yuzali tormoz porshenlariga teng uzatilib, kuchni bir necha barobar oshiradi.",
                    "subject": "Fizika"
                },
                {
                    "id": 4,
                    "question": "Agar velosiped g'ildiragining aylanasi uzunligi 2.2 metr bo'lsa, u 100 marta to'liq aylanganda necha metr masofani bosib o'tadi?",
                    "options": [
                        "22 metr",
                        "110 metr",
                        "220 metr",
                        "440 metr"
                    ],
                    "correct_index": 2,
                    "explanation": "Masofa = Aylanishlar soni × Aylana uzunligi = 100 × 2.2 m = 220 metr.",
                    "subject": "Matematika"
                }
            ]
        },
        "ru": {
            "name": "Велосипед",
            "name_en": "Bicycle",
            "category": "Транспорт и Механика",
            "educational_hook": "Велосипед — это чудо инженерной мысли, приводимое в движение силой человека! Он наглядно демонстрирует законы Ньютона, передаточные числа и биомеханику.",
            "subjects_list": ["Физика", "Математика", "Биология", "Химия", "Технологии", "История"],
            "title": "Физика и инженерия велосипеда",
            "summary": "Каждый раз, нажимая на педали, вы преобразуете химическую энергию мышц в кинетическую механическую энергию. От гироскопического эффекта вращающихся колес до зубчатых передач — велосипед является лабораторией под открытым небом.",
            "modules": [
                {
                    "subject": "Физика",
                    "title": "Механика, трение и сохранение энергии",
                    "icon": "Atom",
                    "concepts": [
                        {
                            "headline": "Передаточное число и механическое преимущество",
                            "explanation": "Если передняя звезда имеет 48 зубьев, а задняя 16, один оборот педалей вращает колесо 3 раза (48/16 = 3:1). Это увеличивает скорость на ровной дороге.",
                            "formula": "Передаточное число = N_перед / N_задн",
                            "real_world_example": "При подъеме в гору включают меньшую переднюю и большую заднюю звезду для снижения крутящего момента на педалях."
                        }
                    ],
                    "real_world_connection": "Скоростные поезда и автомобили используют те же формулы передаточных отношений и трения качения."
                },
                {
                    "subject": "Математика",
                    "title": "Длина окружности, угловая скорость и расчет пути",
                    "icon": "Calculator",
                    "concepts": [
                        {
                            "headline": "Расстояние за один оборот колеса",
                            "explanation": "При диаметре колеса 71 см длина окружности C = 2·π·r ≈ 2.23 м. При 4 оборотах в секунду скорость составляет 8.92 м/с (~32 км/ч).",
                            "formula": "C = 2 · π · r",
                            "real_world_example": "Спидометры автомобилей вычисляют скорость по частоте вращения колес."
                        }
                    ],
                    "real_world_connection": "Автомобильные одометры и датчики ABS работают на основе этой формулы."
                },
                {
                    "subject": "Биология",
                    "title": "Биомеханика и мышечная энергия",
                    "icon": "HeartPulse",
                    "concepts": [
                        {
                            "headline": "Мышечные сокращения и АТФ",
                            "explanation": "Мышцы ног последовательно сокращаются. Митохондрии расщепляют глюкозу с образованием молекул АТФ с КПД около 25%. Оставшиеся 75% рассеиваются в виде тепла.",
                            "formula": "C6H12O6 + 6O2 → 6CO2 + 6H2O + 32 АТФ",
                            "real_world_example": "Потоотделение защищает организм от перегрева за счет испарения воды."
                        }
                    ],
                    "real_world_connection": "Спортивная медицина контролирует метаболический порог велосипедистов через измерители мощности на педалях."
                },
                {
                    "subject": "Химия",
                    "title": "Материаловедение: Вулканизация резины",
                    "icon": "FlaskConical",
                    "concepts": [
                        {
                            "headline": "Вулканизированная резина",
                            "explanation": "Сшивка полимерных цепей каучука атомами серы придает шинам эластичность, термостойкость и прочность на разрыв.",
                            "formula": "Полиизопрен + Серные мостики",
                            "real_world_example": "Шины не трескаются при морозе -20°C и не плавятся на раскаленном асфальте."
                        }
                    ],
                    "real_world_connection": "Авиационные шасси и медицинские протезы используют аналогичные вулканизированные эластомеры."
                },
                {
                    "subject": "История",
                    "title": "Эволюция мобильности человека",
                    "icon": "Landmark",
                    "concepts": [
                        {
                            "headline": "От беговой машины Дреза к свободе передвижения",
                            "explanation": "Изобретенная бароном Карлом Дрезом в 1817 году 'машина для бега' стала прорывом после голода 1816 года и положила начало эмансипации и городскому транспорту.",
                            "formula": "1817: Дрезина → 1885: Безопасный велосипед",
                            "real_world_example": "Первые мощеные дороги в Европе и Америке строились именно по требованию велосипедистов!"
                        }
                    ],
                    "real_world_connection": "Современные европейские города строятся вокруг веломагистралей."
                },
                {
                    "subject": "Технологии",
                    "title": "Гидравлические тормоза и рекуперация",
                    "icon": "Cpu",
                    "concepts": [
                        {
                            "headline": "Закон Паскаля в дисковых тормозах",
                            "explanation": "Давление в замкнутой несжимаемой жидкости передается во всех направлениях одинаково, превращая легкое нажатие пальца в огромное прижимное усилие.",
                            "formula": "P1 = P2 (F1/S1 = F2/S2)",
                            "real_world_example": "Электровелосипеды заряжают аккумулятор при торможении на спусках."
                        }
                    ],
                    "real_world_connection": "В болидах Формулы-1 и самолетах применяется тот же гидравлический принцип торможения."
                }
            ],
            "experiments": [
                {
                    "title": "Гироскопический эффект вращающегося колеса",
                    "materials": ["Снятое велосипедное колесо", "Крепкая веревка (1 м)"],
                    "steps": [
                        "Возьмитесь двумя руками за ось колеса.",
                        "Попросите друга сильно раскрутить колесо.",
                        "Попробуйте быстро наклонить ось вправо и влево — почувствуйте сопротивление (гироскопическую прецессию)!",
                        "Привяжите веревку только к одному концу оси и поднимите: вращающееся колесо не упадет, а будет висеть горизонтально и медленно поворачиваться!"
                    ],
                    "science_behind_it": "Закон сохранения момента импульса противится изменению оси вращения. Это один из факторов динамической устойчивости двухколесного транспорта.",
                    "safety_note": "Не вставляйте пальцы между спицами вращающегося колеса."
                }
            ],
            "fun_facts": [
                {
                    "fact": "Велосипед — самый энергоэффективный пассажирский транспорт на Земле.",
                    "why_cool": "Человек на велосипеде тратит меньше энергии на 1 км, чем пешеход, птица в полете или автомобиль."
                }
            ],
            "vocabulary": [
                {"term": "Момент импульса", "definition": "Физическая величина, характеризующая вращательное движение объекта."},
                {"term": "Передаточное число", "definition": "Отношение числа зубьев ведущей шестерни к числу зубьев ведомой."},
                {"term": "Сила трения покоя", "definition": "Сила, возникающая между соприкасающимися телами и препятствующая их относительному движению."}
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Что происходит при переключении на более высокую передачу (например, с 2:1 на 3:1)?",
                    "options": [
                        "Педали крутятся легче, скорость падает",
                        "За один оборот педалей колесо проходит большее расстояние, но требуется большее усилие",
                        "Трение полностью исчезает",
                        "Велосипед становится легче"
                    ],
                    "correct_index": 1,
                    "explanation": "Высокое передаточное отношение дает выигрыш в пути ценой проигрыша в силе.",
                    "subject": "Физика"
                },
                {
                    "id": 2,
                    "question": "Какой химический процесс делает покрышки прочными и эластичными при любой температуре?",
                    "options": [
                        "Ферментация",
                        "Электролиз",
                        "Вулканизация серой",
                        "Фотосинтез"
                    ],
                    "correct_index": 2,
                    "explanation": "Сшивка полимерных нитей каучука атомами серы называется вулканизацией.",
                    "subject": "Химия"
                },
                {
                    "id": 3,
                    "question": "Какой закон физики объясняет многократное усиление силы в гидравлических тормозах?",
                    "options": [
                        "Закон Архимеда",
                        "Закон Паскаля о передаче давления жидкостью",
                        "Закон Гука",
                        "Уравнение Бернулли"
                    ],
                    "correct_index": 1,
                    "explanation": "Закон Паскаля утверждает, что давление в жидкости передается одинаково во всех направлениях.",
                    "subject": "Физика"
                }
            ]
        }
    },
    "plant": {
        "en": {
            "name": "Green Plant Leaf",
            "name_en": "Plant Leaf",
            "category": "Botanical Biology & Photosynthesis",
            "educational_hook": "A single green leaf is a quantum solar-powered sugar factory converting sunlight, carbon dioxide, and water into the oxygen we breathe!",
            "subjects_list": ["Biology", "Chemistry", "Physics", "Mathematics", "Technology", "History"],
            "title": "The Quantum Biology & Chemistry of Photosynthesis",
            "summary": "Leaves are nature's solar panels. Inside every plant cell, microscopic chloroplasts harvest photons from the Sun to split water molecules and synthesize energy-rich glucose, powering the planetary biosphere.",
            "modules": [
                {
                    "subject": "Biology",
                    "title": "Cellular Anatomy & Stomata Gas Exchange",
                    "icon": "Leaf",
                    "concepts": [
                        {
                            "headline": "Chloroplasts and Thylakoid Grana",
                            "explanation": "Plant cells contain chloroplasts packed with thylakoid membranes. Chlorophyll pigments absorb photons in the blue and red wavelengths while reflecting green light.",
                            "formula": "6CO2 + 6H2O + Sunlight → C6H12O6 + 6O2",
                            "real_world_example": "Stomata pores on the underside of leaves open and close using turgor pressure to balance CO2 intake with water vapor loss."
                        }
                    ],
                    "real_world_connection": "Agricultural drones detect crop health by measuring infrared reflectance of leaf chlorophyll."
                },
                {
                    "subject": "Physics",
                    "title": "Quantum Optics & Capillary Transpiration",
                    "icon": "Atom",
                    "concepts": [
                        {
                            "headline": "Capillary Action and Cohesion-Tension Theory",
                            "explanation": "Water ascends from roots to the highest tree branches (up to 100 meters) against gravity through xylem micro-tubes via hydrogen bonding cohesion and evaporation pull.",
                            "formula": "h = (2 · γ · cos θ) / (ρ · g · r)",
                            "real_world_example": "A mature oak tree transpires over 400 liters of water into the atmosphere daily."
                        }
                    ],
                    "real_world_connection": "Microfluidic cooling systems in supercomputers are modeled after plant vascular xylem networks."
                },
                {
                    "subject": "Mathematics",
                    "title": "Fibonacci Sequences in Leaf Phyllotaxis",
                    "icon": "Calculator",
                    "concepts": [
                        {
                            "headline": "The Golden Angle (137.5°)",
                            "explanation": "Leaves sprout along stems spaced at the Golden Angle (137.5°). This mathematical arrangement prevents upper leaves from casting shadows on lower leaves, maximizing sunlight capture.",
                            "formula": "Φ = (1 + √5) / 2 ≈ 1.618  |  Angle = 360° / Φ² ≈ 137.5°",
                            "real_world_example": "Sunflower seeds and pinecone spirals follow the exact same Fibonacci numbers (13, 21, 34, 55)."
                        }
                    ],
                    "real_world_connection": "Concentrated solar thermal plants arrange solar mirrors in Fibonacci spirals to minimize shadow overlap."
                }
            ],
            "experiments": [
                {
                    "title": "Underwater Photosynthesis Oxygen Bubbles",
                    "materials": ["Fresh green leaf", "Clear glass bowl or jar", "Water", "Small pebble or weight", "Direct sunlight or bright lamp"],
                    "steps": [
                        "Fill a transparent glass bowl with room-temperature water.",
                        "Submerge the fresh leaf completely and weigh it down gently with a small pebble so it stays under water.",
                        "Place the bowl under direct sunlight or a strong lamp.",
                        "Wait 30–60 minutes and observe: dozens of tiny silver bubbles will form on the leaf surface and rise up!"
                    ],
                    "science_behind_it": "The bubbles are pure oxygen (O2) produced as the chloroplasts split water molecules during the light-dependent reactions of photosynthesis.",
                    "safety_note": "Handle glass jars carefully."
                }
            ],
            "fun_facts": [
                {
                    "fact": "Every second, Earth's plants convert 100 terawatts of solar energy into chemical bonds.",
                    "why_cool": "That is roughly 6 times more power than the entire human civilization consumes!"
                }
            ],
            "vocabulary": [
                {"term": "Photosynthesis", "definition": "The biochemical process by which plants use sunlight to synthesize nutrients from CO2 and water."},
                {"term": "Chlorophyll", "definition": "The green pigment found in cyanobacteria and chloroplasts of plants that absorbs light."},
                {"term": "Phyllotaxis", "definition": "The arrangement of leaves on an axis or stem."}
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "What gas do plants release into the atmosphere as a byproduct of photosynthesis?",
                    "options": ["Carbon dioxide (CO2)", "Oxygen (O2)", "Methane (CH4)", "Nitrogen (N2)"],
                    "correct_index": 1,
                    "explanation": "During the photolysis of water in the light reaction, oxygen atoms from H2O molecules are combined and released as O2 gas.",
                    "subject": "Biology"
                },
                {
                    "id": 2,
                    "question": "Why do most plant leaves appear green to human eyes?",
                    "options": [
                        "Because chlorophyll absorbs only green wavelengths",
                        "Because chlorophyll absorbs red and blue light and reflects green light",
                        "Because leaves contain green food coloring",
                        "Because nitrogen glows green in daylight"
                    ],
                    "correct_index": 1,
                    "explanation": "Chlorophyll a and b pigments have absorption peaks in the blue (430 nm) and red (660 nm) parts of the spectrum, while reflecting green light (500–550 nm).",
                    "subject": "Physics"
                }
            ]
        },
        "uz": {
            "name": "O'simlik Bargi",
            "name_en": "Plant Leaf",
            "category": "Botanika va Fotosintez Biologiyasi",
            "educational_hook": "Oddiy yashil barg — quyosh nuri, karbonat angidrid va suvdan biz nafas oladigan kislorodni ishlab chiqaradigan tabiatning kvant quyosh batareyasidir!",
            "subjects_list": ["Biologiya", "Kimyo", "Fizika", "Matematika", "Texnologiya", "Tarix"],
            "title": "Fotosintez Kvant Biologiyasi va Kimyosi",
            "summary": "Barglar — tabiatning eng mukammal quyosh panellaridir. O'simlik hujayralaridagi mikroskopik xloroplastlar quyosh fotonlarini yutib, suv molekulalarini parchalaydi va butun Yer biosferasini energiya bilan ta'minlaydigan glyukozani sintez qiladi.",
            "modules": [
                {
                    "subject": "Biologiya",
                    "title": "Hujayra Anatomiyasi va Og'izchalar (Stomata)",
                    "icon": "Leaf",
                    "concepts": [
                        {
                            "headline": "Xloroplastlar va Xlorofill Pigmenti",
                            "explanation": "Barg hujayralarida xloroplastlar joylashgan. Xlorofill pigmenti spektrning ko'k va qizil nurlarini yutadi, yashil rangni esa qaytaradi. Barg ostidagi og'izchalar (stomata) orqali gaz almashinuvi sodir bo'ladi.",
                            "formula": "6CO2 + 6H2O + Quyosh nuri → C6H12O6 + 6O2",
                            "real_world_example": "Qurg'oqchilikda og'izchalar yopilib, o'simlik suv yo'qotishining oldini oladi."
                        }
                    ],
                    "real_world_connection": "Qishloq xo'jaligi dronlari ekinlarning xlorofill spektrini tahlil qilib, ularning hosildorligini nazorat qiladi."
                },
                {
                    "subject": "Fizika",
                    "title": "Kvant Optikasi va Kapillyar Bosim",
                    "icon": "Atom",
                    "concepts": [
                        {
                            "headline": "Kapillyar Harakat va Koheziya Kuchlari",
                            "explanation": "Suv tomirlar (ksilema) orqali tortishish kuchiga qarshi 100 metr balandlikdagi daraxt cho'qqisiga ham ko'tarila oladi. Bunga suv molekulalarining vodorod bog'lari va transpiratsiya so'rish kuchi sabab bo'ladi.",
                            "formula": "h = (2 · γ · cos θ) / (ρ · g · r)",
                            "real_world_example": "Katta eman daraxti bir kunda havoga 400 litrgacha suv bug'latadi."
                        }
                    ],
                    "real_world_connection": "Superkompyuterlarni sovitishda o'simlik ksilemasi kapillyarlariga o'xshash mikrosuyuqlik tizimlari qo'llaniladi."
                },
                {
                    "subject": "Matematika",
                    "title": "Fibonachchi Qonuni va Oltin Burchak (137.5°)",
                    "icon": "Calculator",
                    "concepts": [
                        {
                            "headline": "Barglarning Poyada Joylashishi",
                            "explanation": "Barglar poya atrofida aynan 137.5° (Oltin burchak) burchak ostida chiqadi. Bu matematik qonuniyat yuqori barglarning quyi barglarga soya solishiga yo'l qo'ymaydi va yorug'likdan maksimal foydalanishni ta'minlaydi.",
                            "formula": "Oltin burchak ≈ 137.5° (Fibonachchi nisbati)",
                            "real_world_example": "Kungaboqar urug'lari va qarag'ay qubbalari aynan shu Fibonachchi qatoriga bo'ysunadi."
                        }
                    ],
                    "real_world_connection": "Quyosh elektr stansiyalarida nometall panellar soyalanmasligi uchun Fibonachchi spirali bo'yicha teriladi."
                }
            ],
            "experiments": [
                {
                    "title": "Suv Ostida Fotosintez Kislorodini Ko'rish",
                    "materials": ["Yangi uzilgan yashil barg", "Shaffof shisha idish", "Suv", "Kichik toshcha", "Quyosh nuri yoki yorug' chiroq"],
                    "steps": [
                        "Shaffof shisha idishga toza suv to'ldiring.",
                        "Yashil bargni suvga to'liq botiring va suzib chiqmasligi uchun ustiga kichik toshcha qo'ying.",
                        "Idishni to'g'ridan-to'g'ri quyosh nuri tushadigan joyga qo'ying.",
                        "30–60 daqiqa kuting: barg yuzasida o'nlab kumushrang mayda pufakchalar paydo bo'lib, yuqoriga ko'tariladi!"
                    ],
                    "science_behind_it": "Bu pufakchalar barg xloroplastlari suv molekulalarini parchalaganda ajralib chiqadigan sof kislorod (O2) gazidir.",
                    "safety_note": "Shisha idish bilan ehtiyotkorlik bilan muomala qiling."
                }
            ],
            "fun_facts": [
                {
                    "fact": "Yer yuzidagi barcha o'simliklar har soniyada 100 teravatt quyosh energiyasini kimyoviy energiyaga aylantiradi.",
                    "why_cool": "Bu butun insoniyat iste'mol qiladigan elektr quvvatidan 6 baravar ko'pdir!"
                }
            ],
            "vocabulary": [
                {"term": "Fotosintez", "definition": "O'simliklarning quyosh nuri ta'sirida noorganik moddalardan organik moddalar sintez qilish jarayoni."},
                {"term": "Xlorofill", "definition": "O'simliklarga yashil rang beruvchi va yorug'lik energiyasini yutuvchi pigment."},
                {"term": "Ksilema", "definition": "O'simliklarda suv va erigan mineral moddalarni ildizdan barglarga yetkazuvchi o'tkazuvchi to'qima."}
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Fotosintez natijasida o'simliklar havoga qanday gaz chiqaradi?",
                    "options": ["Karbonat angidrid (CO2)", "Kislorod (O2)", "Metan (CH4)", "Azot (N2)"],
                    "correct_index": 1,
                    "explanation": "Fotosintezning yorug'lik bosqichida suv fotolizga uchrab, yon mahsulot sifatida kislorod (O2) havoga ajralib chiqadi.",
                    "subject": "Biologiya"
                },
                {
                    "id": 2,
                    "question": "Nima sababdan o'simlik barglari bizga yashil bo'lib ko'rinadi?",
                    "options": [
                        "Xlorofill faqat yashil nurni yutgani uchun",
                        "Xlorofill qizil va ko'k nurlarni yutib, yashil nurni qaytargani uchun",
                        "Bargda yashil bo'yoq bo'lgani uchun",
                        "Azot gazi kunduzi yashil porlagani uchun"
                    ],
                    "correct_index": 1,
                    "explanation": "Xlorofill molekulasi spektrdagi ko'k va qizil to'lqin uzunliklarini faol yutadi, foydalanilmagan yashil nurlar esa ko'zimizga qaytadi.",
                    "subject": "Fizika"
                }
            ]
        },
        "ru": {
            "name": "Зеленый лист растения",
            "name_en": "Plant Leaf",
            "category": "Биология и Фотосинтез",
            "educational_hook": "Обычный зеленый лист — это квантовая солнечная фабрика, превращающая солнечный свет, воду и углекислый газ в кислород!",
            "subjects_list": ["Биология", "Химия", "Физика", "Математика", "Технологии", "История"],
            "title": "Квантовая биология и химия фотосинтеза",
            "summary": "Листья — совершенные природные солнечные батареи. Внутри каждой растительной клетки хлоропласты улавливают фотоны и расщепляют воду, синтезируя глюкозу и поддерживая биосферу Земли.",
            "modules": [
                {
                    "subject": "Биология",
                    "title": "Хлоропласты и газообмен устьиц",
                    "icon": "Leaf",
                    "concepts": [
                        {
                            "headline": "Фотосинтез и пигмент хлорофилл",
                            "explanation": "Хлорофилл поглощает кванты красного и синего спектра, отражая зеленый. Устьица на нижней стороне листа регулируют поступление CO2 и испарение воды.",
                            "formula": "6CO2 + 6H2O + Свет → C6H12O6 + 6O2",
                            "real_world_example": "В засуху устьица закрываются для сохранения влаги."
                        }
                    ],
                    "real_world_connection": "Сельскохозяйственные спутники оценивают состояние полей по спектру отражения хлорофилла."
                }
            ],
            "experiments": [
                {
                    "title": "Выделение кислорода листом под водой",
                    "materials": ["Свежий лист", "Прозрачный стакан с водой", "Камешек", "Солнечный свет"],
                    "steps": [
                        "Опустите лист в стакан с водой и зафиксируйте камешком.",
                        "Поставьте на яркий солнечный свет на 40 минут.",
                        "Наблюдайте образование пузырьков кислорода на поверхности листа!"
                    ],
                    "science_behind_it": "Пузырьки представляют собой чистый кислород, выделяемый при фотолизе воды.",
                    "safety_note": "Аккуратно обращайтесь со стеклом."
                }
            ],
            "fun_facts": [
                {
                    "fact": "Растения Земли вырабатывают в 6 раз больше энергии, чем потребляет все человечество.",
                    "why_cool": "Это около 100 тераватт непрерывной мощности биосферы."
                }
            ],
            "vocabulary": [
                {"term": "Фотосинтез", "definition": "Процесс синтеза органических веществ из неорганических за счет энергии света."},
                {"term": "Хлорофилл", "definition": "Зеленый растительный пигмент, обуславливающий поглощение света."}
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Какой газ выделяется растениями в процессе фотосинтеза?",
                    "options": ["Углекислый газ", "Кислород", "Азот", "Водород"],
                    "correct_index": 1,
                    "explanation": "В световой фазе фотосинтеза при фотолизе воды выделяется кислород O2.",
                    "subject": "Биология"
                }
            ]
        }
    }
}

def get_fallback_detected_objects(keyword: str, language: str = "uz"):
    """Returns detected educational objects matching keyword or defaults to classroom items."""
    k = keyword.lower()
    if any(w in k for w in ["velosiped", "bike", "bicycle", "cycle", "koleso", "велосипед"]):
        obj_key = "bicycle"
    elif any(w in k for w in ["barg", "leaf", "plant", "gul", "flower", "tree", "daraxt", "растение", "лист"]):
        obj_key = "plant"
    else:
        obj_key = "bicycle"

    data = MOCK_CATALOG.get(obj_key, MOCK_CATALOG["bicycle"])
    lang_data = data.get(language, data.get("uz", data["en"]))

    primary = {
        "name": lang_data["name"],
        "name_en": lang_data["name_en"],
        "category": lang_data["category"],
        "educational_hook": lang_data["educational_hook"],
        "subjects": lang_data["subjects_list"],
        "confidence": 0.98,
        "bounding_box": {"ymin": 0.1, "xmin": 0.1, "ymax": 0.9, "xmax": 0.9}
    }

    # Additional contextual components in the scene
    if obj_key == "bicycle":
        components = [
            primary,
            {
                "name": "G'ildirak va Shina" if language == "uz" else ("Wheel & Tire" if language == "en" else "Колесо и шина"),
                "name_en": "Wheel & Tire",
                "category": "Fizika & Materialshunoslik" if language == "uz" else "Physics & Materials",
                "educational_hook": "Dumalanishdagi ishqalanish, aylanma harakat va polimer rezinaning vulkanizatsiyasi." if language == "uz" else "Rolling friction, rotational inertia, and vulcanized rubber polymers.",
                "subjects": ["Fizika", "Kimyo", "Matematika"] if language == "uz" else ["Physics", "Chemistry", "Mathematics"],
                "confidence": 0.93,
                "bounding_box": {"ymin": 0.45, "xmin": 0.55, "ymax": 0.92, "xmax": 0.95}
            },
            {
                "name": "Zanjir va Yulduzchalar" if language == "uz" else ("Chain & Derailleur Gears" if language == "en" else "Цепь и зубчатые шестерни"),
                "name_en": "Chain Drive",
                "category": "Mashinasozlik" if language == "uz" else "Mechanical Engineering",
                "educational_hook": "Mexanik quvvat uzatish, moment va tishli g'ildiraklar nisbati." if language == "uz" else "Mechanical torque transfer and gear tooth ratios.",
                "subjects": ["Fizika", "Texnologiya", "Matematika"] if language == "uz" else ["Physics", "Technology", "Mathematics"],
                "confidence": 0.89,
                "bounding_box": {"ymin": 0.55, "xmin": 0.35, "ymax": 0.85, "xmax": 0.65}
            }
        ]
    else:
        components = [
            primary,
            {
                "name": "Xloroplastlar va Hujayra Strukturasi" if language == "uz" else ("Chloroplasts & Micro-anatomy" if language == "en" else "Хлоропласты и микроструктура"),
                "name_en": "Chloroplasts",
                "category": "Hujayra Biologiyasi" if language == "uz" else "Cell Biology",
                "educational_hook": "Yorug'lik energiyasini kimyoviy bog'larga aylantiruvchi biologik nanofabrika." if language == "uz" else "Biological nanofactories transforming photon energy into chemical glucose bonds.",
                "subjects": ["Biologiya", "Kimyo"] if language == "uz" else ["Biology", "Chemistry"],
                "confidence": 0.91,
                "bounding_box": {"ymin": 0.2, "xmin": 0.2, "ymax": 0.8, "xmax": 0.8}
            }
        ]

    return components

def get_fallback_lesson(object_name: str, language: str = "uz"):
    """Returns a full educational lesson from the mock catalog."""
    k = object_name.lower()
    if any(w in k for w in ["barg", "leaf", "plant", "gul", "flower", "растение", "лист"]):
        obj_key = "plant"
    else:
        obj_key = "bicycle"

    data = MOCK_CATALOG.get(obj_key, MOCK_CATALOG["bicycle"])
    return data.get(language, data.get("uz", data["en"]))
